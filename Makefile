ifeq ($(OS),Windows_NT)
    OS := windows
else
    OS := $(shell uname -s | tr A-Z a-z)
endif

# Цели
.PHONY: all up build deps db dev clean

# Основная цель
all: deps db dev

check_docker:
ifeq ($(OS),windows)
	@docker ps > NUL 2>&1 || (echo "Docker is not running. Please start Docker and try again." && exit 1)
else
	@docker ps > /dev/null 2>&1 || (echo "Docker is not running. Please start Docker and try again." && exit 1)
endif

# Docker цели
up: check_docker
	docker-compose up setup
	docker-compose up

build: check_docker
	docker-compose build

down: check_docker
	docker-compose down

up-non-log: check_docker
	docker-compose -f ./docker-compose-non-log.yml up

down-non-log: check_docker
	docker-compose -f ./docker-compose-non-log.yml down

# Установка зависимостей с помощью poetry и создание виртуального окружения
deps:
	poetry install

# Работа с базой данных
db: deps
	cd backend && \
	alembic revision --autogenerate && \
	alembic upgrade head

# Запуск приложения в режиме разработки
dev: db
	cd backend/src && \
	uvicorn main:app --reload

# Очистка проекта
clean:
	poetry env remove python
	find . -type d -name "__pycache__" -exec rm -rf {} +
