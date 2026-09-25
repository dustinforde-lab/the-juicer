# Cloudflare Tunnel Launcher for The Juicer (Off-Network Mobile Access)
param(
    [int]$Port = 8501
)

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "🌐 [THE JUICER] Launching Secure Mobile Tunnel..." -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Check if cloudflared is installed
if (!(Get-Command "cloudflared" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: 'cloudflared' is not installed or not in PATH." -ForegroundColor Red
    Write-Host "💡 Install via winget: winget install Cloudflare.CloudflareTunnel" -ForegroundColor Yellow
    exit
}

Write-Host "🔗 Establishing secure outbound connection to Cloudflare edge..." -ForegroundColor Green
Write-Host "📱 Open the generated HTTPS URL on your phone's browser away from home!" -ForegroundColor Yellow
Write-Host "=========================================================" -ForegroundColor Cyan

cloudflared tunnel --url http://localhost:$Port
