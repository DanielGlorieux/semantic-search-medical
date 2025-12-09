"""
Script pour corriger l'encodage du fichier LaTeX
Remplace les caractères spéciaux français et emojis dans les commentaires
"""

import re

def fix_latex_file(input_file, output_file):
    """Fix UTF-8 encoding issues in LaTeX file"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapping des caractères problématiques dans les commentaires Python
    replacements = {
        # Accents français dans les commentaires
        '# Création': '# Creation',
        '# Chargement': '# Load',
        '# Génération': '# Generate',
        '# Encodage': '# Encode',
        '# Récupération': '# Get',
        '# Sauvegarde': '# Save',
        '# données': '# data',
        '# modèle': '# model',
        '# requête': '# query',
        '# résultats': '# results',
        '# Collection métriques': '# Metrics collection',
        '# Modèles Pydantic': '# Pydantic models',
        '# Moteur de recherche': '# Search engine',
        '# Construction index': '# Index building',
        '# Vérification setup': '# Setup verification',
        '# Nettoyage': '# Cleaning',
        
        # Emojis dans le code Streamlit
        '"⚙️ Configuration"': '"Configuration"',
        '"🔍 Rechercher"': '"Search"',
        'f"✓ {': 'f"Found {',
        '} résultats"': '} results"',
        '"Nombre de résultats"': '"Number of results"',
        'f"Résultat {': 'f"Result {',
        '"Entrez votre recherche :"': '"Enter your query:"',
        
        # Autres textes français
        'Suppression': 'Remove',
        'Normalisation': 'Normalize',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Écrire le fichier corrigé
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ File fixed: {output_file}")
    print(f"  Applied {len(replacements)} replacements")

if __name__ == "__main__":
    input_file = "rapport_recherche_semantique.tex"
    output_file = "rapport_recherche_semantique_fixed.tex"
    
    fix_latex_file(input_file, output_file)
    print("\nNow compile with:")
    print(f"  pdflatex {output_file}")
