#!/usr/bin/env pwsh
# GitHub Artifacts Cleanup Script
# 
# This script analyzes and cleans up GitHub Actions artifacts to reduce storage costs.
# 
# Usage:
#   .\scripts\cleanup-github-artifacts.ps1 -DryRun          # Show what would be deleted
#   .\scripts\cleanup-github-artifacts.ps1 -KeepLast 5      # Keep only last 5 of each type
#   .\scripts\cleanup-github-artifacts.ps1 -DeleteAll       # Delete ALL artifacts (dangerous!)

param(
    [switch]$DryRun = $false,
    [int]$KeepLast = 3,  # Keep last N artifacts of each type
    [switch]$DeleteAll = $false,
    [switch]$DeleteExpired = $false,  # Only delete expired artifacts
    [switch]$Force = $false  # Skip confirmation prompt
)

$ErrorActionPreference = "Stop"

Write-Host "=== GitHub Artifacts Cleanup Tool ===" -ForegroundColor Cyan
Write-Host ""

# Get repository info
$repoInfo = git remote get-url origin
if ($repoInfo -match "github\.com[:/]([^/]+)/([^/\.]+)") {
    $owner = $matches[1]
    $repo = $matches[2]
    Write-Host "Repository: $owner/$repo" -ForegroundColor Green
} else {
    Write-Error "Could not determine repository from git remote"
    exit 1
}

# Fetch all runs
Write-Host "`nFetching workflow runs..." -ForegroundColor Yellow
$runs = gh run list --limit 300 --json databaseId,conclusion,createdAt | ConvertFrom-Json
Write-Host "Found $($runs.Count) workflow runs" -ForegroundColor Green

# Collect all artifacts
Write-Host "`nAnalyzing artifacts..." -ForegroundColor Yellow
$allArtifacts = @()
$totalActive = 0
$totalExpired = 0
$activeCount = 0
$expiredCount = 0

foreach ($run in $runs) {
    try {
        $response = gh api /repos/$owner/$repo/actions/runs/$($run.databaseId)/artifacts 2>$null | ConvertFrom-Json
        foreach ($art in $response.artifacts) {
            $obj = [PSCustomObject]@{
                Id = $art.id
                RunId = $run.databaseId
                Name = $art.name
                SizeBytes = $art.size_in_bytes
                SizeMB = [math]::Round($art.size_in_bytes/1MB, 2)
                Expired = $art.expired
                Created = $run.createdAt
            }
            $allArtifacts += $obj
            
            if ($art.expired) {
                $totalExpired += $art.size_in_bytes
                $expiredCount++
            } else {
                $totalActive += $art.size_in_bytes
                $activeCount++
            }
        }
    } catch {
        # Silently skip runs with no artifacts or errors
    }
}

Write-Host "`n=== CURRENT STORAGE USAGE ===" -ForegroundColor Cyan
Write-Host "Active artifacts:  $activeCount (Total: $([math]::Round($totalActive/1GB, 2)) GB)" -ForegroundColor Green
Write-Host "Expired artifacts: $expiredCount (Total: $([math]::Round($totalExpired/1GB, 2)) GB)" -ForegroundColor Yellow
Write-Host "Grand total:       $($activeCount + $expiredCount) artifacts ($([math]::Round(($totalActive + $totalExpired)/1GB, 2)) GB)" -ForegroundColor White

# Breakdown by type
Write-Host "`n=== BREAKDOWN BY ARTIFACT TYPE ===" -ForegroundColor Cyan
$allArtifacts | Where-Object { -not $_.Expired } | Group-Object Name | Sort-Object Count -Descending | ForEach-Object {
    $totalGB = [math]::Round(($_.Group | Measure-Object -Property SizeMB -Sum).Sum/1024, 2)
    Write-Host "  $($_.Name): $($_.Count) artifacts ($totalGB GB)" -ForegroundColor White
}

# Determine what to delete
$toDelete = @()

if ($DeleteAll) {
    Write-Host "`n[WARNING] DeleteAll mode - will delete ALL artifacts!" -ForegroundColor Red
    $toDelete = $allArtifacts | Where-Object { -not $_.Expired }
} elseif ($DeleteExpired) {
    Write-Host "`n[INFO] DeleteExpired mode - will delete expired artifacts only" -ForegroundColor Yellow
    $toDelete = $allArtifacts | Where-Object { $_.Expired }
} else {
    Write-Host "`n[INFO] KeepLast mode - will keep last $KeepLast of each artifact type" -ForegroundColor Yellow
    
    # Group by artifact name and keep only the last N of each
    $grouped = $allArtifacts | Where-Object { -not $_.Expired } | Group-Object Name
    
    foreach ($group in $grouped) {
        $sorted = $group.Group | Sort-Object Created -Descending
        $toKeep = $sorted | Select-Object -First $KeepLast
        $toDeleteFromGroup = $sorted | Select-Object -Skip $KeepLast
        
        if ($toDeleteFromGroup) {
            $toDelete += $toDeleteFromGroup
            Write-Host "  $($group.Name): Keeping $($toKeep.Count), deleting $($toDeleteFromGroup.Count)" -ForegroundColor White
        } else {
            Write-Host "  $($group.Name): Keeping all $($toKeep.Count) (under threshold)" -ForegroundColor Green
        }
    }
}

if ($toDelete.Count -eq 0) {
    Write-Host "`n[SUCCESS] No artifacts to delete!" -ForegroundColor Green
    exit 0
}

# Calculate savings
$savingsBytes = ($toDelete | Measure-Object -Property SizeBytes -Sum).Sum
$savingsGB = [math]::Round($savingsBytes/1GB, 2)

Write-Host "`n=== DELETION PLAN ===" -ForegroundColor Cyan
Write-Host "Artifacts to delete: $($toDelete.Count)" -ForegroundColor Yellow
Write-Host "Storage to reclaim: $savingsGB GB" -ForegroundColor Yellow

if ($DryRun) {
    Write-Host "`n[DRY RUN] Would delete the following artifacts:" -ForegroundColor Magenta
    $toDelete | Sort-Object Created -Descending | Select-Object -First 20 Name, SizeMB, @{Name="Created";Expression={$_.Created.ToString('yyyy-MM-dd HH:mm')}} | Format-Table -AutoSize
    
    if ($toDelete.Count -gt 20) {
        Write-Host "... and $($toDelete.Count - 20) more" -ForegroundColor Gray
    }
    
    Write-Host "`n[DRY RUN] No artifacts were deleted. Run without -DryRun to actually delete." -ForegroundColor Magenta
    exit 0
}

# Confirm deletion
if (-not $Force) {
    Write-Host "`n[WARNING] This will permanently delete $($toDelete.Count) artifacts ($savingsGB GB)" -ForegroundColor Red
    $confirmation = Read-Host "Type 'DELETE' to confirm"

    if ($confirmation -ne "DELETE") {
        Write-Host "`n[CANCELLED] No artifacts were deleted." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "`n[FORCE MODE] Skipping confirmation, deleting $($toDelete.Count) artifacts..." -ForegroundColor Yellow
}

# Perform deletion
Write-Host "`nDeleting artifacts..." -ForegroundColor Yellow
$deleted = 0
$failed = 0

foreach ($artifact in $toDelete) {
    try {
        gh api --method DELETE /repos/$owner/$repo/actions/artifacts/$($artifact.Id) 2>&1 | Out-Null
        $deleted++
        Write-Host "  [OK] Deleted: $($artifact.Name) ($($artifact.SizeMB) MB, created $($artifact.Created.ToString('yyyy-MM-dd')))" -ForegroundColor Green
    } catch {
        $failed++
        Write-Host "  [FAIL] Could not delete artifact $($artifact.Id): $_" -ForegroundColor Red
    }
}

Write-Host "`n=== CLEANUP COMPLETE ===" -ForegroundColor Cyan
Write-Host "Successfully deleted: $deleted artifacts" -ForegroundColor Green
Write-Host "Failed: $failed artifacts" -ForegroundColor $(if ($failed -gt 0) { "Red" } else { "Green" })
Write-Host "Storage reclaimed: ~$savingsGB GB" -ForegroundColor Green

