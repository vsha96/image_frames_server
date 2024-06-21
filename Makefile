# Constants
ENV=./venv
PYTHON=$(ENV)/bin/python

APP_NAME=image_frames_server_fastapi
SERVICE_NAME=web

PRECOMMIT_VERSION=3.7.1

install:
	python3.12 -m venv $(ENV)
	$(ENV)/bin/pip install --upgrade pip
	$(ENV)/bin/pip install -r requirements.txt

# Start the FastAPI server locally using Uvicorn:
# run: install
#    ./venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Build and run the Docker containers
.PHONY: run-docker
run-docker:
	docker compose -p $(APP_NAME) up --build

# Stop and remove containers
.PHONY: down
down:
	docker compose -p $(APP_NAME) down

# Run tests
.PHONY: test
test:
	docker compose -p $(APP_NAME) up -d  # Ensure the containers are up and running in detached mode
	docker compose -p $(APP_NAME) exec $(SERVICE_NAME) pytest ./app/tests
	docker compose -p $(APP_NAME) stop  # Optional: Take down the containers after testing

pre-commit-download:
	# Install pre-commit with 0 dependencies;
	@if [ -f pre-commit.pyz ]; then \
		echo "pre-commit is already downloaded."; \
	else \
		echo "pre-commit not found, downloading..."; \
		curl -L https://github.com/pre-commit/pre-commit/releases/download/v${PRECOMMIT_VERSION}/pre-commit-${PRECOMMIT_VERSION}.pyz > pre-commit.pyz; \
		echo "pre-commit downloaded successfully."; \
	fi

pre-commit-run-all: pre-commit-download
	$(PYTHON) pre-commit.pyz run --all-files

lint-auto: pre-commit-run-all
	@echo "linting..."
