# This script calculates the total word count of all .qmd files listed in _quarto.yml
# and estimates the total page count of the book.

$totalWords = 0
$files = Get-Content -Path '_quarto.yml' | Select-String -Pattern '([\w\/\.-]+\.qmd)' | ForEach-Object { $_.Matches.Groups[1].Value }

foreach ($file in $files) {
    if (Test-Path $file) {
        try {
            $content = Get-Content -Path $file -Raw
            # Remove YAML frontmatter and code chunks to get a more accurate word count of the prose
            $prose = $content -replace '---[\s\S]*?---', '' -replace '```{.*?}[\s\S]*?```', ''
            $wordCount = ($prose | Measure-Object -Word).Words
            $totalWords += $wordCount
        } catch {
            Write-Host "Could not process file: $file"
        }
    } else {
        Write-Host "File not found: $file"
    }
}

$estimatedPages = [math]::Ceiling($totalWords / 275)

Write-Host "Total word count (prose only): $totalWords"
Write-Host "Estimated page count (at 275 words/page): $estimatedPages"
