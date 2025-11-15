.PHONY: help build up down logs restart clean test train-model

# Variables
COMPOSE_FILE=docker-compose.yml
PROJECT_NAME=concesionario

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configurar el proyecto (copiar .env.example a .env)
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Archivo .env creado. Edita las variables de entorno antes de continuar."; \
	else \
		echo "⚠️  El archivo .env ya existe."; \
	fi

build: ## Construir todas las imágenes Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Levantar todos los servicios
	docker-compose -f $(COMPOSE_FILE) up -d

down: ## Detener todos los servicios
	docker-compose -f $(COMPOSE_FILE) down

logs: ## Ver logs de todos los servicios
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-backend: ## Ver logs del backend
	docker-compose -f $(COMPOSE_FILE) logs -f backend

logs-frontend: ## Ver logs del frontend
	docker-compose -f $(COMPOSE_FILE) logs -f frontend

logs-backoffice: ## Ver logs del backoffice
	docker-compose -f $(COMPOSE_FILE) logs -f backoffice

logs-mongodb: ## Ver logs de MongoDB
	docker-compose -f $(COMPOSE_FILE) logs -f mongodb

restart: ## Reiniciar todos los servicios
	docker-compose -f $(COMPOSE_FILE) restart

restart-backend: ## Reiniciar solo el backend
	docker-compose -f $(COMPOSE_FILE) restart backend

restart-frontend: ## Reiniciar solo el frontend
	docker-compose -f $(COMPOSE_FILE) restart frontend

ps: ## Ver estado de los servicios
	docker-compose -f $(COMPOSE_FILE) ps

clean: ## Detener servicios y eliminar volúmenes
	docker-compose -f $(COMPOSE_FILE) down -v
	docker system prune -f

clean-all: ## Limpieza completa (incluye imágenes)
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	docker system prune -af

shell-backend: ## Abrir shell en el contenedor del backend
	docker-compose -f $(COMPOSE_FILE) exec backend /bin/bash

shell-mongodb: ## Abrir shell de MongoDB
	docker-compose -f $(COMPOSE_FILE) exec mongodb mongosh -u admin -p changeme123

train-model: ## Entrenar el modelo de preferencias
	docker-compose -f $(COMPOSE_FILE) exec backend python chatbot/vector.py

test-backend: ## Ejecutar tests del backend (si existen)
	docker-compose -f $(COMPOSE_FILE) exec backend pytest

dev: setup build up ## Setup completo para desarrollo
	@echo "✅ Entorno de desarrollo listo!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "Backend Docs: http://localhost:8000/docs"
	@echo "Backoffice: http://localhost:8501"
	@echo "MongoDB: mongodb://localhost:27017"

install: ## Instalar dependencias en contenedores
	docker-compose -f $(COMPOSE_FILE) exec backend pip install -r requirements.txt
	docker-compose -f $(COMPOSE_FILE) exec frontend npm install

seed: ## Ejecutar seed de la base de datos
	docker-compose -f $(COMPOSE_FILE) exec backend python seed_database.py

seed-local: ## Ejecutar seed localmente (sin Docker)
	cd backend/FastApi && python seed_database.py
