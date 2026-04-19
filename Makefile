# QuickDelivery Food Platform - Makefile
# Common commands for development and deployment

.PHONY: help build start stop restart logs ps clean migrate seed health dev prod

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
NC := \033[0m # No Color

# Configuration
COMPOSE_FILE := docker-compose.yml
ENV_FILE := .env
PROJECT_NAME := quickdelivery

help: ## Show this help message
	@echo "$(BLUE)QuickDelivery Food Platform - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

check-env: ## Check if .env file exists
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(YELLOW)Warning: .env file not found. Creating from .env.example...$(NC)"; \
		cp .env.example $(ENV_FILE); \
		echo "$(GREEN).env created. Please review and update it before running.$(NC)"; \
	fi

build: check-env ## Build all Docker images
	@echo "$(BLUE)Building all services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) build
	@echo "$(GREEN)Build completed!$(NC)"

start: check-env ## Start all services
	@echo "$(BLUE)Starting QuickDelivery services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)Services started!$(NC)"
	@echo ""
	@echo "Available at:"
	@echo "  Customer:   http://localhost:3001"
	@echo "  Restaurant: http://localhost:3002"
	@echo "  Admin:      http://localhost:3003"
	@echo "  API:        http://localhost:3000"

stop: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down
	@echo "$(GREEN)Services stopped!$(NC)"

restart: stop start ## Restart all services

logs: ## View logs from all services
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-backend: ## View backend logs only
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## View frontend logs only
	docker-compose -f $(COMPOSE_FILE) logs -f customer-app restaurant-app admin-app

ps: ## List running containers
	docker-compose -f $(COMPOSE_FILE) ps

clean: ## Stop and remove all containers and volumes (DESTROYS DATA!)
	@echo "$(YELLOW)WARNING: This will destroy all data including database volumes!$(NC)"
	@read -p "Are you sure? [y/N] " confirm && [ $$confirm = y ] || exit 1
	@echo "$(BLUE)Removing containers and volumes...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down -v
	@echo "$(GREEN)Cleanup completed!$(NC)"

migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend npm run migrate

seed: ## Seed database with test data
	@echo "$(BLUE)Seeding database...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend npm run seed

health: ## Check health status of all services
	@echo "$(BLUE)Checking service health...$(NC)"
	@echo ""
	@echo "Container Status:"
	@docker-compose -f $(COMPOSE_FILE) ps
	@echo ""
	@echo "$(GREEN)Health checks completed!$(NC)"

shell-backend: ## Open shell in backend container
	docker-compose -f $(COMPOSE_FILE) exec backend sh

shell-db: ## Open PostgreSQL shell
	docker-compose -f $(COMPOSE_FILE) exec postgres psql -U postgres -d quickdelivery

shell-redis: ## Open Redis CLI
	docker-compose -f $(COMPOSE_FILE) exec redis redis-cli

update: ## Update and restart all services
	@echo "$(BLUE)Updating services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) pull
	docker-compose -f $(COMPOSE_FILE) up -d --build
	@echo "$(GREEN)Update completed!$(NC)"

dev: ## Start in development mode (with volume mounts)
	@echo "$(BLUE)Starting in development mode...$(NC)"
	NODE_ENV=development docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)Development mode started!$(NC)"

prod: ## Start in production mode
	@echo "$(BLUE)Starting in production mode...$(NC)"
	NODE_ENV=production docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)Production mode started!$(NC)"

backup-db: ## Backup PostgreSQL database
	@echo "$(BLUE)Creating database backup...$(NC)"
	@mkdir -p backups
	docker-compose -f $(COMPOSE_FILE) exec -T postgres pg_dump -U postgres quickdelivery > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Backup created in backups/ directory!$(NC)"

restore-db: ## Restore PostgreSQL database (usage: make restore-db FILE=backups/backup_xxx.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "$(YELLOW)Error: Please specify FILE=path/to/backup.sql$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Restoring database from $(FILE)...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec -T postgres psql -U postgres quickdelivery < $(FILE)
	@echo "$(GREEN)Database restored!$(NC)"

test: ## Run backend tests
	@echo "$(BLUE)Running tests...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend npm test

lint: ## Run linting on backend
	@echo "$(BLUE)Running linter...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec backend npm run lint
