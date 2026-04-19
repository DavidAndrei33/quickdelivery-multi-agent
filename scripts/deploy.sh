#!/bin/bash

# QuickDelivery Food Platform - Deployment Script
# Usage: ./deploy.sh [command] [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="quickdelivery"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if docker and docker-compose are installed
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f "$ENV_FILE" ]; then
        log_warning ".env file not found. Copying from .env.example..."
        if [ -f ".env.example" ]; then
            cp .env.example "$ENV_FILE"
            log_success ".env file created from .env.example"
            log_warning "Please review and update .env file with your configuration before continuing."
        else
            log_error ".env.example file not found. Cannot create .env file."
            exit 1
        fi
    fi
    
    log_success "Prerequisites check passed"
}

# Build all services
build() {
    log_info "Building all services..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" build --no-cache "$@"
    log_success "Build completed"
}

# Start services
start() {
    log_info "Starting QuickDelivery services..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d
    log_success "Services started successfully"
    
    echo ""
    echo "Services available at:"
    echo "  - API Backend:      http://localhost:3000"
    echo "  - Customer App:     http://localhost:3001"
    echo "  - Restaurant App:   http://localhost:3002"
    echo "  - Admin App:        http://localhost:3003"
    echo "  - Nginx (Proxy):    http://localhost:80"
    echo ""
    echo "Database:"
    echo "  - PostgreSQL:       localhost:5432"
    echo "  - Redis:            localhost:6379"
}

# Stop services
stop() {
    log_info "Stopping QuickDelivery services..."
    docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" down
    log_success "Services stopped"
}

# Restart services
restart() {
    log_info "Restarting QuickDelivery services..."
    stop
    start
}

# View logs
logs() {
    local service="$1"
    if [ -n "$service" ]; then
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" logs -f "$service"
    else
        docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" logs -f
    fi
}

# Check health status
health() {
    log_info "Checking service health..."
    
    echo ""
    echo "Container Status:"
    docker-compose -f "$COMPOSE_FILE" ps
    
    echo ""
    echo "Health Checks:"
    
    # Check PostgreSQL
    if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
        log_success "PostgreSQL is healthy"
    else
        log_error "PostgreSQL is not responding"
    fi
    
    # Check Redis
    if docker-compose -f "$COMPOSE_FILE" exec -T redis redis-cli ping > /dev/null 2>&1; then
        log_success "Redis is healthy"
    else
        log_error "Redis is not responding"
    fi
    
    # Check Backend
    if curl -s http://localhost:3000/api/v1/health > /dev/null 2>&1; then
        log_success "Backend API is healthy"
    else
        log_error "Backend API is not responding"
    fi
}

# Reset everything (WARNING: destroys data!)
reset() {
    log_warning "This will destroy all data including database volumes!"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        log_info "Stopping services and removing volumes..."
        docker-compose -f "$COMPOSE_FILE" down -v
        log_success "All services and volumes removed"
    else
        log_info "Reset cancelled"
    fi
}

# Run database migrations
migrate() {
    log_info "Running database migrations..."
    docker-compose -f "$COMPOSE_FILE" exec backend npm run migrate
}

# Seed database
seed() {
    log_info "Seeding database..."
    docker-compose -f "$COMPOSE_FILE" exec backend npm run seed
}

# Update images
update() {
    log_info "Pulling latest images..."
    docker-compose -f "$COMPOSE_FILE" pull
    log_info "Rebuilding services..."
    docker-compose -f "$COMPOSE_FILE" up -d --build
    log_success "Update completed"
}

# Show help
help() {
    echo "QuickDelivery Food Platform - Deployment Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build     - Build all Docker images"
    echo "  start     - Start all services"
    echo "  stop      - Stop all services"
    echo "  restart   - Restart all services"
    echo "  logs      - View logs (optionally: logs [service-name])"
    echo "  health    - Check health status of services"
    echo "  migrate   - Run database migrations"
    echo "  seed      - Seed database with test data"
    echo "  update    - Update and restart services"
    echo "  reset     - Destroy all data and containers (DANGEROUS!)"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 start"
    echo "  $0 logs backend"
    echo ""
}

# Main
main() {
    case "${1:-help}" in
        build)
            check_prerequisites
            build "${@:2}"
            ;;
        start)
            check_prerequisites
            start
            ;;
        stop)
            stop
            ;;
        restart)
            check_prerequisites
            restart
            ;;
        logs)
            logs "$2"
            ;;
        health)
            health
            ;;
        migrate)
            migrate
            ;;
        seed)
            seed
            ;;
        update)
            check_prerequisites
            update
            ;;
        reset)
            reset
            ;;
        help|--help|-h)
            help
            ;;
        *)
            log_error "Unknown command: $1"
            help
            exit 1
            ;;
    esac
}

main "$@"
