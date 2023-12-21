#! /bin/bash
# /Users/tp | RENAME the cfg.wsb file |

# Set the execution policy for the current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# Download and execute the Scoop installation script
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
