# Start All Services for Flight Fare Prediction

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Flight Fare Prediction - Services" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$projectRoot = "c:\Users\hp\Desktop\flight_fare_prediction"

# Kill any existing processes on ports 4000 and 5001
Write-Host "Checking for existing services..." -ForegroundColor Yellow
Get-NetTCPConnection -LocalPort 4000 -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    Write-Host "  Stopped process on port 4000" -ForegroundColor Gray
}
Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    Write-Host "  Stopped process on port 5001" -ForegroundColor Gray
}

Start-Sleep -Seconds 1

# Start ML Service (Flask - Port 5001)
Write-Host "`n[1/2] Starting Flask ML Service..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; python backend\ml_service.py"
Write-Host "  ✓ ML Service started in new window" -ForegroundColor Green

Start-Sleep -Seconds 4

# Start Node.js Backend (Port 4000)
Write-Host "`n[2/2] Starting Node.js Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; npm start"
Write-Host "  ✓ Backend service started in new window" -ForegroundColor Green

Start-Sleep -Seconds 4

# Check if services are running
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Service Status Check" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$mlRunning = Get-NetTCPConnection -LocalPort 5001 -ErrorAction SilentlyContinue
$nodeRunning = Get-NetTCPConnection -LocalPort 4000 -ErrorAction SilentlyContinue

if ($mlRunning) {
    Write-Host "✅ Flask ML Service (Port 5001): RUNNING" -ForegroundColor Green
} else {
    Write-Host "❌ Flask ML Service (Port 5001): NOT RUNNING" -ForegroundColor Red
}

if ($nodeRunning) {
    Write-Host "✅ Node.js Backend (Port 4000): RUNNING" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js Backend (Port 4000): NOT RUNNING" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Available Endpoints" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "Backend API:" -ForegroundColor White
Write-Host "  http://localhost:4000/api/flights" -ForegroundColor Gray
Write-Host "  http://localhost:4000/api/ml/health" -ForegroundColor Gray
Write-Host "  http://localhost:4000/api/ml/predict" -ForegroundColor Gray
Write-Host "`nML Service:" -ForegroundColor White
Write-Host "  http://localhost:5001/health" -ForegroundColor Gray
Write-Host "  http://localhost:5001/predict" -ForegroundColor Gray

Write-Host "`n========================================`n" -ForegroundColor Cyan
Write-Host "Services are running in separate PowerShell windows." -ForegroundColor Yellow
Write-Host "Close those windows to stop the services.`n" -ForegroundColor Yellow
