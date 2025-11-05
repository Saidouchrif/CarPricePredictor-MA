# Script de démarrage du monitoring

Write-Host "=== Démarrage du Monitoring ===" -ForegroundColor Cyan
Write-Host ""

# Démarrer les services
Write-Host "▶️  Démarrage de Redis, Prometheus, Grafana..." -ForegroundColor Yellow
docker-compose -f docker-compose.monitoring.yml up -d

Write-Host ""
Write-Host "⏳ Attente du démarrage des services..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "✅ Services démarrés!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Accès aux services:" -ForegroundColor Cyan
Write-Host "  Prometheus: http://localhost:9090" -ForegroundColor White
Write-Host "  Grafana:    http://localhost:3000 (admin/admin123)" -ForegroundColor White
Write-Host "  Redis:      localhost:6379" -ForegroundColor White
Write-Host ""

$open = Read-Host "Ouvrir Grafana dans le navigateur? (o/N)"
if ($open -eq "o" -or $open -eq "O") {
    Start-Process "http://localhost:3000"
}
