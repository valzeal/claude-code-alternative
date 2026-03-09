#!/bin/bash
# Zeal Code - Autonomous Deployment Script
# This script deploys Zeal Code to your VPS
# Usage: ./deploy-to-vps.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Configuration
PROJECT_DIR="/opt/zeal-code"
REPO_URL="https://github.com/valzeal/claude-code-alternative.git"
API_DOMAIN="api.zealhaven.net"
UI_DOMAIN="app.zealhaven.net"
USER="ridzeal"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    log_warn "Running as root. Some commands will use sudo where needed."
fi

# Step 1: Update system
log_step "Updating system packages"
sudo apt-get update && sudo apt-get upgrade -y

# Step 2: Install Docker
log_step "Installing Docker"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    log_info "Docker installed successfully"
else
    log_info "Docker already installed"
fi

# Step 3: Install Docker Compose
log_step "Installing Docker Compose"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    log_info "Docker Compose installed successfully"
else
    log_info "Docker Compose already installed"
fi

# Step 4: Create project directory
log_step "Setting up project directory"
sudo mkdir -p $PROJECT_DIR
sudo chown -R $USER:$USER $PROJECT_DIR

# Step 5: Clone repository
log_step "Cloning repository"
if [ -d "$PROJECT_DIR/claude-code-alternative" ]; then
    cd $PROJECT_DIR/claude-code-alternative
    git pull origin main
    log_info "Repository updated"
else
    git clone $REPO_URL $PROJECT_DIR/claude-code-alternative
    cd $PROJECT_DIR/claude-code-alternative
    log_info "Repository cloned"
fi

# Step 6: Build Docker images
log_step "Building Docker images"
cd $PROJECT_DIR/claude-code-alternative
docker-compose build

# Step 7: Stop old containers (if any)
log_step "Stopping old containers"
docker-compose down 2>/dev/null || true

# Step 8: Start new containers
log_step "Starting containers"
docker-compose up -d

# Step 9: Wait for services to be healthy
log_step "Waiting for services to be healthy"
sleep 30

# Step 10: Configure Nginx
log_step "Configuring Nginx"

# Copy Nginx configurations
sudo cp $PROJECT_DIR/claude-code-alternative/nginx/zeal-code-api.conf /etc/nginx/sites-available/
sudo cp $PROJECT_DIR/claude-code-alternative/nginx/zeal-code-ui.conf /etc/nginx/sites-available/

# Enable sites
sudo ln -sf /etc/nginx/sites-available/zeal-code-api.conf /etc/nginx/sites-enabled/
sudo ln -sf /etc/nginx/sites-available/zeal-code-ui.conf /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

log_info "Nginx configured and reloaded"

# Step 11: Verify deployment
log_step "Verifying deployment"

# Check API health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    log_info "✅ API is running"
else
    log_error "❌ API health check failed"
fi

# Check UI health
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    log_info "✅ UI is running"
else
    log_error "❌ UI health check failed"
fi

# Step 12: Display status
log_step "Deployment Status"
echo ""
docker-compose ps
echo ""

# Step 13: Show logs
log_step "Recent logs"
echo "=== API Logs ==="
docker logs zeal-code-api --tail 20
echo ""
echo "=== UI Logs ==="
docker logs zeal-code-ui --tail 20

# Step 14: Cleanup
log_step "Cleaning up old Docker images"
docker image prune -f

log_info "Deployment completed successfully!"
echo ""
echo "🎉 Zeal Code is now deployed!"
echo ""
echo "Services:"
echo "  - API: http://$API_DOMAIN"
echo "  - UI:  http://$UI_DOMAIN"
echo ""
echo "Next steps:"
echo "  1. Configure DNS records:"
echo "     - api.zealhaven.net → 103.150.101.223"
echo "     - app.zealhaven.net → 103.150.101.223"
echo "  2. Set up SSL certificates:"
echo "     sudo certbot --nginx -d $API_DOMAIN -d $UI_DOMAIN"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To restart services:"
echo "  docker-compose restart"
echo ""
