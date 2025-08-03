# Check if git is installed and available
Write-Output "Checking for git installation..."

try {
    $gitVersion = git --version
    Write-Output "Git is installed: $gitVersion"
    
    # Check if we're in a git repository and show status
    Write-Output "Checking git repository status..."

    try {
        # Check if we're in a git repository
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($gitRoot) {
            Write-Output "Current directory is a git repository"
            Write-Output "Repository root: $gitRoot"
            
            # Show git status
            Write-Output "\nGit status:"
            git status --porcelain
            
            # Show current branch
            Write-Output "\nCurrent branch:"
            git branch --show-current
            
            # Show recent commits
            Write-Output "\nRecent commits:"
            git log --oneline -5
            
            # Show if there are any uncommitted changes
            $status = git status --porcelain
            if ($status) {
                Write-Output "\nUncommitted changes detected:"
                Write-Output $status
            } else {
                Write-Output "\nNo uncommitted changes"
            }
        } else {
            Write-Output "Current directory is NOT a git repository"
        }
    } catch {
        Write-Output "Error checking git repository status: $_"
    }
} catch {
    Write-Output "Git is not installed or not in PATH"
    Write-Output "Error: $_"
}
