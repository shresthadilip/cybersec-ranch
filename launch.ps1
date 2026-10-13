# PowerShell Launcher for CyberSec Ranch Training Lab Suite
param (
    [Parameter(Position = 0)]
    [ValidateSet("all", "custom-ctf", "web-classic", "web-modern", "api-graphql", "core", "dashboard", "stop", "down", "logs", "status", "clean")]
    [string]$Action = "custom-ctf",

    [Parameter()]
    [switch]$Build,

    [Parameter()]
    [switch]$Help
)

function Show-Banner {
    Write-Host ""
    Write-Host " ===================================================================" -ForegroundColor Cyan
    Write-Host " 🤠  CYBERSEC RANCH — CYBERSECURITY TRAINING & CTF LAB SUITE" -ForegroundColor White
    Write-Host " ===================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Usage {
    Show-Banner
    Write-Host "Usage: .\launch.ps1 [Profile | Action] [Options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Profiles:" -ForegroundColor Green
    Write-Host "  custom-ctf    : Start all 19 custom CTF challenges & labs (SQLi, SSRF, JWT, SSTI, Cmd, LFI, IDOR, Hash, XXE, NoSQLi, Deserialization, Race Condition, GraphQL, CORS/CSRF, PWN BOF, WebSocket, Recon, PrivEsc)"
    Write-Host "  web-classic   : Start classic PHP/MySQL labs (DVWA, bWAPP, Mutillidae II, XVWA)"
    Write-Host "  web-modern    : Start modern web labs (OWASP Juice Shop, OWASP WebGoat/WebWolf)"
    Write-Host "  api-graphql   : Start API labs (DVGA GraphQL, vAPI)"
    Write-Host "  all           : Start ALL training labs and dashboard (high RAM usage)"
    Write-Host "  dashboard     : Start only the central training dashboard"
    Write-Host ""
    Write-Host "Actions:" -ForegroundColor Green
    Write-Host "  stop / down   : Stop and teardown running lab containers"
    Write-Host "  logs          : Stream container logs"
    Write-Host "  status        : Check status of all containers"
    Write-Host "  clean         : Prune unused containers and ctf volumes"
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  -Build        : Force rebuild of custom docker images"
    Write-Host "  -Help         : Show this help message"
    Write-Host ""
}

if ($Help) {
    Show-Usage
    exit 0
}

Show-Banner

# Check if Docker is available
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "[-] Docker is not detected in PATH. Please install Docker Desktop or run Docker daemon." -ForegroundColor Red
    exit 1
}

$BuildFlag = if ($Build) { "--build" } else { "" }

switch ($Action) {
    "stop" {
        Write-Host "[*] Stopping all CTF training lab containers..." -ForegroundColor Yellow
        docker compose --profile all down
    }
    "down" {
        Write-Host "[*] Stopping and removing all containers & networks..." -ForegroundColor Yellow
        docker compose --profile all down
    }
    "logs" {
        docker compose logs -f
    }
    "status" {
        Write-Host "[*] Current Container Status:" -ForegroundColor Cyan
        docker compose ps
    }
    "clean" {
        Write-Host "[!] Cleaning up stopped containers and unused volumes..." -ForegroundColor Yellow
        docker compose --profile all down -v
    }
    Default {
        Write-Host "[+] Launching Profile: '$Action'..." -ForegroundColor Cyan
        docker compose --profile $Action up -d $BuildFlag
        Write-Host ""
        Write-Host "[✓] Environment is starting up!" -ForegroundColor Green
        Write-Host " 👉 Open Training Dashboard: http://localhost:8000" -ForegroundColor White
        Write-Host ""
        Write-Host "[*] Checking running containers:" -ForegroundColor Cyan
        docker compose ps
    }
}
