.PHONY: help train test run-actions run-rasa clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  train        - Train the Rasa model"
	@echo "  test         - Run tests"
	@echo "  run-actions  - Run action server"
	@echo "  run-rasa     - Run Rasa server"
	@echo "  clean        - Clean generated files"
	@echo "  docker-build - Build Docker images"
	@echo "  docker-up    - Start services with Docker Compose"
	@echo "  docker-down  - Stop Docker Compose services"

train:
	rasa train

test:
	python -m pytest tests/ -v

run-actions:
	rasa run actions --debug

run-rasa:
	rasa run --enable-api --cors "*" --debug

clean:
	rm -rf models/*.tar.gz
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

validate:
	rasa data validate

shell:
	rasa shell

interactive:
	rasa interactive