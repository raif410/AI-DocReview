# Simple server check script
Write-Host "Checking server status..."
Start-Sleep -Seconds 2

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    Write-Host ""
    Write-Host "========================================"
    Write-Host "  SUCCESS! SERVER IS RUNNING!"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "API: http://localhost:8000"
    Write-Host "Docs: http://localhost:8000/docs"
    Write-Host "Health: $($response.Content)"
    Write-Host ""
} catch {
    Write-Host "Server is starting or not ready yet."
    Write-Host "Try opening http://localhost:8000/docs in your browser"
}

