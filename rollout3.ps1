    # Install Git and update Scoop buckets
    scoop install git
    scoop update
    scoop bucket add versions
    scoop bucket add extras
    scoop install versions/windows-terminal-preview
    scoop install versions/vscode-insiders
    # scoop install main/winpython  # un-comment if you prefer over micromamba


    # Set desktop target and PATH additions (using Environment Variables)
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User") # Get existing User PATH
    $desktop = "C:\Users\WDAGUtilityAccount\Desktop"
    $env:PATH += ";$desktop\micromamba;$desktop\Scoop\bin"
    $env:PATH += ";$desktopPath\micromamba;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")

    # Download Micromamba
    Invoke-WebRequest -Uri "https://micro.mamba.pm/api/micromamba/win-64" -OutFile "$desktop\micromamba-installer.exe"
    if (-not (Test-Path "$desktop\micromamba-installer.exe")) {
        Write-Error "Failed to download Micromamba installer."
        Exit # Or stop the script if download is critical 
    }

    # Install Micromamba
    Start-Process -FilePath "$desktop\micromamba-installer.exe" -ArgumentList "/S /D=$desktop\micromamba" -Wait

    # Launch common applications
    Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    Start-Process "notepad.exe"
    Start-Process "explorer.exe"

    # Invoke post.ps1 for further setup
    Invoke-Expression -Command "$desktop\dev\post.ps1" 
        