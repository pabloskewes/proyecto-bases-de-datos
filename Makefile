SHELL := /bin/bash	

run_frontend:
	@echo "Running app (DEV)..."
	@source venv/bin/activate && \
		cd frontend && \
		echo $$PWD && \
		python app.py
		
run_backend:
	@echo "Running app (DEV)..."
	@source venv/bin/activate && \
		cd backend && \
		echo $$PWD && \
		uvicorn main:app --reload --port 8091
