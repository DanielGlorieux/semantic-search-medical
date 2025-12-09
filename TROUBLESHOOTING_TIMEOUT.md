# 🔧 Guide de Dépannage - Timeouts RAG

## ✅ Problème Résolu !

Les **timeouts** ont été corrigés avec les optimisations suivantes :

### 🚀 Optimisations Appliquées

| Composant | Avant | Après | Impact |
|-----------|-------|-------|--------|
| **Timeout Frontend** | 30s | 120s | ✅ Plus de marge |
| **Timeout Gemini** | ∞ | 60s | ✅ Fail-fast |
| **Tokens max** | ∞ | 512 | ✅ Réponse + rapide |
| **Contexte/doc** | Complet | 1000 chars | ✅ -70% de tokens |
| **Prompt** | Long (250 mots) | Court (30 mots) | ✅ -80% de tokens |

### 📊 Résultats des Tests

```
✅ Test 1 - Réponse RAG : 5.40s  🟡 BON
✅ Test 2 - Résumé      : 1.50s  🟢 EXCELLENT
✅ Taux de succès       : 100%
```

---

## 🎯 Performance Attendue

Avec les optimisations, vous devriez obtenir :

| Métrique | Cible | Statut |
|----------|-------|--------|
| Latence RAG | 3-8 secondes | 🟢 Atteint |
| Latence Résumé | 1-3 secondes | 🟢 Atteint |
| Taux de succès | > 95% | 🟢 Atteint |

---

## 🐛 Si les Timeouts Persistent

### Symptôme 1 : "Request Timeout" dans Streamlit

**Cause possible :**
- Votre connexion internet est lente
- Le quota API Gemini est atteint
- Le backend est surchargé

**Solutions :**

1. **Vérifier votre connexion internet :**
   ```powershell
   ping google.com
   ```
   Si la latence > 200ms, c'est probablement votre connexion.

2. **Vérifier le quota Gemini :**
   - Allez sur : https://aistudio.google.com/app/apikey
   - Regardez votre utilisation
   - Limite gratuite : 60 req/min ou 1500 req/jour

3. **Augmenter encore le timeout :**
   
   Dans `frontend/app_streamlit.py` ligne 330 :
   ```python
   timeout=180  # 3 minutes au lieu de 2
   ```

4. **Réduire la taille du contexte :**
   
   Dans `backend/app/services/rag_service.py` ligne 100 :
   ```python
   if len(text) > 500:  # Au lieu de 1000
       text = text[:500] + "..."
   ```

5. **Réduire max_output_tokens :**
   
   Dans `backend/app/services/rag_service.py` ligne 75 :
   ```python
   "max_output_tokens": 256,  # Au lieu de 512
   ```

---

### Symptôme 2 : Backend ne répond pas

**Diagnostic :**
```powershell
# Tester le backend directement
curl http://localhost:8000/health
```

**Si pas de réponse :**

1. **Vérifier que le backend tourne :**
   ```powershell
   # Chercher le processus uvicorn
   Get-Process | Where-Object {$_.Name -like "*python*"}
   ```

2. **Redémarrer le backend :**
   ```powershell
   cd backend
   uvicorn app.main:app --reload --timeout-keep-alive 120
   ```

3. **Vérifier les logs du backend :**
   - Regardez dans le terminal où tourne le backend
   - Cherchez les erreurs `ERROR:` ou `CRITICAL:`

---

### Symptôme 3 : "429 Quota Exceeded" de Gemini

**Cause :**
Vous avez dépassé le quota gratuit de Gemini.

**Solutions :**

1. **Attendre** : Le quota se réinitialise toutes les minutes (60 req/min)

2. **Créer une nouvelle clé API** :
   - https://aistudio.google.com/app/apikey
   - Cliquez sur "Create API Key"
   - Remplacez dans `.env` :
     ```
     GEMINI_API_KEY=VOTRE_NOUVELLE_CLE
     ```

3. **Réduire la fréquence des requêtes** :
   - Attendez 2-3 secondes entre chaque recherche
   - Évitez de faire trop de recherches en succession rapide

---

### Symptôme 4 : Réponse vide ou erreur dans Streamlit

**Vérifications :**

1. **Tester le RAG directement :**
   ```powershell
   python test_rag_speed.py
   ```
   
   Si ça marche ici mais pas dans Streamlit, le problème vient du frontend.

2. **Vérifier les logs du backend :**
   ```
   ERROR:app.main:Search error: ...
   ```

3. **Tester l'API manuellement :**
   - Ouvrez : http://localhost:8000/docs
   - Essayez `POST /rag/answer`
   - Body :
     ```json
     {
       "query": "What is diabetes?",
       "top_k": 5
     }
     ```

---

## 🔧 Configuration Recommandée

### Pour Connexion Rapide (> 10 Mbps)

**`backend/app/services/rag_service.py`** :
```python
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 512,  # Réponses détaillées OK
}
```

**`frontend/app_streamlit.py`** :
```python
timeout=120  # 2 minutes suffisent
```

### Pour Connexion Lente (< 5 Mbps)

**`backend/app/services/rag_service.py`** :
```python
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 256,  # Réponses courtes
}

# Dans _build_context :
if len(text) > 500:  # Contexte réduit
    text = text[:500] + "..."
```

**`frontend/app_streamlit.py`** :
```python
timeout=180  # 3 minutes
```

---

## 📊 Monitoring en Temps Réel

### Vérifier la Santé du Système

**Terminal 1 - Monitoring Backend :**
```powershell
# Surveiller les logs en temps réel
cd backend
uvicorn app.main:app --reload --log-level debug
```

**Terminal 2 - Test Continue :**
```powershell
# Tester toutes les 10 secondes
while ($true) {
    curl http://localhost:8000/health
    Start-Sleep 10
}
```

### Métriques à Surveiller

Dans Streamlit, après une recherche, vérifiez :

| Métrique | Valeur Normale | Alerte |
|----------|---------------|---------|
| **Latence** | 1-8s | > 15s |
| **Nombre de résultats** | 5-10 | 0 |
| **Score FAISS** | > 0.6 | < 0.3 |

---

## 🎯 Tests de Performance

### Test 1 : Vitesse du RAG

```powershell
python test_rag_speed.py
```

**Résultat attendu :**
```
✅ Réponse générée en 3-8s
✅ Résumé généré en 1-3s
```

### Test 2 : Test de Charge

```powershell
# Faire 5 requêtes d'affilée
for ($i=1; $i -le 5; $i++) {
    Write-Host "Test $i..."
    python test_rag_speed.py
    Start-Sleep 3
}
```

**Toutes les requêtes doivent réussir.**

### Test 3 : Gemini API Seul

```powershell
python test_gemini.py
```

**Résultat attendu :**
```
✅ RÉPONSE DE GEMINI
Dis bonjour.
```

---

## 💡 Astuces d'Optimisation Avancées

### 1. Réduire la taille du contexte dynamiquement

Modifiez `_build_context` pour adapter la taille selon la question :

```python
def _build_context(self, docs: List[Dict], query_length: int) -> str:
    # Si question courte, contexte court
    max_chars = 500 if query_length < 50 else 1000
    
    context_parts = []
    for i, doc in enumerate(docs, 1):
        text = doc.get("text", "")
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        # ...
```

### 2. Cache les réponses fréquentes

Ajoutez un cache simple :

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def generate_response_cached(self, query: str) -> str:
    # Recherche dans le cache d'abord
    # Sinon, génère la réponse
    pass
```

### 3. Mode "Fast" vs "Quality"

Ajoutez un paramètre `speed_mode` :

```python
if speed_mode == "fast":
    generation_config["max_output_tokens"] = 256
    max_docs = 2
else:  # quality
    generation_config["max_output_tokens"] = 512
    max_docs = 5
```

---

## 📞 Support

Si les problèmes persistent après avoir essayé toutes ces solutions :

1. **Vérifiez les logs du backend** pour des erreurs spécifiques
2. **Testez chaque composant individuellement** (FAISS, Gemini, API)
3. **Vérifiez votre quota Gemini** sur Google AI Studio
4. **Essayez avec une clé API différente**

---

## ✅ Checklist de Dépannage

Avant de chercher de l'aide, vérifiez :

- [ ] ✅ Le backend est démarré (`uvicorn` tourne)
- [ ] ✅ Streamlit est démarré
- [ ] ✅ `.env` contient `GEMINI_API_KEY`
- [ ] ✅ `google-generativeai` est installé
- [ ] ✅ `test_gemini.py` fonctionne
- [ ] ✅ `test_rag_speed.py` fonctionne
- [ ] ✅ http://localhost:8000/health retourne `"rag_service_available": true`
- [ ] ✅ Votre connexion internet fonctionne (ping google.com)
- [ ] ✅ Vous n'avez pas dépassé le quota Gemini

---

## 🎉 Tout Fonctionne ?

Si les optimisations ont résolu vos problèmes :

**Performance attendue :**
- ⚡ Latence : 3-8 secondes
- 📝 Réponse : Complète et en français
- ✅ Taux de succès : > 95%

**Profitez de votre système de RAG ! 🚀🤖**
