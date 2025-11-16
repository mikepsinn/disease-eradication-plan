param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$QuartoArgs
)

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

$econConfig = "_quarto-economics.yml"
if (-not (Test-Path $econConfig)) {
    Write-Error "Missing $econConfig. Unable to render economics website."
    exit 1
}

Copy-Item $econConfig "_quarto.yml" -Force

Write-Host "Rendering economics site (_quarto.yml <- $econConfig)..." -ForegroundColor Cyan
quarto render @QuartoArgs

