DC = sudo docker compose
LOGS = sudo docker logs
ENV = --env-file app/conf/.env
APP_FILE = docker-compose.yml
APP_CONTAINER = api
EXEC = sudo docker exec -it

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} ${ENV} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} uv run alembic revision --autogenerate -m "${MESSAGE}"

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} uv run alembic upgrade head

.PHONY: init_migrations
init_migrations:
	${EXEC} ${APP_CONTAINER} uv run alembic init migrations