.DEFAULT_GOAL = help

help:
	@echo ""
	@echo ========== HELP ==========
	@echo ""
	@echo Setup the Sales Flow RAG Application
	@echo To install: make install
	@echo To build: make build
	@echo To help: make
	@echo Tip: before run, you must the local config and environment variables files
	@echo Tip: Install first, Build after
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
