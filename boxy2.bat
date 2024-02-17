:: This batch file sets up the environment for the sandbox init process
:: It adds Scoop to the PATH and launches the rollout script.

REM Add Scoop to PATH for this session 
setx PATH "%PATH%;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin"

REM Execute the rollout script in PowerShell
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\WDAGUtilityAccount\Desktop\rollout2.ps1" 
