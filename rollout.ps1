    # Install Git and update Scoop buckets
    scoop install git
    scoop update
    scoop bucket add versions
    scoop bucket add extras
    scoop install versions/windows-terminal-preview
    scoop install main/gh
    # scoop install main/winpython  # un-comment if you prefer over micromamba


    # Set desktop target and PATH additions (using Environment Variables)
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "User") # Get existing User PATH
    $desktop = "C:\Users\WDAGUtilityAccount\Desktop"
    $env:PATH += ";$desktop\micromamba;$desktop\Scoop\bin"
    
    # Define the RunCommand function
    function RunCommand($command) {
        Write-Host "Running command: $command"
        Invoke-Expression $command
    }

    # Install required packages
    RunCommand "scoop install extras/okular"
    RunCommand "scoop install extras/irfanview-lean"
    RunCommand "scoop install extras/mpc-hc-fork"
    RunCommand "scoop install main/sourcegraph-cli"
    RunCommand "scoop install main/frp"
    RunCommand "scoop install main/gnutls"
    RunCommand "scoop install extras/carapace-bin"
    RunCommand "scoop install versions/vscode-insiders"
    RunCommand "scoop install main/yq"
    RunCommand "scoop install main/jc"
    RunCommand "scoop install extras/vscode"
    RunCommand "scoop install main/eza"
    RunCommand "scoop install extras/chatall"
    RunCommand "scoop install main/fq"
    RunCommand "scoop install main/nu"
    RunCommand "scoop install extras/texteditorpro"
    RunCommand "scoop install extras/ghidra"
    RunCommand "scoop install main/miller"
    RunCommand "scoop install main/selenium"
    RunCommand "scoop install extras/mambaforge"
    RunCommand "scoop install main/gcc"
    RunCommand "scoop install main/clink"
    RunCommand "scoop install main/clink-flex-prompt"
    RunCommand "scoop install extras/x64dbg"
    RunCommand "scoop bucket add nerd-fonts"
    RunCommand "scoop install nerd-fonts/FiraMono-NF-Mono"
    RunCommand "scoop install nerd-fonts/FiraCode-NF"
    RunCommand "scoop install versions/googlechrome-canary"
        
    $env:PATH += ";$desktopPath\micromamba;C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Scoop\bin"
    [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")

    # Launch common applications
    Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    Start-Process "notepad.exe"
    Start-Process "explorer.exe"
    try {
        Start-Process "wt.exe" -Wait
    } catch {
        Start-Process "powershell.exe" 
    }