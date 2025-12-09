# 🚀 Démarrage Rapide - Medical Search Engine

## ⚡ Lancer l'Application en 2 Minutes

### Étape 1: Activer l'Environnement Virtuel

```powershell
cd C:\Users\danie\Desktop\TP\semantic_search_project
.\venv\Scripts\Activate.ps1
```

### Étape 2: Ouvrir 2 Terminaux PowerShell

**Terminal 1 - Backend API**:
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Attendez le message:
```
✅ INFO: Application startup complete.
✅ Search engine loaded successfully
✅ RAG service initialized successfully
```

**Terminal 2 - Frontend Streamlit**:
```powershell
streamlit run frontend\app_streamlit.py --server.port 8501
```

Attendez le message:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Étape 3: Ouvrir dans le Navigateur

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

### Étape 4: Tester !

1. Dans l'interface Streamlit, entrez une question:
   - "What are the symptoms of diabetes?"
   - "How is glaucoma treated?"
   - "What causes heart disease?"

2. Activez "🤖 RAG avec Gemini" pour obtenir une réponse en français

3. Consultez les statistiques et graphiques

## 🎯 Exemples de Requêtes

### Questions Médicales
```
- What is diabetes?
- How to prevent heart disease?
- What are the symptoms of glaucoma?
- Treatment options for high blood pressure
- What causes alzheimer's disease?
```

### Avec RAG (Réponses en Français)
Activez simplement "🤖 RAG avec Gemini" dans la sidebar et posez votre question en anglais. Vous recevrez:
1. Une réponse synthétique en français
2. Les documents sources utilisés
3. Les scores de pertinence

## 📊 Vérifications

### Backend Fonctionne ?
```bash
curl http://localhost:8000/health
```

Réponse attendue:
```json
{
  "status": "healthy",
  "search_engine_loaded": true,
  "rag_service_available": true
}
```

### Recherche Fonctionne ?
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is diabetes?\", \"top_k\": 5}"
```

### RAG Fonctionne ?
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is diabetes?\", \"use_rag\": true, \"top_k\": 3}"
```

## 🔧 Dépannage Rapide

### Erreur: "Module not found"
```bash
pip install -r backend/requirements.txt
```

### Erreur: "FAISS index not found"
```bash
python scripts/build_index.py
```

### Erreur: "Connection refused"
- Vérifiez que le backend est démarré (Terminal 1)
- Vérifiez le port 8000 avec: `netstat -an | findstr "8000"`

### Erreur: "Gemini API Key not found"
```bash
# Créer .env dans semantic_search_project/
echo "GEMINI_API_KEY=votre_clé_ici" > .env
```

Obtenir une clé (GRATUIT): https://ai.google.dev/

### Réponses RAG Lentes
- Normal: 3-8 secondes pour la première requête
- Gemini prend du temps pour générer des réponses complètes
- Les requêtes suivantes sont plus rapides

### Réponses Tronquées
Si les réponses sont coupées, vérifiez `backend/app/services/rag_service.py`:
```python
"max_output_tokens": 2048,  # Doit être >= 2048
```

## 🎨 Interface Streamlit

### Sidebar (Configuration)
- **Top-K**: Nombre de résultats (1-20)
- **Re-ranking**: CrossEncoder pour meilleure précision
- **Mode Hybride**: Combine sémantique + lexical
- **RAG**: Active la génération de réponses IA

### Section Principale
1. **Barre de Recherche**: Entrez votre question
2. **Boutons**:
   - 🔍 Rechercher: Lance la recherche
   - 📄 Exemples: Charge des questions prédéfinies
   - 📊 Statistiques: Affiche les métriques du dataset

3. **Résultats**:
   - 🤖 Réponse IA (si RAG activé)
   - 📑 Documents pertinents avec scores
   - 📈 Graphiques de performance

### Statistiques Descriptives
- Distribution des sources médicales
- Longueur moyenne des documents
- Nombre de documents par domaine (focus_area)
- Timeline des requêtes

## 🎬 Utilisation Avancée

### Mode Comparaison
1. Faites une recherche avec RAG désactivé
2. Notez les résultats
3. Activez RAG et refaites la même recherche
4. Comparez la différence !

### Export Résultats
- Les résultats peuvent être téléchargés en JSON
- Bouton "💾 Export" dans l'interface

### Filtres par Source
- Filtrez par source médicale (NIHSeniorHealth, GARD, etc.)
- Affinez vos résultats par domaine (focus_area)

## 📝 Commandes Utiles

### Redémarrer l'Application
```bash
# Terminal 1 (Backend)
Ctrl+C
uvicorn app.main:app --reload

# Terminal 2 (Frontend)
Ctrl+C
streamlit run frontend\app_streamlit.py
```

### Vérifier les Logs
```bash
# Backend logs (dans Terminal 1)
# Les erreurs apparaissent en rouge

# Frontend logs (dans Terminal 2)
# Les erreurs apparaissent avec traceback
```

### Nettoyer le Cache
```bash
# Streamlit cache
streamlit cache clear

# Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

## 🎯 Prochaines Étapes

### Niveau Débutant
1. ✅ Tester différentes questions
2. ✅ Explorer les statistiques
3. ✅ Comparer avec/sans RAG

### Niveau Intermédiaire
1. 📊 Analyser les notebooks Jupyter
2. 🔧 Modifier les paramètres de recherche
3. 📈 Calculer les métriques (Recall, MRR)

### Niveau Avancé
1. 🎨 Personnaliser l'interface Streamlit
2. 🤖 Optimiser les prompts RAG
3. 📚 Ajouter de nouvelles sources de données
4. 🚀 Déployer en production

## 📚 Documentation Complète

- **START_HERE.md**: Guide complet pour débuter
- **SOLUTION_COMPLETE.md**: Tous les problèmes résolus
- **ARCHITECTURE.md**: Architecture technique
- **MEDQUAD_GUIDE.md**: Guide du dataset
- **GEMINI_SETUP.md**: Configuration Gemini
- **COMPILE_LATEX.md**: Compilation du rapport

## 💡 Astuces

### Performance
- Désactiver le re-ranking pour des recherches plus rapides
- Réduire top_k pour moins de latence
- Le premier appel RAG est toujours plus lent (chargement modèle)

### Qualité
- Utiliser le re-ranking pour de meilleurs résultats
- Le RAG fonctionne mieux avec top_k=3 ou 5
- Les questions en anglais donnent de meilleurs résultats

### Debug
- Consulter les logs en temps réel
- Utiliser l'API docs pour tester: http://localhost:8000/docs
- Vérifier le health endpoint: http://localhost:8000/health

## 🎓 Support

### Problème Persiste ?
1. Consulter SOLUTION_COMPLETE.md
2. Vérifier les logs (Terminal 1 et 2)
3. Tester avec `test_gemini.py` ou `test_rag_speed.py`
4. Vérifier la configuration dans `.env`

### Tests Automatiques
```bash
# Test Gemini
python test_gemini.py

# Test vitesse RAG
python test_rag_speed.py

# Tests unitaires
pytest tests/
```

## ✅ Checklist de Démarrage

- [ ] Environnement virtuel activé
- [ ] Backend démarré (port 8000)
- [ ] Frontend démarré (port 8501)
- [ ] http://localhost:8501 accessible
- [ ] http://localhost:8000/docs accessible
- [ ] Clé Gemini configurée (si RAG)
- [ ] Première recherche testée
- [ ] RAG testé

## 🎉 Félicitations !

Votre moteur de recherche médicale est opérationnel ! 

**Prochaine étape**: Explorez les notebooks dans `notebooks/` pour comprendre comment tout fonctionne en détail.

---

**Auteur**: ILBOUDO P. Daniel Glorieux  
**Projet**: Recherche Sémantique Médicale avec RAG  
**Technologies**: Python, FAISS, Sentence Transformers, Gemini, FastAPI, Streamlit
