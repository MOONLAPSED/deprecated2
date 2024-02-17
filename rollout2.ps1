# Run a command
function RunCommand($command) {
    Write-Host "Running command: $command"
    Invoke-Expression $command
}

# Run the commands
RunCommand("scoop install main/yq")
RunCommand("scoop install main/jc")
RunCommand("scoop install extras/vscode")
RunCommand("scoop install main/eza")
RunCommand("scoop install extras/chatall")
RunCommand("scoop install extras/scrawler")
RunCommand("scoop install main/fq")
RunCommand("scoop install main/nu")
RunCommand("scoop install extras/texteditorpro")
RunCommand("scoop install extras/ghidra")
RunCommand("scoop install main/miller")
RunCommand("scoop install main/selenium")
RunCommand("scoop install extras/mambaforge")
RunCommand("scoop install main/gcc")
RunCommand("scoop install main/clink")
RunCommand("scoop install main/clink-flex-prompt")
RunCommand("scoop install extras/x64dbg")
RunCommand("scoop bucket add nerd-fonts")
RunCommand("scoop install nerd-fonts/FiraMono-NF-Mono")
RunCommand("scoop install nerd-fonts/FiraCode-NF")
RunCommand("scoop install versions/googlechrome-canary")
