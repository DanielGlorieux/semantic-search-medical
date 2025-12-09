# 🏥 Medical Search Engine - Projet de Recherche Sémantique

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

## 📋 Description

Application de recherche sémantique médicale avec génération de réponses par IA (RAG). Utilise FAISS pour l'indexation vectorielle, Sentence Transformers pour les embeddings, et Google Gemini pour générer des réponses conviviales en français.

**Dataset**: 16,412 questions médicales du dataset MedQuAD (Kaggle)  
**Technologies**: Python, FAISS, Sentence Transformers, Google Gemini, FastAPI, Streamlit

### ✨ Fonctionnalités Clés

- 🔍 **Recherche Sémantique Ultra-Rapide** (~50ms)
- 🤖 **RAG avec Google Gemini** (réponses en français)
- ⚡ **Re-ranking Intelligent** avec CrossEncoder
- 📊 **Interface Moderne** avec statistiques en temps réel
- 📈 **Métriques de Performance** (Recall, MRR, Latence)
- 🌐 **API REST** documentée (Swagger)
- 🎨 **Thème Sombre** optimisé pour la lisibilité

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
