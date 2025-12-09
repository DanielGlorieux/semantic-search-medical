# Guide d'utilisation du Projet

## 📚 Table des matières
1. [Installation](#installation)
2. [Préparation des données](#préparation-des-données)
3. [Construction de l'index](#construction-de-lindex)
4. [Lancement de l'application](#lancement-de-lapplication)
5. [Tests](#tests)
6. [Extension personnalisée](#extension-personnalisée)

## Installation

### 1. Créer un environnement virtuel
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. Installer les dépendances
```bash
cd backend
pip install -r requirements.txt
```

## Préparation des données

### 1. Collecter vos données
Placez votre corpus brut dans `data/raw/corpus.csv` avec au minimum une colonne `text`.

### 2. Nettoyer les données
```bash
python scripts/preprocessing/clean_data.py
```

Cela créera `data/processed/docs.csv` avec le texte nettoyé.

## Construction de l'index

### 1. Générer les embeddings et construire l'index FAISS
```bash
python scripts/build_index.py
```

Cela créera:
- `models/embeddings.npy` : les embeddings des documents
- `models/index.faiss` : l'index FAISS

Cette étape peut prendre du temps selon la taille du corpus.

## Lancement de l'application

### Backend (FastAPI)
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur http://localhost:8000

Documentation interactive : http://localhost:8000/docs

### Frontend (Streamlit)
Dans un autre terminal:
```bash
streamlit run frontend/app_streamlit.py
```

L'interface sera disponible sur http://localhost:8501

## Tests

### Exécuter les tests
```bash
pytest tests/ -v
```

### Tests avec couverture
```bash
pytest tests/ --cov=backend/app --cov-report=html
```

## Exploration avec Notebooks

Les notebooks Jupyter dans le dossier `notebooks/` permettent:
- `01_data_exploration.ipynb` : Explorer les données
- `02_embeddings_visualization.ipynb` : Visualiser les embeddings
- `03_evaluation.ipynb` : Évaluer le moteur de recherche

## Extension personnalisée

Idées d'extensions:
1. **Ajout de filtres** : filtrer par date, catégorie, etc.
2. **Mode hybride avancé** : combiner dense + sparse (BM25)
3. **Génération de réponses** : intégrer un LLM pour générer des réponses
4. **Clustering** : regrouper les documents similaires
5. **API de feedback** : permettre aux utilisateurs de noter les résultats
6. **Dashboard avancé** : ajouter plus de visualisations
7. **Support multilingue** : modèles multilingues
8. **Cache de requêtes** : accélérer les requêtes fréquentes

## Architecture de l'application

```
User Query → FastAPI Backend → Encoder → FAISS Search → CrossEncoder Reranking → Results
                                    ↓
                              Metrics Collection
```

## Métriques d'évaluation

- **Recall@K** : proportion de documents pertinents récupérés parmi tous les pertinents
- **MRR@K** : Mean Reciprocal Rank - position moyenne du premier document pertinent
- **Latence** : temps de réponse moyen

## Troubleshooting

### L'API ne démarre pas
- Vérifier que les dépendances sont installées
- Vérifier que le port 8000 n'est pas déjà utilisé

### Le moteur de recherche n'est pas chargé
- Vérifier que l'index FAISS existe dans `models/`
- Vérifier que les documents existent dans `data/processed/`

### Erreurs de mémoire
- Réduire le batch_size dans la configuration
- Utiliser un index FAISS compressé (IndexIVFPQ)

## Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Streamlit Documentation](https://docs.streamlit.io/)
