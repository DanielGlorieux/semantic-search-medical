# 📄 Guide de Compilation LaTeX

## Problèmes Identifiés et Solutions

### 1. Erreurs UTF-8 dans les listings

**Problème**: Caractères accentués français dans les commentaires Python causent des erreurs LaTeX
```
! LaTeX Error: Invalid UTF-8 byte sequence
```

**Solutions**:

#### Option A: Utiliser listingsutf8 (Recommandé)
```latex
\usepackage{listingsutf8}

\begin{lstlisting}[inputencoding=utf8]
# Création de données
# Génération d'embeddings
\end{lstlisting}
```

#### Option B: Enlever les accents des commentaires
```python
# Avant
# Création doc_id
# Chargement données
# Génération embeddings

# Après  
# Creation doc_id
# Chargement donnees
# Generation embeddings
```

#### Option C: Utiliser tcblisting avec UTF-8
```latex
\usepackage[most]{tcolorbox}
\newtcblisting{pythoncode}{
    listing only,
    listing options={
        language=Python,
        inputencoding=utf8
    }
}
```

### 2. Images Manquantes

**Problème**: 
```
! Package pdftex.def Error: File `logos/Logo_ECC.jpg' not found
```

**Solution**:
```bash
# Créer le dossier
mkdir logos

# Copier les logos (ou utiliser draft mode)
# Si pas de logos disponibles, commenter dans le .tex:
% \includegraphics{logos/Logo_ECC.jpg}
```

Ou utiliser draft mode:
```latex
\documentclass[draft]{rapportECC}
```

### 3. Caractères Unicode dans la Structure

**Problème**: Caractères box-drawing (├, └, │, ─) non supportés
```
! LaTeX Error: Unicode character ├ (U+251C) not set up for use with LaTeX
```

**Solution**: Utiliser le package `pmboxdraw` ou remplacer par ASCII

```latex
% Avant (dans le document)
├── backend/
│   ├── app/
│   │   ├── main.py

% Après (ASCII simple)
+-- backend/
|   +-- app/
|   |   +-- main.py
```

## 🚀 Compilation Rapide

### Méthode 1: Script Automatique

Créer `compile.ps1`:
```powershell
# Compilation LaTeX avec gestion d'erreurs
$file = "rapport_recherche_semantique"

# Première passe
pdflatex -interaction=nonstopmode $file.tex

# Bibliographie (si utilisée)
if (Test-Path "$file.bcf") {
    biber $file
}

# Deuxième passe
pdflatex -interaction=nonstopmode $file.tex

# Troisième passe (pour TOC)
pdflatex -interaction=nonstopmode $file.tex

# Ouvrir le PDF
Start-Process "$file.pdf"
```

Exécuter:
```bash
.\compile.ps1
```

### Méthode 2: Make

```makefile
LATEX=pdflatex
BIBER=biber
FILE=rapport_recherche_semantique

pdf:
	$(LATEX) -interaction=nonstopmode $(FILE).tex
	$(BIBER) $(FILE)
	$(LATEX) -interaction=nonstopmode $(FILE).tex
	$(LATEX) -interaction=nonstopmode $(FILE).tex

clean:
	rm -f *.aux *.log *.out *.toc *.bcf *.run.xml *.listing

view: pdf
	start $(FILE).pdf

.PHONY: pdf clean view
```

Exécuter:
```bash
make pdf
make view
```

### Méthode 3: Latexmk (Automatique)

Créer `.latexmkrc`:
```perl
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode';
$biber = 'biber %O %S';
```

Exécuter:
```bash
latexmk -pdf rapport_recherche_semantique.tex
```

## 🛠️ Correction des Erreurs UTF-8

### Script Python pour Nettoyer les Listings

Créer `fix_latex_encoding.py`:
```python
import re

def remove_accents(text):
    """Enlève les accents des commentaires Python"""
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ô': 'o', 'ö': 'o',
        'î': 'i', 'ï': 'i',
        'ç': 'c',
        'É': 'E', 'È': 'E', 'Ê': 'E',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def fix_latex_file(input_file, output_file):
    """Corrige les encodages dans les listings"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver tous les blocs lstlisting
    pattern = r'(\\begin\{lstlisting\}.*?\\end\{lstlisting\})'
    
    def fix_listing(match):
        listing = match.group(1)
        # Enlever accents seulement dans les commentaires
        lines = listing.split('\n')
        fixed_lines = []
        for line in lines:
            if '#' in line:
                parts = line.split('#', 1)
                if len(parts) == 2:
                    code, comment = parts
                    comment = remove_accents(comment)
                    line = code + '#' + comment
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)
    
    content = re.sub(pattern, fix_listing, content, flags=re.DOTALL)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Fichier corrigé: {output_file}")

if __name__ == "__main__":
    fix_latex_file(
        "rapport_recherche_semantique.tex",
        "rapport_recherche_semantique_fixed.tex"
    )
```

Exécuter:
```bash
python fix_latex_encoding.py
pdflatex rapport_recherche_semantique_fixed.tex
```

## 📋 Template Corrigé

### En-tête avec Support UTF-8 Complet

```latex
\documentclass[12pt]{rapportECC}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{listingsutf8}  % Support UTF-8 dans listings

% Configuration listings avec UTF-8
\lstset{
    inputencoding=utf8,
    extendedchars=true,
    literate=
        {é}{{\'e}}1 {è}{{\`e}}1 {ê}{{\^e}}1 {ë}{{\"e}}1
        {à}{{\`a}}1 {â}{{\^a}}1 {ä}{{\"a}}1
        {ù}{{\`u}}1 {û}{{\^u}}1 {ü}{{\"u}}1
        {ô}{{\^o}}1 {ö}{{\"o}}1
        {î}{{\^i}}1 {ï}{{\"i}}1
        {ç}{{\c{c}}}1
}

% Ou utiliser tcolorbox (plus moderne)
\usepackage[most]{tcolorbox}
\newtcblisting{pythoncode}{
    listing only,
    listing options={
        language=Python,
        basicstyle=\ttfamily\small,
        inputencoding=utf8,
        extendedchars=true,
    },
    colback=gray!5,
    colframe=blue!50!black,
}
```

### Remplacer les Listings

```latex
% Avant
\begin{lstlisting}
# Création doc_id
df['doc_id'] = df.index.astype(str)
\end{lstlisting}

% Après (Option 1: Sans accents)
\begin{lstlisting}
# Creation doc_id
df['doc_id'] = df.index.astype(str)
\end{lstlisting}

% Après (Option 2: Avec tcolorbox)
\begin{pythoncode}
# Création doc_id (UTF-8 supporté)
df['doc_id'] = df.index.astype(str)
\end{pythoncode}
```

## ✅ Checklist Avant Compilation

- [ ] Vérifier encodage UTF-8 du fichier .tex
- [ ] Enlever accents des commentaires Python dans listings
- [ ] Vérifier chemins des images (ou mode draft)
- [ ] Remplacer caractères Unicode (├, └, │) par ASCII
- [ ] Tester compilation en mode draft d'abord
- [ ] Vérifier packages installés
- [ ] Mettre à jour nom/prénom dans le document

## 🎯 Compilation Finale

```bash
# 1. Mode draft (rapide, sans images)
pdflatex -interaction=nonstopmode "\def\isdraft{1}\input{rapport_recherche_semantique.tex}"

# 2. Si OK, compilation complète
pdflatex -interaction=nonstopmode rapport_recherche_semantique.tex
pdflatex -interaction=nonstopmode rapport_recherche_semantique.tex
pdflatex -interaction=nonstopmode rapport_recherche_semantique.tex

# 3. Ouvrir le PDF
start rapport_recherche_semantique.pdf
```

## 📝 Nom et Prénom dans le Document

Chercher et remplacer dans le .tex:
```latex
\newcommand{\auteur}{ILBOUDO P. Daniel Glorieux}
\newcommand{\email}{daniel.ilboudo@example.com}
\newcommand{\filiere}{Génie Industriel}
\newcommand{\annee}{2024-2025}
```

## 🆘 En Cas d'Erreur

### Erreur Persistante
1. Compiler en mode draft
2. Identifier la ligne problématique dans le .log
3. Commenter le bloc problématique
4. Compiler progressivement

### Caractères Problématiques
```bash
# Trouver les caractères non-ASCII
grep -P "[\x80-\xFF]" rapport_recherche_semantique.tex
```

### Nettoyage
```bash
# Supprimer fichiers auxiliaires
rm *.aux *.log *.out *.toc *.bcf *.run.xml *.listing *.nlo

# Recompiler from scratch
pdflatex rapport_recherche_semantique.tex
```

## 🎓 Résultat Attendu

Un PDF professionnel avec:
- ✅ Page de garde avec logo ECC
- ✅ Table des matières
- ✅ Sections bien structurées
- ✅ Code Python avec coloration syntaxique
- ✅ Figures et tableaux
- ✅ Bibliographie
- ✅ Annexes

Bonne compilation ! 📄✨
