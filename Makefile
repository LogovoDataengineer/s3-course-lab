# Короткие команды для учебного стенда. Запускать из корня репозитория.
SHELL := /bin/bash
.PHONY: up down ps logs reset

up:        ## собрать (в первый раз), запустить стенд и дождаться готовности
	@docker compose up -d --wait --wait-timeout 180 minio
	@docker compose run --rm init
	@mkdir -p $(HOME)/.local/bin
	@test -x $(HOME)/.local/bin/mc || docker compose cp minio:/usr/local/bin/mc $(HOME)/.local/bin/mc >/dev/null 2>&1
	@echo "Стенд запущен. Консоль MinIO: порт 19001 (вкладка PORTS), S3 API: http://localhost:19000"

down:      ## остановить стенд, данные сохраняются
	@docker compose stop

ps:        ## показать состояние контейнеров
	@docker compose ps -a --format 'table {{.Name}}\t{{.Status}}\t{{.Ports}}'

logs:      ## последние строки журнала MinIO
	@docker compose logs --tail 50 minio

reset:     ## удалить контейнеры и ВСЕ данные стенда
	@test "$(CONFIRM)" = "yes" || (echo "Удалит все бакеты и объекты. Запустите: make reset CONFIRM=yes"; exit 1)
	docker compose down -v
