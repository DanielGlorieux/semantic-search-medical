# Projet de Recherche Sémantique - Big Data & Vector DB

## 📋 Description
Application de recherche sémantique utilisant Spark, FAISS et des embeddings pour retrouver des documents pertinents à partir de requêtes en langage naturel.

## 🏗️ Architecture
```
├── backend/          # API FastAPI
├── frontend/         # Interface utilisateur (Streamlit/React)
├── data/            # Données brutes et traitées
├── notebooks/       # Jupyter notebooks d'exploration
├── models/          # Modèles et index FAISS
├── scripts/         # Scripts de prétraitement
├── config/          # Fichiers de configuration
├── tests/           # Tests unitaires
└── docs/            # Documentation
```

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip
- Node.js (si React est utilisé)

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend (Streamlit)
```bash
pip install streamlit
```

### Frontend (React - optionnel)
```bash
cd frontend
npm install
```

## 📊 Étapes du Projet

### 1. Construction du Corpus
- Collecte de 500-2000 documents
- Nettoyage du texte
- Sauvegarde en CSV

### 2. Vectorisation et Indexation
- Génération des embeddings avec sentence-transformers
- Création de l'index FAISS
- Sauvegarde des modèles

### 3. API Backend
- Endpoints REST avec FastAPI
- Re-ranking avec CrossEncoder
- Métriques de performance

### 4. Interface Web
- Interface Streamlit ou React
- Recherche interactive
- Visualisation des résultats

### 5. Évaluation
- Recall@10, MRR@10
- Latence moyenne
- Visualisation des embeddings (UMAP/t-SNE)

### 6. Extension Personnalisée
- Innovation libre
- Améliorations personnelles

## 🎯 Utilisation

### Lancer le Backend
```bash
cd backend
uvicorn app.main:app --reload
```

### Lancer le Frontend (Streamlit)
```bash
streamlit run frontend/app_streamlit.py
```

### Lancer le Frontend (React)
```bash
cd frontend
npm start
```

## 📈 Métriques de Performance
- Recall@10
- MRR@10
- Latence moyenne
- Temps de réponse

## 🧪 Tests
```bash
pytest tests/
```

## 📝 Documentation
Voir le dossier `docs/` pour la documentation détaillée.

## 👥 Contributeurs
[Votre nom/équipe]

## 📄 Licence
MIT
