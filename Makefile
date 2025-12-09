# Makefile pour simplifier les commandes

.PHONY: install clean run-backend run-frontend test build-index help

help:
	@echo "Commandes disponibles:"
	@echo "  make install        - Installer les dépendances"
	@echo "  make clean          - Nettoyer les fichiers temporaires"
	@echo "  make run-backend    - Lancer le backend FastAPI"
	@echo "  make run-frontend   - Lancer le frontend Streamlit"
	@echo "  make test           - Exécuter les tests"
	@echo "  make build-index    - Construire l'index FAISS"
	@echo "  make clean-data     - Nettoyer les données"

install:
	pip install -r backend/requirements.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete

run-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	streamlit run frontend/app_streamlit.py

test:
	pytest tests/ -v

build-index:
	python scripts/build_index.py

clean-data:
	python scripts/preprocessing/clean_data.py
