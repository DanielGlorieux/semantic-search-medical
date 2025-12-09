"""
Script pour vérifier que tout est prêt avant de lancer l'application
"""

from pathlib import Path
import sys

def check_files():
    """Vérifier que tous les fichiers nécessaires existent"""
    
    print("\n" + "="*60)
    print("🔍 VÉRIFICATION DE L'INSTALLATION")
    print("="*60 + "\n")
    
    project_root = Path(__file__).parent.parent
    errors = []
    warnings = []
    
    # 1. Vérifier les données
    print("📊 Données:")
    docs_file = project_root / "data" / "processed" / "docs.csv"
    if docs_file.exists():
        import pandas as pd
        df = pd.read_csv(docs_file)
        print(f"  ✅ docs.csv trouvé ({len(df)} documents)")
        if 'text' not in df.columns:
            errors.append("La colonne 'text' est manquante dans docs.csv")
        if 'doc_id' not in df.columns:
            errors.append("La colonne 'doc_id' est manquante dans docs.csv")
    else:
        errors.append(f"Fichier manquant: {docs_file}")
        print(f"  ❌ docs.csv manquant")
    
    # 2. Vérifier l'index FAISS
    print("\n🤖 Index FAISS:")
    index_file = project_root / "models" / "index.faiss"
    if index_file.exists():
        print(f"  ✅ index.faiss trouvé ({index_file.stat().st_size / 1024 / 1024:.1f} MB)")
    else:
        errors.append("Index FAISS manquant - Exécutez: python scripts/build_index.py")
        print(f"  ❌ index.faiss manquant")
    
    # 3. Vérifier les embeddings
    print("\n📐 Embeddings:")
    embeddings_file = project_root / "models" / "embeddings.npy"
    if embeddings_file.exists():
        import numpy as np
        emb = np.load(embeddings_file)
        print(f"  ✅ embeddings.npy trouvé ({emb.shape[0]} docs, {emb.shape[1]} dim)")
    else:
        warnings.append("embeddings.npy manquant (sera créé par build_index.py)")
        print(f"  ⚠️  embeddings.npy manquant")
    
    # 4. Vérifier les dépendances
    print("\n📦 Dépendances:")
    try:
        import fastapi
        print(f"  ✅ FastAPI installé")
    except ImportError:
        errors.append("FastAPI non installé")
        print(f"  ❌ FastAPI manquant")
    
    try:
        import sentence_transformers
        print(f"  ✅ Sentence Transformers installé")
    except ImportError:
        errors.append("Sentence Transformers non installé")
        print(f"  ❌ Sentence Transformers manquant")
    
    try:
        import faiss
        print(f"  ✅ FAISS installé")
    except ImportError:
        errors.append("FAISS non installé")
        print(f"  ❌ FAISS manquant")
    
    try:
        import streamlit
        print(f"  ✅ Streamlit installé")
    except ImportError:
        warnings.append("Streamlit non installé")
        print(f"  ⚠️  Streamlit manquant")
    
    # Résumé
    print("\n" + "="*60)
    if errors:
        print("❌ ERREURS TROUVÉES:")
        for error in errors:
            print(f"  • {error}")
        print("\n🔧 ACTIONS REQUISES:")
        if any("index.faiss" in e for e in errors):
            print("  1. Exécuter: python scripts/build_index.py")
        if any("docs.csv" in e for e in errors):
            print("  1. Placer vos données dans data/raw/medquad.csv")
            print("  2. Exécuter: python scripts/preprocessing/convert_medquad.py")
            print("  3. Exécuter: python scripts/preprocessing/clean_data.py")
        if any("installé" in e for e in errors):
            print("  1. Exécuter: pip install -r backend/requirements.txt")
    elif warnings:
        print("⚠️  AVERTISSEMENTS:")
        for warning in warnings:
            print(f"  • {warning}")
    else:
        print("✅ TOUT EST PRÊT!")
        print("\n🚀 Vous pouvez lancer l'application:")
        print("  Terminal 1: cd backend && uvicorn app.main:app --reload")
        print("  Terminal 2: streamlit run frontend/app_streamlit.py")
    
    print("="*60 + "\n")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = check_files()
    sys.exit(0 if success else 1)
