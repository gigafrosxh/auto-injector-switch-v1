# Richtet SwitchAutoInject als Aufgabe bei Benutzeranmeldung ein (unsichtbar, ohne Adminrechte).
# Entfernen: .\uninstall-autostart.ps1
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'SwitchAutoInject.ps1'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' `
    -Argument "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$script`""
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName 'SwitchAutoInject' -Action $action -Trigger $trigger -Settings $settings `
    -Description 'Injiziert verifiziertes Payload (Hekate) automatisch bei Switch im RCM' -Force | Out-Null
Start-ScheduledTask -TaskName 'SwitchAutoInject'
Write-Host 'Autostart eingerichtet und gestartet. Log: autoinject.log im Skriptordner'
