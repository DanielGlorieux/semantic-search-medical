# 🏥 Guide Spécial MedQuAD

Excellent choix pour le domaine médical ! Voici comment utiliser le dataset MedQuAD de Kaggle.

## 📊 Format du Dataset MedQuAD

Votre CSV MedQuAD a ce format :
```csv
question,answer,source,focus_area
"What is (are) Glaucoma ?","Glaucoma is a group...","NIHSeniorHealth","Glaucoma"
```

## 🔄 Conversion au Format Requis

### Étape 1 : Placer votre fichier

```bash
# Télécharger MedQuAD depuis Kaggle
# Le placer dans: data/raw/medquad.csv
```

### Étape 2 : Convertir avec le script

```bash
python scripts/preprocessing/convert_medquad.py
```

Ce script créera `data/raw/corpus.csv` au bon format.

## 🎛️ Modes de Conversion

Le script offre plusieurs modes de conversion :

### Mode 1 : QA (Recommandé) ⭐
Combine question + réponse
```python
mode="qa"
```
**Résultat:**
```
Question: What is (are) Glaucoma?

Answer: Glaucoma is a group of diseases that can damage the eye's optic nerve...
```

**Avantages:**
- ✅ Contexte complet
- ✅ Meilleur pour la recherche sémantique
- ✅ L'utilisateur peut poser des questions et trouver des réponses

### Mode 2 : Answer Only
Utilise seulement les réponses
```python
mode="answer"
```
**Utilisation:** Quand les réponses sont suffisamment détaillées seules

### Mode 3 : Question Only
Utilise seulement les questions
```python
mode="question"
```
**Utilisation:** Pour un moteur de recherche de questions similaires

### Mode 4 : Full
Inclut tous les champs (question, answer, source, focus_area)
```python
mode="full"
```
**Utilisation:** Pour garder toutes les métadonnées

## 🚀 Workflow Complet

### 1. Télécharger MedQuAD
```bash
# Depuis Kaggle: https://www.kaggle.com/datasets/
# Rechercher "medquad" ou "medical questions"
# Télécharger et extraire
```

### 2. Placer le fichier
```bash
# Copier dans votre projet
copy medquad.csv semantic_search_project\data\raw\
```

### 3. Convertir
```bash
cd semantic_search_project
python scripts/preprocessing/convert_medquad.py
```

**Output:**
```
INFO:__main__:Chargement de MedQuAD depuis data/raw/medquad.csv
INFO:__main__:Dataset chargé: 16407 lignes
INFO:__main__:Colonnes trouvées: ['question', 'answer', 'source', 'focus_area']
INFO:__main__:Mode: Question + Answer combinés
INFO:__main__:✓ Corpus converti sauvegardé: data/raw/corpus.csv
INFO:__main__:  - 16407 documents
```

### 4. Nettoyer
```bash
python scripts/preprocessing/clean_data.py
```

### 5. Construire l'index
```bash
python scripts/build_index.py
```

### 6. Lancer l'application
```bash
# Terminal 1
cd backend
uvicorn app.main:app --reload

# Terminal 2
streamlit run frontend/app_streamlit.py
```

## 🎨 Personnalisation

### Modifier le mode de conversion

Éditer `scripts/preprocessing/convert_medquad.py` ligne 119:
```python
convert_medquad_to_corpus(
    input_path=input_file,
    output_path=output_file,
    mode="qa"  # Changer ici: "qa", "answer", "question", "full"
)
```

### Garder les métadonnées

Le script garde automatiquement `source` et `focus_area` comme colonnes additionnelles.

Vous pouvez les utiliser pour :
- **Filtrer** par source (ex: "NIHSeniorHealth" vs autres)
- **Filtrer** par domaine médical (ex: "Glaucoma", "Diabetes", etc.)
- **Afficher** dans l'interface utilisateur

## 📊 Statistiques MedQuAD

Dataset typique MedQuAD :
- **~16,000+** questions-réponses médicales
- **Sources:** NIH Senior Health, GARD, et autres
- **Domaines:** Maladies rares, conditions communes, etc.
- **Langues:** Anglais

## 🎯 Exemples de Requêtes

Avec votre moteur de recherche MedQuAD, vous pourrez rechercher :

```
"What are the symptoms of diabetes?"
→ Trouve les documents sur les symptômes du diabète

"How to treat glaucoma?"
→ Trouve les traitements pour le glaucome

"What causes heart disease?"
→ Trouve les causes des maladies cardiaques
```

## 💡 Idées d'Extensions pour MedQuAD

1. **Filtres par domaine médical** : Focus area dropdown
2. **Filtres par source** : NIH, GARD, etc.
3. **Highlighting des symptômes** : Coloration spéciale
4. **Liens vers sources** : URLs officielles
5. **Traduction** : Support multilingue
6. **Chatbot médical** : RAG avec LLM pour réponses naturelles
7. **Disclaimer** : Avertissement médical important

## ⚠️ Important - Disclaimer Médical

**À AJOUTER dans votre interface:**

```
⚠️ AVERTISSEMENT MÉDICAL
Cette application est à but éducatif et de recherche uniquement.
Ne remplace PAS un avis médical professionnel.
Consultez toujours un médecin qualifié pour des questions de santé.
```

## 🔍 Vérification

Après conversion, vérifier :

```bash
# Voir les premières lignes
head data/raw/corpus.csv

# Compter les documents
wc -l data/raw/corpus.csv

# Ou en Python
python -c "import pandas as pd; df=pd.read_csv('data/raw/corpus.csv'); print(f'Documents: {len(df)}'); print(df.head())"
```

## ✅ Checklist

- [ ] MedQuAD téléchargé de Kaggle
- [ ] Fichier placé dans `data/raw/medquad.csv`
- [ ] Script de conversion exécuté
- [ ] `corpus.csv` créé avec succès
- [ ] Nombre de documents vérifié (>10,000)
- [ ] Format vérifié (doc_id, text)
- [ ] Prêt pour l'étape de nettoyage

## 🆘 Problèmes Courants

### "File not found: medquad.csv"
```bash
# Vérifier le chemin
ls data/raw/

# Le fichier doit s'appeler exactement medquad.csv
# Ou modifier le script ligne 115
```

### "KeyError: 'question'"
```bash
# Vérifier les noms de colonnes dans votre CSV
# Ils doivent être: question, answer, source, focus_area
# Ou adapter le script
```

### Fichier trop gros
```bash
# Utiliser un subset
python -c "import pandas as pd; df=pd.read_csv('data/raw/medquad.csv'); df.head(5000).to_csv('data/raw/medquad_subset.csv', index=False)"
```

---

**Bon courage avec votre projet médical ! 🏥🚀**

Les questions-réponses médicales sont parfaites pour démontrer la puissance de la recherche sémantique !
