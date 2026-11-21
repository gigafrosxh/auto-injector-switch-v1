# Entfernt den Autostart und beendet den laufenden Waechter.
Stop-ScheduledTask -TaskName 'SwitchAutoInject' -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName 'SwitchAutoInject' -Confirm:$false -ErrorAction SilentlyContinue
Write-Host 'Autostart entfernt.'
