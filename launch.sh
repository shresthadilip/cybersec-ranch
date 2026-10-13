#!/usr/bin/env bash
# ==============================================================================
# CyberSec Ranch - Bash Automation Launcher
# ==============================================================================

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

show_banner() {
    echo -e "${CYAN}"
    echo "==================================================================="
    echo "🤠  CYBERSEC RANCH — CYBERSECURITY TRAINING & CTF LAB SUITE"
    echo "==================================================================="
    echo -e "${NC}"
}

show_usage() {
    show_banner
    echo -e "${YELLOW}Usage: ./launch.sh [PROFILE / ACTION] [OPTIONS]${NC}"
    echo ""
    echo -e "${GREEN}Profiles:${NC}"
    echo "  custom-ctf   : Start all 19 custom CTF challenges & labs (SQLi, SSRF, JWT, SSTI, Cmd, LFI, IDOR, Hash, XXE, NoSQLi, Deserialization, Race Condition, GraphQL, CORS/CSRF, PWN BOF, WebSocket, Recon, PrivEsc)"
    echo "  web-classic  : Start classic PHP/MySQL labs (DVWA, bWAPP, Mutillidae, XVWA)"
    echo "  web-modern   : Start modern web labs (OWASP Juice Shop, WebGoat, WebWolf)"
    echo "  api-graphql  : Start API & GraphQL labs (DVGA, vAPI)"
    echo "  all          : Start ALL training labs and dashboard (high RAM usage)"
    echo "  dashboard    : Start only the central dashboard"
    echo ""
    echo -e "${GREEN}Actions:${NC}"
    echo "  down / stop  : Stop all running containers"
    echo "  logs         : Stream live container logs"
    echo "  status       : View status of containers"
    echo "  clean        : Teardown and delete docker volumes"
    echo ""
}

# Handle flag options (-p / --profile) or positional arguments
if [ "$1" = "-p" ] || [ "$1" = "--profile" ]; then
    PROFILE="${2:-custom-ctf}"
else
    PROFILE="${1:-custom-ctf}"
fi

if [ "$PROFILE" = "--help" ] || [ "$PROFILE" = "-h" ]; then
    show_usage
    exit 0
fi

show_banner

if ! command -v docker &> /dev/null; then
    echo -e "${RED}[-] Docker is not installed or not in PATH.${NC}"
    exit 1
fi

case "$PROFILE" in
    stop|down)
        echo -e "${YELLOW}[*] Stopping all lab containers...${NC}"
        docker compose --profile all down
        ;;
    logs)
        docker compose logs -f
        ;;
    status)
        echo -e "${CYAN}[*] Current Container Status:${NC}"
        docker compose ps
        ;;
    clean)
        echo -e "${YELLOW}[!] Removing containers and volumes...${NC}"
        docker compose --profile all down -v
        ;;
    *)
        echo -e "${CYAN}[+] Launching Profile: '$PROFILE'...${NC}"
        docker compose --profile "$PROFILE" up -d
        echo ""
        echo -e "${GREEN}[✓] Training environment is active!${NC}"
        echo -e " 👉 Access Dashboard at: ${CYAN}http://localhost:8000${NC}"
        echo ""
        docker compose ps
        ;;
esac
