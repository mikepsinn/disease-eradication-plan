$start_time = Get-Date
quarto render
$end_time = Get-Date
$duration = $end_time - $start_time
Write-Output "Quarto render took: $($duration.TotalSeconds) seconds"
