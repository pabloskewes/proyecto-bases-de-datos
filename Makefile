SHELL := /bin/bash	

# run app
run_dev:
	@echo "Running app (DEV)..."
	@source venv/bin/activate && \
		python3 src/app.py
		