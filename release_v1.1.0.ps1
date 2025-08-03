# Release v1.1.0 to GitHub
Write-Output "==============================================="
Write-Output "      InquiryCircle v1.1.0 Release Script"
Write-Output "==============================================="

Set-Location -Path "C:\Users\scott\CascadeProjects\InquiryCircle"

Write-Output "1. Checking git status..."
Write-Output "=========================="
.\check_git_status.ps1

Write-Output "\n2. Adding and committing changes..."
Write-Output "=================================="
git add .
git commit -m "Release v1.1.0 - CircleMessage1 Feature"

Write-Output "\n3. Pushing to GitHub..."
Write-Output "======================"
git push origin main

Write-Output "\n4. Tagging release..."
Write-Output "===================="
.\tag_release.ps1

Write-Output "\n5. Pushing tags to GitHub..."
Write-Output "==========================="
git push --tags

Write-Output "\n==============================================="
Write-Output "      InquiryCircle v1.1.0 Release Complete!"
Write-Output "==============================================="
Write-Output "\nRelease v1.1.0 has been successfully pushed to GitHub with tag."

# Pause to keep window open
Read-Host -Prompt "\nPress Enter to exit"
