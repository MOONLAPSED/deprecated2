setx PATH "%PATH%;C:\Users\<your_username>\AppData\Local\Programs\Scoop\bin"
# Ensure Elevated Permissions (Administrator)
if (-Not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {    
    Write-Warning "This script requires elevated permissions. Please re-run as administrator."
    Start-Process powershell.exe -Verb RunAs -ArgumentList "-File `"$PSCommandPath`""
    Exit 
} 
