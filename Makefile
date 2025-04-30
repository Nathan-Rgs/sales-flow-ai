.DEFAULT_GOAL = help

help:
	@echo ""
	@echo ========== HELP ==========
	@echo ""
	@echo Setup the Sales Flow RAG application
	@echo To install: make install
	@echo To help: make
	@echo ""
	@echo ==========================
	@echo ""

install:
	@echo === INSTALL ===
	sudo apt install figlet python3.12 python3.12-venv python3.12-dev build-essential

build:
	@figlet === BUILD ===
	python3.12 -m venv .venv
	./.venv/bin/pip install -r ./config/requirements.txt
	@mkdir ./logs
	@mkdir ./data
