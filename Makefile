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
		python main.py
		