# 🔧 SOLUTION À L'ERREUR : 'NoneType' object has no attribute 'search'

## ❌ Problème Identifié

Le moteur de recherche ne trouve pas l'index FAISS car :
1. Les dépendances backend ne sont pas installées
2. L'index FAISS n'a pas été construit

## ✅ Solution (3 étapes - 5 minutes)

### Étape 1 : Installer les dépendances backend (2 min)

```bash
# Ouvrir un terminal PowerShell
cd C:\Users\danie\Desktop\TP\semantic_search_project

# Installer les dépendances
pip install -r backend/requirements.txt
```

⏳ Attendez que l'installation se termine...

### Étape 2 : Construire l'index FAISS (3 min)

```bash
# Dans le même terminal
python scripts/build_index.py
```

**Ce qui va se passer :**
1. ✅ Chargement de 16,412 documents
2. ✅ Téléchargement du modèle sentence-transformers (première fois seulement)
3. ✅ Génération des embeddings (peut prendre 2-3 minutes)
4. ✅ Construction de l'index FAISS
5. ✅ Sauvegarde dans `models/`

**Fichiers créés :**
- `models/embeddings.npy` (~25 MB)
- `models/index.faiss` (~25 MB)

### Étape 3 : Relancer l'application

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload
```

Attendez de voir :
```
INFO:     Application startup complete.
INFO:     Loading search engine...
INFO:     Search engine loaded successfully
```

```bash
# Terminal 2 - Frontend (nouveau terminal)
cd C:\Users\danie\Desktop\TP\semantic_search_project
streamlit run frontend/app_streamlit.py
```

## 🎯 Tester

1. Ouvrir http://localhost:8501
2. Entrer une requête : `"What are the symptoms of diabetes?"`
3. Cliquer sur "Rechercher"
4. ✨ Voir les résultats !

## 🔍 Vérifier que Tout est OK

```bash
# Exécuter le script de vérification
python scripts/check_setup.py
```

Vous devriez voir :
```
✅ TOUT EST PRÊT!
```

## 🆘 Si ça ne marche toujours pas

### Problème 1 : Erreur d'installation pip

```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Réessayer
pip install -r backend/requirements.txt
```

### Problème 2 : Mémoire insuffisante pendant build_index

Éditer `scripts/build_index.py` ligne 35 :
```python
# Changer batch_size de 32 à 16
batch_size=16,
```

### Problème 3 : Torch/PyTorch

```bash
# Installer PyTorch CPU seulement
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Problème 4 : FAISS

```bash
# Installer FAISS CPU
pip install faiss-cpu
```

## 📊 Temps Estimés

| Étape | Temps |
|-------|-------|
| Installation dépendances | 2-3 min |
| Build index (16K docs) | 2-5 min |
| **Total** | **5-8 min** |

## 🎓 Explication Technique

**Pourquoi cette erreur ?**

Le code backend fait :
```python
results, latency = search_engine.search(query, ...)
```

Mais `search_engine.index` est `None` car :
- L'index FAISS n'existe pas dans `models/index.faiss`
- Le `load()` ne trouve rien et échoue silencieusement
- La méthode `search()` essaie d'utiliser `self.index.search()` → BOOM!

**Solution :**
1. ✅ Construire l'index avec `build_index.py`
2. ✅ Fixer les chemins (déjà fait dans search_engine.py)
3. ✅ Le `load()` trouve maintenant les fichiers
4. ✅ La recherche fonctionne !

---

**Temps total : ~5 minutes** ⏱️

Suivez les étapes et tout fonctionnera ! 🚀
