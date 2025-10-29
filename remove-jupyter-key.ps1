Get-ChildItem -Path . -Filter *.qmd -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName
    $newContent = $content | Where-Object { $_ -notmatch "^\s*jupyter:\s*dih-project-kernel\s*$" }
    Set-Content -Path $_.FullName -Value $newContent
}
Write-Output "Removed 'jupyter: dih-project-kernel' from all .qmd files."
