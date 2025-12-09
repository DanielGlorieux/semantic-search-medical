# 🚀 Démarrage Rapide du RAG

## ✅ Le RAG est maintenant configuré !

### 🔧 Ce qui a été corrigé :

1. ✅ `google-generativeai` installé
2. ✅ Modèle corrigé : `gemini-2.5-flash` (au lieu de l'ancien `gemini-pro`)
3. ✅ API testée et fonctionnelle
4. ✅ Votre clé API fonctionne correctement

---

## 🚀 Démarrage en 3 Étapes

### 1️⃣ Démarrer le Backend

Ouvrez un terminal PowerShell :

```powershell
cd C:\Users\danie\Desktop\TP\semantic_search_project\backend
uvicorn app.main:app --reload
```

**Attendez de voir :**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Loading search engine...
INFO:     Search engine loaded successfully
INFO:     Initializing RAG service with Gemini...
INFO:     Gemini model initialized successfully  ← IMPORTANT !
INFO:     RAG service initialized successfully   ← IMPORTANT !
```

### 2️⃣ Lancer Streamlit

Ouvrez un **NOUVEAU terminal** PowerShell :

```powershell
cd C:\Users\danie\Desktop\TP\semantic_search_project
streamlit run frontend/app_streamlit.py
```

**Votre navigateur s'ouvrira automatiquement sur :** `http://localhost:8501`

### 3️⃣ Tester le RAG

Dans l'interface Streamlit :

1. **Dans la sidebar (à gauche)**, cochez ✅ **"🤖 Activer RAG avec Gemini"**
2. **Tapez une question médicale**, par exemple :
   - `What are the symptoms of diabetes?`
   - `How is glaucoma treated?`
   - `What causes high blood pressure?`
3. **Cliquez sur 🔍 Rechercher**

---

## 🎯 Ce que vous allez voir

### 🤖 Réponse Générée par l'IA
Une belle carte avec la réponse en **français**, structurée et conviviale :

```
D'après les informations médicales disponibles, le diabète 
se manifeste par plusieurs symptômes importants :

• Soif excessive (polydipsie)
• Envie fréquente d'uriner (polyurie)
• Fatigue chronique
• Vision floue
• Perte de poids inexpliquée

Ces symptômes apparaissent lorsque le corps ne peut plus 
réguler correctement le taux de glucose dans le sang...

⚠️ Ces informations ne remplacent pas un avis médical 
professionnel. Consultez votre médecin pour un diagnostic.
```

### 📝 Résumé des Sources
Un résumé court des documents utilisés :

```
Ces informations proviennent de 3 documents médicaux 
officiels du NIH (National Institutes of Health) concernant 
le diabète, ses symptômes et son diagnostic.
```

### 📋 Documents Sources
Les documents bruts récupérés par FAISS, avec leurs scores de pertinence.

---

## ✅ Vérification du Statut

### Test 1 : Vérifier le Backend

Ouvrez : http://localhost:8000/health

Vous devriez voir :
```json
{
  "status": "healthy",
  "search_engine_loaded": true,
  "rag_service_available": true  ← Doit être TRUE !
}
```

### Test 2 : Tester l'API RAG directement

Ouvrez : http://localhost:8000/docs

Essayez l'endpoint **POST /rag/answer** avec :
```json
{
  "query": "What are the symptoms of diabetes?",
  "top_k": 5
}
```

---

## 💡 Exemples de Questions

### Questions Médicales Générales
- `What are the symptoms of diabetes?`
- `How is high blood pressure diagnosed?`
- `What causes heart disease?`

### Questions sur des Maladies Spécifiques
- `What are the risk factors for glaucoma?`
- `How is asthma treated?`
- `What are the symptoms of stroke?`

### Questions sur les Traitements
- `How is cancer treated?`
- `What medications are used for hypertension?`
- `What are the side effects of diabetes medication?`

---

## 🐛 Dépannage

### Problème : "rag_service_available": false

**Solution :**
```powershell
# Vérifier que google-generativeai est installé
pip show google-generativeai

# Si non installé
pip install google-generativeai
```

### Problème : Erreur de clé API

**Solution :**
1. Vérifiez `.env` :
   ```powershell
   cat .env
   ```
2. La clé doit commencer par `AIzaSy...`
3. Obtenez une nouvelle clé : https://makersuite.google.com/app/apikey

### Problème : "Quota exceeded"

**Solution :**
- Vous avez dépassé le quota gratuit (60 req/min ou 1500 req/jour)
- Attendez quelques minutes
- Ou créez une nouvelle clé API

### Problème : Le backend ne démarre pas

**Solution :**
```powershell
# Vérifier les logs d'erreur
cd backend
python -c "from app.main import app; print('OK')"

# Vérifier que les dépendances sont installées
pip install -r requirements.txt
```

---

## 📊 Métriques du RAG

- **Latence moyenne** : 1-3 secondes
- **Qualité des réponses** : Excellente (Gemini 2.5 Flash)
- **Langue de sortie** : Français
- **Sources utilisées** : 3-5 documents
- **Coût** : GRATUIT (jusqu'à 1500 req/jour)

---

## 🎉 Félicitations !

Votre système de **Recherche Sémantique avec RAG** est opérationnel !

Vous avez maintenant :
- ✅ Moteur de recherche sémantique (FAISS + Sentence Transformers)
- ✅ Re-ranking avec CrossEncoder
- ✅ Génération de réponses conviviales en français (Gemini)
- ✅ Interface web moderne (Streamlit)
- ✅ API REST (FastAPI)

**Profitez-en ! 🚀🤖**

---

## 📚 Pour aller plus loin

- Consultez `GEMINI_SETUP.md` pour plus de détails
- Testez différentes questions
- Explorez l'API : http://localhost:8000/docs
- Personnalisez les prompts dans `backend/app/services/rag_service.py`
