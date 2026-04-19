#!/bin/bash

# QuickDelivery - Docker Environment Setup Script
# This script initializes the Docker environment for development

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "QuickDelivery - Docker Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi
echo "✓ Docker found"

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi
echo "✓ Docker Compose found"

# Create necessary directories
echo ""
echo "Creating project directories..."
mkdir -p "$PROJECT_ROOT/backups"
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/database/init"
mkdir -p "$PROJECT_ROOT/docker/nginx/ssl"

# Create .env if it doesn't exist
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo "✓ .env file created"
    echo "⚠️  Please review and customize .env file before starting services"
else
    echo "✓ .env file already exists"
fi

# Set permissions
echo ""
echo "Setting permissions..."
chmod +x "$PROJECT_ROOT/scripts/deploy.sh"

# Verify file structure
echo ""
echo "Verifying file structure..."
REQUIRED_FILES=(
    "docker-compose.yml"
    "docker/Dockerfile.backend"
    "docker/Dockerfile.frontend"
    "docker/nginx/nginx.conf"
    "docker/nginx/spa.conf"
    "scripts/deploy.sh"
    "Makefile"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "✓ $file"
    else
        echo "❌ $file (missing)"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "⚠️  Some required files are missing!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review .env file and customize as needed"
echo "  2. Run: make start    (or: ./scripts/deploy.sh start)"
echo "  3. Access apps at:"
echo "     - Customer:   http://localhost:3001"
echo "     - Restaurant: http://localhost:3002"
echo "     - Admin:      http://localhost:3003"
echo "     - API:        http://localhost:3000"
echo ""
echo "Useful commands:"
echo "  make help     - Show all available commands"
echo "  make logs     - View service logs"
echo "  make health   - Check service health"
echo ""
