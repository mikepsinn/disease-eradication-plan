param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$QuartoArgs
)

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

$bookConfig = "_quarto-book.yml"
if (-not (Test-Path $bookConfig)) {
    Write-Error "Missing $bookConfig. Unable to preview book."
    exit 1
}

Copy-Item $bookConfig "_quarto.yml" -Force

Write-Host "Previewing book (_quarto.yml <- $bookConfig)..." -ForegroundColor Cyan
quarto preview @QuartoArgs

