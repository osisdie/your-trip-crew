.PHONY: up down build logs seed migrate test lint viz-flow open-flow

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

logs-%:
	docker compose logs -f $*

build:
	docker compose build

migrate:
	docker compose exec trip-backend alembic upgrade head

seed:
	docker compose exec trip-backend python -m scripts.seed_packages

test-backend:
	docker compose exec trip-backend pytest app/tests/ -v

test-frontend:
	docker compose exec trip-frontend npm test

lint-backend:
	docker compose exec trip-backend ruff check app/

psql:
	docker compose exec trip-postgres psql -U tripuser -d tripdb

redis-cli:
	docker compose exec trip-redis redis-cli

viz-flow:
	python3 agents/scripts/visualize_flow.py && echo "Open agents/flow_visualization.html in browser"

open-flow:
	cmd.exe /c start "" "$$(wslpath -w '$(CURDIR)/agents/flow_visualization.html')"

clean:
	docker compose down -v --remove-orphans
