"""
Script pour s'assurer que les doc_id sont des strings dans le CSV
"""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_doc_ids():
    """Convertir tous les doc_id en strings"""
    
    project_root = Path(__file__).parent.parent
    docs_file = project_root / "data" / "processed" / "docs.csv"
    
    if not docs_file.exists():
        logger.error(f"Fichier non trouvé: {docs_file}")
        return False
    
    logger.info(f"Chargement de {docs_file}")
    df = pd.read_csv(docs_file)
    
    # Vérifier le type actuel
    logger.info(f"Type actuel de doc_id: {df['doc_id'].dtype}")
    logger.info(f"Exemple de doc_id: {df['doc_id'].head(3).tolist()}")
    
    # Convertir en string
    df['doc_id'] = df['doc_id'].astype(str)
    
    # Sauvegarder
    df.to_csv(docs_file, index=False)
    logger.info(f"✓ Fichier mis à jour avec doc_id en string")
    logger.info(f"Type après conversion: {df['doc_id'].dtype}")
    logger.info(f"Exemple après: {df['doc_id'].head(3).tolist()}")
    
    return True

if __name__ == "__main__":
    success = fix_doc_ids()
    if success:
        print("\n✅ doc_id convertis en strings!")
        print("Relancez le backend maintenant:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
    else:
        print("\n❌ Erreur lors de la conversion")
