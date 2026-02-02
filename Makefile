# Variables
PYTHON = python3
PIP = pip
VENV = .venv
BIN = $(VENV)/bin

.PHONY: install run debug clean lint lint-strict

# Install project dependencies
install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/$(PIP) install --upgrade pip
	$(BIN)/$(PIP) install flake8 mypy setuptools wheel build
	@if [ -f requirements.txt ]; then $(BIN)/$(PIP) install -r requirements.txt; fi

# Execute the main script
run:
	$(BIN)/$(PYTHON) a_maze_ing.py config.txt

# Run in debug mode using pdb
debug:
	$(BIN)/$(PYTHON) -m pdb a_maze_ing.py config.txt

# Remove temporary files or caches
clean:
	rm -rf $(VENV)
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Mandatory lint with specified flags
lint:
	$(BIN)/flake8 .
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Optional strict checking
lint-strict:
	$(BIN)/flake8 .
	$(BIN)/mypy . --strict