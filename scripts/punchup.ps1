# Punch-up pass via Claude Opus 4.6 with ZERO Claude Code harness context.
# Bills the Claude subscription (headless claude -p), not API credits.
#
# Usage:
#   ./scripts/punchup.ps1 -File knowledge/proof/wishonias-wager.qmd
#   ./scripts/punchup.ps1 -File knowledge/appendix/joke.qmd -Instruction "Punch up only the section 'The shirt'"
#   ./scripts/punchup.ps1 -File x.qmd -Model claude-opus-4-8   # compare models on the same passage
param(
    [Parameter(Mandatory = $true)] [string]$File,
    [string]$Instruction = "Run the Punch-Up Pass on this passage. Suggest only changes that make it funnier or stronger under the style guide. Tie goes to the incumbent: if a line is already as good as it gets, leave it alone.",
    [string]$Model = "claude-opus-4-6"
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent

$styleGuide = Get-Content (Join-Path $root "GUIDES\STYLE_GUIDE.md") -Raw

$preamble = @"
You are the punch-up writer for the book "How to End War and Disease" (the Earth Optimization Services manual). The style guide below is binding law: the Voice Map, the comedy mechanics and kill-tests, giving-never-asking, ownership-not-admission, the monorail pitchman for in-world artifacts, dead-straight formality on the commission and certificates, no em-dashes anywhere, and shorter is funnier.

Output format: a numbered list of suggestions, each exactly:
BEFORE: <the exact current text>
AFTER: <your version>
WHY: <one line>

Rules: never rewrite the whole passage; pick the lines that matter most (hooks, openers, closers). Keep Quarto syntax ({{< var ... >}}, [@citations], [links](.qmd)) byte-identical inside your AFTER text. Never invent or hardcode a number: every numeric value comes from an existing {{< var ... >}} parameter or stays out of the line. If nothing should change, say so in one line. Do not explain the style guide back; just apply it.
"@

$systemPrompt = $preamble + "`n`n---`n`nSTYLE GUIDE (binding):`n`n" + $styleGuide

$passagePath = if ([System.IO.Path]::IsPathRooted($File)) { $File } else { Join-Path $root $File }
$passage = Get-Content $passagePath -Raw

$tmp = New-TemporaryFile
Set-Content $tmp $systemPrompt -Encoding utf8

$prompt = "$Instruction`n`n<passage path=`"$File`">`n$passage`n</passage>"

try {
    $prompt | claude -p --model $Model --system-prompt-file $tmp --tools ""
}
finally {
    Remove-Item $tmp -Force
}
