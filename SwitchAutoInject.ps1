<#
SwitchAutoInject - injiziert automatisch NUR ein per SHA256 verifiziertes Payload
(Standard: Hekate 6.5.5), sobald eine Switch V1 im RCM-Modus (USB 0955:7321)
angeschlossen wird.

Sicherheit:
- Es wird ausschliesslich eine Datei injiziert, deren SHA256 exakt dem
  konfigurierten Hash entspricht. Der Hash wird VOR JEDER Injektion neu berechnet;
  injiziert werden genau die geprueften Bytes (Kopie im Temp-Ordner).
- Ohne Freigabe (-Approve) wird nie injiziert, nur erkannt und protokolliert.
  Die Freigabe ist an den Hash gebunden; ein anderer Hash braucht eine neue Freigabe.
- Das Tool schreibt nichts auf die Switch (kein NAND, kein BOOT0), es schickt das
  Payload nur per RCM in den RAM.

Konfiguration: config.json neben diesem Skript (Vorlage: config.example.json).
Relative Pfade gelten relativ zum Skriptordner. Parameter ueberschreiben die Datei.

Aufrufe:
  .\SwitchAutoInject.ps1 -Approve     Freigabe erteilen (an den Hash gebunden)
  .\SwitchAutoInject.ps1 -Revoke      Freigabe zuruecknehmen
  .\SwitchAutoInject.ps1 -DryRun      Nur erkennen + Hash pruefen, nichts injizieren
  .\SwitchAutoInject.ps1 -Once        Eine Injektion, dann beenden
  .\SwitchAutoInject.ps1              Dauerbetrieb (so laeuft es per Autostart)
#>
[CmdletBinding()]
param(
    [switch]$Approve,
    [switch]$Revoke,
    [switch]$DryRun,
    [switch]$Once,
    [string]$ConfigPath,
    [string]$PayloadPath,
    [string]$PayloadSha256,
    [string]$SmashExe,
    [int]$PollSeconds = 0
)

$ErrorActionPreference = 'Stop'

# --- Konfiguration -------------------------------------------------------------
$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $ConfigPath) { $ConfigPath = Join-Path $ScriptDir 'config.json' }
$cfg = @{
    PayloadPath   = 'payload\hekate_ctcaer_6.5.5.bin'
    PayloadSha256 = '09752ABD207803708ADD6E22151E94B71FFBAAFF769D1BAD759584B76EF6F05E'
    SmashExe      = 'C:\Program Files (x86)\TegraRcmGUI\TegraRcmSmash.exe'
    PollSeconds   = 2
    MaxTries      = 3
}
if (Test-Path -LiteralPath $ConfigPath) {
    $json = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
    foreach ($p in $json.PSObject.Properties) { if ($null -ne $p.Value -and "$($p.Value)" -ne '') { $cfg[$p.Name] = $p.Value } }
}
if ($PayloadPath)   { $cfg.PayloadPath   = $PayloadPath }
if ($PayloadSha256) { $cfg.PayloadSha256 = $PayloadSha256 }
if ($SmashExe)      { $cfg.SmashExe      = $SmashExe }
if ($PollSeconds -gt 0) { $cfg.PollSeconds = $PollSeconds }

function Resolve-ScriptPath([string]$p) {
    $p = [Environment]::ExpandEnvironmentVariables($p)
    if ([System.IO.Path]::IsPathRooted($p)) { return $p }
    return (Join-Path $ScriptDir $p)
}

$PayloadFile  = Resolve-ScriptPath $cfg.PayloadPath
$PinnedSha256 = ([string]$cfg.PayloadSha256).ToUpperInvariant()
$SmashPath    = Resolve-ScriptPath $cfg.SmashExe
$RcmIdPattern = 'USB\VID_0955&PID_7321*'
$ApprovalFile = Join-Path $ScriptDir 'approved.txt'
$LogFile      = Join-Path $ScriptDir 'autoinject.log'

if ($PinnedSha256 -notmatch '^[0-9A-F]{64}$') { throw "Ungueltiger SHA256 in der Konfiguration: $PinnedSha256" }
# -----------------------------------------------------------------------------

function Write-Log([string]$msg) {
    $line = '{0}  {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg
    Write-Host $line
    try {
        Add-Content -Path $LogFile -Value $line -Encoding UTF8
        if ((Get-Item $LogFile).Length -gt 1MB) { Move-Item $LogFile "$LogFile.old" -Force }
    } catch { }
}

function Get-VerifiedPayloadBytes {
    if (-not (Test-Path -LiteralPath $PayloadFile)) { throw "Payload fehlt: $PayloadFile" }
    $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $PayloadFile))
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $hash = ([System.BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-', '')
    if ($hash -ne $PinnedSha256) { throw "SHA256 stimmt NICHT: $hash (erwartet $PinnedSha256) - Injektion verweigert." }
    return ,$bytes
}

function Test-Approved {
    if (-not (Test-Path -LiteralPath $ApprovalFile)) { return $false }
    $content = Get-Content -LiteralPath $ApprovalFile -Raw
    return ($content -match [regex]::Escape($PinnedSha256))
}

function Test-RcmPresent {
    $dev = Get-PnpDevice -PresentOnly -ErrorAction SilentlyContinue |
        Where-Object { $_.InstanceId -like $RcmIdPattern }
    return [bool]$dev
}

function Invoke-Injection {
    $bytes = Get-VerifiedPayloadBytes
    $tmp = Join-Path $env:TEMP ('switchautoinject_{0}.bin' -f [guid]::NewGuid().ToString('N'))
    try {
        [System.IO.File]::WriteAllBytes($tmp, $bytes)
        Write-Log "SHA256 OK, injiziere $(Split-Path $PayloadFile -Leaf) ($($bytes.Length) Bytes) ..."
        $out = & $SmashPath $tmp 2>&1 | Out-String
        $code = $LASTEXITCODE
        $clean = ($out -replace "`0", '' -replace '\s+', ' ').Trim()
        Write-Log "TegraRcmSmash Exit $code : $clean"
        return ($code -eq 0)
    } finally {
        Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
}

# --- Befehle ------------------------------------------------------------------
if ($Revoke) {
    Remove-Item -LiteralPath $ApprovalFile -Force -ErrorAction SilentlyContinue
    Write-Log 'Freigabe zurueckgenommen.'
    return
}
if ($Approve) {
    $null = Get-VerifiedPayloadBytes
    "Freigabe fuer automatische Injektion von $(Split-Path $PayloadFile -Leaf)`r`nSHA256 $PinnedSha256`r`nErteilt am $(Get-Date -Format s)" |
        Set-Content -LiteralPath $ApprovalFile -Encoding UTF8
    Write-Log "Freigabe erteilt (an SHA256 $PinnedSha256 gebunden)."
    return
}

if (-not (Test-Path -LiteralPath $SmashPath)) { throw "TegraRcmSmash nicht gefunden: $SmashPath" }

# nur eine Instanz
$mutex = New-Object System.Threading.Mutex($false, 'Local\SwitchAutoInject')
if (-not $mutex.WaitOne(0)) { Write-Log 'Laeuft bereits, beende.'; return }

try {
    $null = Get-VerifiedPayloadBytes
    Write-Log ("Gestartet. Warte auf Switch im RCM (0955:7321). Modus: {0}" -f $(if ($DryRun) { 'DryRun' } elseif (Test-Approved) { 'aktiv' } else { 'OHNE Freigabe (nur Erkennung)' }))

    $handled = $false   # diese RCM-Verbindung schon behandelt?
    while ($true) {
        $present = Test-RcmPresent
        if (-not $present) {
            if ($handled) { Write-Log 'Switch nicht mehr im RCM, wieder bereit.' }
            $handled = $false
        }
        elseif (-not $handled) {
            Write-Log 'Switch im RCM erkannt.'
            $handled = $true
            if ($DryRun) {
                $null = Get-VerifiedPayloadBytes
                Write-Log 'DryRun: Hash OK, wuerde jetzt injizieren.'
            }
            elseif (-not (Test-Approved)) {
                Write-Log 'Keine Freigabe -> keine Injektion. Freigabe mit: SwitchAutoInject.ps1 -Approve'
            }
            else {
                Start-Sleep -Milliseconds 800   # Treiber kurz settlen lassen
                $ok = $false
                for ($i = 1; $i -le $cfg.MaxTries -and -not $ok; $i++) {
                    try { $ok = Invoke-Injection } catch { Write-Log "Fehler: $($_.Exception.Message)"; break }
                    if (-not $ok) { Start-Sleep -Seconds 2 }
                }
                if ($ok) { Write-Log 'Injektion erfolgreich.' } else { Write-Log 'Injektion fehlgeschlagen. Neuer Versuch erst nach erneutem Einstecken.' }
                if ($Once) { break }
            }
        }
        Start-Sleep -Seconds $cfg.PollSeconds
    }
} finally {
    $mutex.ReleaseMutex()
    $mutex.Dispose()
}
