"""
Script pour convertir le dataset MedQuAD de Kaggle au format attendu
Format source: question,answer,source,focus_area
Format cible: doc_id,text
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_medquad_to_corpus(input_path: str, output_path: str, mode: str = "qa"):
    """
    Convertir MedQuAD au format corpus standard
    
    Args:
        input_path: Chemin vers le fichier MedQuAD
        output_path: Chemin de sortie
        mode: 
            - "qa": Combine question + answer
            - "answer": Utilise seulement answer
            - "question": Utilise seulement question
            - "full": Inclut tous les champs
    """
    logger.info(f"Chargement de MedQuAD depuis {input_path}")
    
    # Charger le dataset
    df = pd.read_csv(input_path)
    logger.info(f"Dataset chargé: {len(df)} lignes")
    
    # Afficher les colonnes pour vérification
    logger.info(f"Colonnes trouvées: {df.columns.tolist()}")
    
    # Créer le texte selon le mode choisi
    if mode == "qa":
        # Combiner question et réponse (recommandé pour la recherche)
        df['text'] = "Question: " + df['question'].astype(str) + "\n\nAnswer: " + df['answer'].astype(str)
        logger.info("Mode: Question + Answer combinés")
        
    elif mode == "answer":
        # Utiliser seulement les réponses
        df['text'] = df['answer'].astype(str)
        logger.info("Mode: Réponses seulement")
        
    elif mode == "question":
        # Utiliser seulement les questions
        df['text'] = df['question'].astype(str)
        logger.info("Mode: Questions seulement")
        
    elif mode == "full":
        # Inclure tous les champs avec métadonnées
        df['text'] = (
            "Question: " + df['question'].astype(str) + "\n\n" +
            "Answer: " + df['answer'].astype(str) + "\n\n" +
            "Source: " + df['source'].astype(str) + "\n" +
            "Focus Area: " + df['focus_area'].astype(str)
        )
        logger.info("Mode: Tous les champs")
    else:
        raise ValueError(f"Mode inconnu: {mode}. Utilisez 'qa', 'answer', 'question', ou 'full'")
    
    # Créer doc_id
    df['doc_id'] = df.index.astype(str)
    
    # Nettoyer les valeurs manquantes
    df['text'] = df['text'].fillna('')
    
    # Filtrer les textes vides
    initial_count = len(df)
    df = df[df['text'].str.strip() != '']
    final_count = len(df)
    logger.info(f"Documents après filtrage: {final_count} (supprimés: {initial_count - final_count})")
    
    # Sélectionner les colonnes finales
    result = df[['doc_id', 'text']].copy()
    
    # Optionnel: garder les métadonnées dans des colonnes séparées
    if 'source' in df.columns:
        result['source'] = df['source']
    if 'focus_area' in df.columns:
        result['focus_area'] = df['focus_area']
    
    # Créer le dossier de sortie si nécessaire
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder
    result.to_csv(output_path, index=False)
    logger.info(f"✓ Corpus converti sauvegardé: {output_path}")
    logger.info(f"  - {len(result)} documents")
    logger.info(f"  - Colonnes: {result.columns.tolist()}")
    
    # Afficher quelques statistiques
    avg_length = result['text'].str.len().mean()
    logger.info(f"  - Longueur moyenne du texte: {avg_length:.0f} caractères")
    
    return result

def preview_conversion(input_path: str, n: int = 3):
    """Prévisualiser la conversion"""
    logger.info("=== PRÉVISUALISATION ===")
    df = pd.read_csv(input_path)
    
    for i in range(min(n, len(df))):
        logger.info(f"\n--- Document {i+1} ---")
        logger.info(f"Question: {df.iloc[i]['question'][:100]}...")
        logger.info(f"Answer: {df.iloc[i]['answer'][:100]}...")
        logger.info(f"Source: {df.iloc[i]['source']}")
        logger.info(f"Focus Area: {df.iloc[i]['focus_area']}")

if __name__ == "__main__":
    # Chemins
    input_file = "data/raw/medquad.csv"  # Votre fichier MedQuAD
    output_file = "data/raw/corpus.csv"
    
    # Prévisualiser
    preview_conversion(input_file, n=2)
    
    # Convertir (choisir le mode)
    # Mode "qa" est recommandé pour avoir question + réponse
    convert_medquad_to_corpus(
        input_path=input_file,
        output_path=output_file,
        mode="qa"  # Options: "qa", "answer", "question", "full"
    )
    
    logger.info("\n✓ Conversion terminée!")
    logger.info(f"Fichier créé: {output_file}")
    logger.info("\nProchaine étape:")
    logger.info("  python scripts/preprocessing/clean_data.py")
