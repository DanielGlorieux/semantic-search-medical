# 📄 Compilation du Rapport LaTeX

## 📋 Fichier créé

- **`rapport_recherche_semantique.tex`** - Rapport complet du projet (40+ pages)

## 🔧 Prérequis

Vous avez besoin d'une distribution LaTeX installée :

### Windows
- **MiKTeX** : https://miktex.org/download
- **TeX Live** : https://www.tug.org/texlive/

### Mac
- **MacTeX** : https://www.tug.org/mactex/

### Linux
```bash
sudo apt-get install texlive-full
```

## 📦 Packages LaTeX requis

Le rapport utilise ces packages (installés automatiquement avec MiKTeX/TeX Live) :
- `rapportECC` (classe de document - doit être fournie par votre école)
- `lipsum`
- `biblatex`
- `appendix`
- `media9`
- `tcolorbox`
- `xcolor`
- `longtable`
- `array`
- `booktabs`
- `hyperref`

## 🚀 Compilation

### Option 1 : Ligne de commande

```bash
cd C:\Users\danie\Desktop\TP\semantic_search_project

# Compilation complète avec bibliographie
pdflatex rapport_recherche_semantique.tex
bibtex rapport_recherche_semantique
pdflatex rapport_recherche_semantique.tex
pdflatex rapport_recherche_semantique.tex
```

### Option 2 : Overleaf (Recommandé)

1. Aller sur https://www.overleaf.com/
2. Créer un nouveau projet
3. Uploader `rapport_recherche_semantique.tex`
4. Uploader la classe `rapportECC.cls` (fournie par votre école)
5. Compiler (Ctrl+S ou bouton "Recompile")

### Option 3 : TeXstudio / TeXmaker

1. Ouvrir `rapport_recherche_semantique.tex`
2. Configurer le compilateur : PDFLaTeX
3. F5 ou Bouton "Build & View"

## ⚠️ Note importante : Classe rapportECC

Le rapport utilise la classe `rapportECC` qui est spécifique à l'École Centrale de Lyon.

**Vous devez avoir :**
- `rapportECC.cls` dans le même dossier que le `.tex`
- OU dans votre distribution LaTeX

**Si vous n'avez pas cette classe :**

### Solution 1 : Remplacer la classe

Éditer ligne 1 du fichier :
```latex
% Au lieu de:
\documentclass{rapportECC}

% Utiliser:
\documentclass[12pt,a4paper]{article}

% Et ajouter après:
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}
\usepackage[left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm]{geometry}

% Définir les commandes manquantes:
\newcommand{\titre}[1]{\title{#1}}
\newcommand{\sujet}[1]{}
\newcommand{\Encadrants}[1]{\author{Encadrant: #1}}
\newcommand{\etudiants}[1]{\author{#1}}
\newcommand{\fairemarges}{}
\newcommand{\fairepagedegarde}{\maketitle}
\newcommand{\tabledematieres}{\tableofcontents\newpage}
```

### Solution 2 : Demander la classe à votre école

Contactez votre enseignant ou le service informatique pour obtenir `rapportECC.cls`.

## 📊 Structure du Rapport

Le rapport contient :

### Sections principales (40+ pages)
1. **Introduction** (2 pages)
   - Contexte et objectifs
   - Domaine médical choisi

2. **Architecture du système** (4 pages)
   - Schéma global
   - Description des composants
   - Technologies utilisées

3. **Technologies utilisées** (3 pages)
   - Stack technique complète
   - Modèles ML (Sentence Transformers, CrossEncoder)
   - FAISS

4. **Implémentation** (8 pages)
   - Structure du projet
   - Workflow de développement
   - Code détaillé avec exemples

5. **Résultats et Évaluation** (5 pages)
   - Métriques de performance
   - Exemples de recherches
   - Visualisations

6. **Difficultés et Solutions** (4 pages)
   - 5 problèmes majeurs rencontrés
   - Solutions détaillées

7. **Extensions** (3 pages)
   - Extensions implémentées
   - Extensions futures

8. **Conclusion** (2 pages)
   - Synthèse
   - Compétences acquises
   - Impact et perspectives

9. **Annexes** (10+ pages)
   - Installation et configuration
   - Commandes utiles
   - Structure des données
   - API Reference
   - Troubleshooting
   - Références

### Éléments inclus
- ✅ Code source formaté avec coloration syntaxique
- ✅ Schémas ASCII art de l'architecture
- ✅ Tableaux de métriques
- ✅ Exemples de requêtes réels
- ✅ Guide d'installation complet
- ✅ API documentation
- ✅ Troubleshooting détaillé
- ✅ Bibliographie et références

## 🎨 Personnalisation

### Modifier les informations

Ligne 51-52 du fichier :
```latex
\Encadrants{Dr. Pegdwendé Nicolas \textsc{SAWADOGO}}
\etudiants{[Votre Nom et Prénom]}  % ← Modifier ici
```

### Ajouter des images

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{images/architecture.png}
\caption{Architecture du système}
\label{fig:architecture}
\end{figure}
```

### Ajouter des références

Créer un fichier `bibtex.bib` :
```bibtex
@article{reimers2019sentence,
  title={Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks},
  author={Reimers, Nils and Gurevych, Iryna},
  journal={EMNLP},
  year={2019}
}
```

Puis citer dans le texte :
```latex
Tel que décrit par \cite{reimers2019sentence}...
```

## 🔍 Vérification

Après compilation, vérifier :
- ✅ Table des matières générée
- ✅ Numérotation des sections correcte
- ✅ Code source bien formaté
- ✅ Tableaux alignés
- ✅ Liens hypertextes fonctionnels
- ✅ Pas d'erreurs LaTeX

## 📤 Export

Le PDF sera créé dans le même dossier :
- **Fichier output** : `rapport_recherche_semantique.pdf`
- **Taille estimée** : 2-3 MB
- **Pages** : ~40-45 pages

## 🆘 Problèmes courants

### Erreur "File rapportECC.cls not found"
→ Voir section "Note importante" ci-dessus

### Erreur "Package tcolorbox not found"
```bash
# MiKTeX
mpm --install=tcolorbox

# TeX Live
tlmgr install tcolorbox
```

### Caractères spéciaux mal affichés
```latex
% Ajouter en haut du fichier
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
```

### Bibliographie vide
```bash
# Compiler dans cet ordre
pdflatex rapport_recherche_semantique.tex
bibtex rapport_recherche_semantique
pdflatex rapport_recherche_semantique.tex
pdflatex rapport_recherche_semantique.tex
```

## 💡 Conseils

1. **Utilisez Overleaf** pour éviter les problèmes de compilation
2. **Compilez régulièrement** pour détecter les erreurs tôt
3. **Sauvegardez** votre travail fréquemment
4. **Vérifiez** la table des matières et les numéros de pages
5. **Testez** tous les liens hypertextes avant soumission

## 📧 Support

En cas de problème :
1. Vérifier les logs de compilation (`.log` file)
2. Chercher l'erreur sur https://tex.stackexchange.com/
3. Demander de l'aide à votre enseignant

---

**Bon courage pour la compilation ! 📚**
