# 🤖 Configuration de Google Gemini pour le RAG

Ce guide vous explique comment obtenir et configurer votre clé API Gemini pour activer la fonctionnalité RAG (Retrieval-Augmented Generation).

## 📋 Prérequis

- Un compte Google
- Accès à Google AI Studio
- Python 3.8+

## 🔑 Étape 1 : Obtenir une Clé API Gemini

### Option 1 : Via Google AI Studio (Recommandé - GRATUIT)

1. **Accéder à Google AI Studio**
   ```
   https://makersuite.google.com/app/apikey
   ```

2. **Se connecter avec votre compte Google**
   - Utilisez votre compte Gmail personnel ou professionnel

3. **Créer une clé API**
   - Cliquez sur "Create API Key"
   - Sélectionnez "Create API key in new project" (ou un projet existant)
   - Copiez la clé générée (elle ressemble à : `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

4. **⚠️ IMPORTANT : Gardez cette clé secrète !**
   - Ne la partagez jamais publiquement
   - Ne la commitez pas dans Git
   - Stockez-la dans le fichier `.env`

### Option 2 : Via Google Cloud Console

1. Aller sur : https://console.cloud.google.com/
2. Créer un nouveau projet
3. Activer "Generative Language API"
4. Créer des identifiants (API Key)

## ⚙️ Étape 2 : Configuration du Projet

### 1. Créer le fichier `.env`

```bash
# À la racine du projet
cd C:\Users\danie\Desktop\TP\semantic_search_project
```

Créez un fichier nommé `.env` avec le contenu suivant :

```env
# Gemini API Key
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Backend Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

**Remplacez** `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` par votre vraie clé API !

### 2. Installer les dépendances

```bash
cd backend
pip install google-generativeai python-dotenv
```

Ou installez tout depuis requirements.txt :

```bash
pip install -r requirements.txt
```

## 🚀 Étape 3 : Tester l'Installation

### Test 1 : Vérifier l'API directement

Créez un fichier `test_gemini.py` :

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configurer Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY non trouvée dans .env")
    exit(1)

print(f"✅ Clé API trouvée: {api_key[:10]}...")

# Tester l'API
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content("Dis bonjour en français")
    print(f"✅ Réponse de Gemini: {response.text}")
    print("\n🎉 Gemini fonctionne correctement !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
```

Exécutez le test :

```bash
python test_gemini.py
```

### Test 2 : Vérifier le Backend

Démarrez le backend :

```bash
cd backend
uvicorn app.main:app --reload
```

Testez le endpoint RAG :

```bash
curl -X POST "http://localhost:8000/rag/answer" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of diabetes?", "top_k": 3}'
```

Ou ouvrez : http://localhost:8000/docs

## 📊 Étape 4 : Utiliser le RAG dans l'Interface

### Lancer l'application Streamlit

```bash
cd ..
streamlit run frontend/app_streamlit.py
```

### Utiliser le RAG

1. Dans la **sidebar**, cochez ✅ **"Activer RAG avec Gemini"**
2. Tapez votre question médicale
3. Cliquez sur **"🔍 Rechercher"**
4. Vous verrez :
   - 🤖 **Réponse Générée par l'IA** (en français, conviviale)
   - 📝 **Résumé des Sources**
   - 📋 **Documents Sources** (détails bruts)

## 💡 Exemples de Questions

Testez avec ces questions :

```
1. "What are the symptoms of glaucoma?"
2. "How is diabetes diagnosed?"
3. "What causes heart disease?"
4. "What is the treatment for hypertension?"
5. "What are the risk factors for cancer?"
```

Le RAG va :
- ✅ Récupérer les documents pertinents
- ✅ Générer une réponse en français
- ✅ Structurer l'information de manière claire
- ✅ Ajouter un avertissement médical

## 🔒 Sécurité

### Fichier `.gitignore`

Assurez-vous que `.env` est dans `.gitignore` :

```gitignore
# Environment variables
.env
.env.local
.env.*.local

# API Keys
*.key
secrets/
```

### Vérifier que .env n'est pas tracké

```bash
git status
# .env ne doit PAS apparaître dans la liste
```

## 📈 Limites de l'API Gratuite

### Google AI Studio (Gratuit)

- ✅ **60 requêtes par minute**
- ✅ **1,500 requêtes par jour**
- ✅ Idéal pour développement et tests
- ✅ Pas besoin de carte bancaire

### Si vous dépassez les limites

Vous verrez ce message :
```
Resource has been exhausted (e.g. quota limit)
```

**Solutions :**
1. Attendez quelques minutes
2. Optimisez le nombre de requêtes
3. Utilisez un cache pour les requêtes similaires
4. Passez à Google Cloud avec facturation

## 🐛 Dépannage

### Erreur : "API key not valid"

```bash
# Vérifiez que la clé est correcte
cat .env | grep GEMINI_API_KEY

# Régénérez une nouvelle clé sur https://makersuite.google.com/app/apikey
```

### Erreur : "Module 'google.generativeai' not found"

```bash
pip install google-generativeai
```

### Erreur : "GEMINI_API_KEY not found"

```bash
# Vérifiez que le fichier .env existe
ls -la .env

# Vérifiez le contenu
cat .env

# Le backend doit charger load_dotenv()
```

### Le RAG ne s'active pas

1. Vérifiez le statut du backend :
   ```
   http://localhost:8000/health
   ```
   
2. Cherchez `"rag_service_available": true`

3. Vérifiez les logs du backend :
   ```
   # Dans le terminal où tourne uvicorn
   # Vous devriez voir : "RAG service initialized successfully"
   ```

## 📚 Ressources

- **Documentation Gemini** : https://ai.google.dev/docs
- **Google AI Studio** : https://makersuite.google.com/
- **Exemples de code** : https://github.com/google/generative-ai-python
- **Tarification** : https://ai.google.dev/pricing

## ✅ Checklist de Vérification

- [ ] Clé API Gemini obtenue
- [ ] Fichier `.env` créé avec la clé
- [ ] `.env` dans `.gitignore`
- [ ] `google-generativeai` installé
- [ ] Test `test_gemini.py` réussi
- [ ] Backend démarre sans erreur
- [ ] Endpoint `/health` retourne `rag_service_available: true`
- [ ] Interface Streamlit affiche l'option RAG
- [ ] Une question retourne une réponse en français

## 🎉 C'est Prêt !

Votre système RAG avec Gemini est maintenant opérationnel ! Profitez de réponses médicales conviviales générées par l'IA. 🤖🏥
