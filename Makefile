SHELL := /bin/bash	

# run app
run_dev:
	@echo "Running app (DEV)..."
	@source venv/bin/activate && \
		cd frontend && \
		echo $$PWD && \
		python app.py
		