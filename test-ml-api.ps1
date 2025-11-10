# Test ML API Endpoints

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing ML API Integration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$baseUrl = "http://localhost:4000/api/ml"

# Test 1: Health Check
Write-Host "`n[Test 1] ML Service Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "✅ Health Check Passed" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "❌ Health Check Failed: $_" -ForegroundColor Red
}

# Test 2: Single Price Prediction
Write-Host "`n[Test 2] Single Price Prediction..." -ForegroundColor Yellow
try {
    $body = @{
        airline = "IndiGo"
        origin = "Delhi"
        destination = "Mumbai"
        days_until_flight = 7
        stops = 0
        departure_hour = 10
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/predict" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Prediction Successful" -ForegroundColor Green
    $response | ConvertTo-Json
} catch {
    Write-Host "❌ Prediction Failed: $_" -ForegroundColor Red
}

# Test 3: Multiple Dates Prediction (30 days)
Write-Host "`n[Test 3] 30-Day Price Forecast..." -ForegroundColor Yellow
try {
    $body = @{
        airline = "IndiGo"
        origin = "Delhi"
        destination = "Mumbai"
        days_ahead = 30
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/predict/multiple" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Forecast Successful" -ForegroundColor Green
    Write-Host "Predictions for next 30 days:" -ForegroundColor White
    $response.data.predictions | Select-Object -First 5 | Format-Table -AutoSize
    Write-Host "Cheapest day: $($response.data.cheapest_day.day) at ₹$($response.data.cheapest_day.price)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Forecast Failed: $_" -ForegroundColor Red
}

# Test 4: Booking Recommendation
Write-Host "`n[Test 4] Booking Recommendation..." -ForegroundColor Yellow
try {
    $body = @{
        current_price = 5500
        airline = "IndiGo"
        origin = "Delhi"
        destination = "Mumbai"
        days_until_flight = 7
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$baseUrl/recommend" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Recommendation Generated" -ForegroundColor Green
    Write-Host "Recommendation: $($response.data.recommendation)" -ForegroundColor Cyan
    Write-Host "Action: $($response.data.action)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Recommendation Failed: $_" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Testing Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
