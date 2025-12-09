# 🚀 Guide de Démarrage Rapide

## Étape 1 : Installation (5 min)

### Windows
```bash
# Créer un environnement virtuel
python -m venv venv
venv\Scripts\activate

# Installer les dépendances
cd backend
pip install -r requirements.txt
```

### Linux/Mac
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
cd backend
pip install -r requirements.txt
```

## Étape 2 : Préparer vos données (10 min)

### Option A : Utiliser un dataset existant
Télécharger un dataset de Kaggle (ex: articles scientifiques, FAQ, etc.)

### Option B : Créer votre propre corpus
Créer `data/raw/corpus.csv` avec au minimum :
```csv
doc_id,text
1,"Votre premier document..."
2,"Votre second document..."
```

### Nettoyer les données
```bash
python scripts/preprocessing/clean_data.py
```

## Étape 3 : Construire l'index FAISS (15-30 min)

```bash
python scripts/build_index.py
```

⏳ Cette étape peut prendre du temps selon la taille de votre corpus.

Fichiers créés :
- `models/embeddings.npy`
- `models/index.faiss`

## Étape 4 : Lancer l'application (2 min)

### Terminal 1 : Backend
```bash
cd backend
uvicorn app.main:app --reload
```

✓ API disponible sur : http://localhost:8000
✓ Documentation : http://localhost:8000/docs

### Terminal 2 : Frontend
```bash
streamlit run frontend/app_streamlit.py
```

✓ Interface disponible sur : http://localhost:8501

## Étape 5 : Tester l'application

1. Ouvrir http://localhost:8501
2. Entrer une requête : "Comment investir en bourse ?"
3. Voir les résultats !

## 🎯 Prochaines Étapes

### Explorer les notebooks
```bash
jupyter notebook notebooks/
```

### Évaluer le modèle
- Ouvrir `notebooks/03_evaluation.ipynb`
- Calculer Recall@10 et MRR@10

### Visualiser les embeddings
- Ouvrir `notebooks/02_embeddings_visualization.ipynb`
- Voir les clusters de documents

### Personnaliser
- Modifier la configuration dans `config/config.yaml`
- Ajouter vos propres features
- Améliorer l'interface

## ❓ Problèmes fréquents

### "Module not found"
```bash
pip install -r backend/requirements.txt
```

### "Index not found"
```bash
python scripts/build_index.py
```

### "Port already in use"
```bash
# Changer le port
uvicorn app.main:app --port 8001
streamlit run frontend/app_streamlit.py --server.port 8502
```

## 📊 Exemple de Workflow

```
1. Collecter données (Kaggle/Web scraping)
   ↓
2. Placer dans data/raw/corpus.csv
   ↓
3. python scripts/preprocessing/clean_data.py
   ↓
4. python scripts/build_index.py
   ↓
5. Lancer backend + frontend
   ↓
6. Tester et évaluer
   ↓
7. Itérer et améliorer
```

## 🎓 Ressources Utiles

- **Datasets Kaggle** : https://www.kaggle.com/datasets
- **Hugging Face Models** : https://huggingface.co/models
- **FAISS Tutorial** : https://github.com/facebookresearch/faiss/wiki
- **Streamlit Gallery** : https://streamlit.io/gallery

## 📹 Vidéo de Démo

Pour la soumission, créer une vidéo montrant :
1. ✅ Chargement des données
2. ✅ Construction de l'index
3. ✅ Recherche interactive
4. ✅ Visualisation des résultats
5. ✅ Métriques de performance
6. ✅ Votre extension personnalisée

Bon courage ! 🚀
