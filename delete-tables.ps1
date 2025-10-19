$headers = @{
    'Authorization' = 'Bearer patAQEwwKXChpQBnL.d9ca339d66431e6cfece5a3fe1c1d69c6c36848386804a3b1bc773dfedcde127'
}

$tables = @(
    'tblPDuov84u0ipfl2',
    'tblQWoSMsHiOXnqIn',
    'tbldUBwpWXdoYwqaE',
    'tblCzRgzOiKDwcEF9',
    'tbl1wk2OoiUYxrXQs',
    'tbliWNzfCiSvqnLFr'
)

foreach ($tableId in $tables) {
    try {
        $uri = "https://api.airtable.com/v0/meta/bases/appRA45hnZpiTyRjB/tables/$tableId"
        $response = Invoke-WebRequest -Uri $uri -Method DELETE -Headers $headers -UseBasicParsing
        Write-Host "Deleted table $tableId" -ForegroundColor Green
    } catch {
        Write-Host "Error deleting table ${tableId}: $_" -ForegroundColor Red
    }
}

Write-Host "Table deletion complete!" -ForegroundColor Cyan
