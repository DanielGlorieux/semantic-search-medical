import pandas as pd
import numpy as np
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_faiss_index():
    """Build FAISS index from documents"""
    
    # Paths
    data_dir = Path("data/processed")
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Load documents
    logger.info("Loading documents...")
    docs_path = data_dir / "docs.csv"
    if not docs_path.exists():
        raise FileNotFoundError(f"Documents file not found: {docs_path}")
    
    docs = pd.read_csv(docs_path)
    logger.info(f"Loaded {len(docs)} documents")
    
    # Load encoder
    logger.info("Loading sentence transformer...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Generate embeddings
    logger.info("Generating embeddings...")
    texts = docs['text'].tolist()
    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True
    )
    embeddings = embeddings.astype('float32')
    
    # Save embeddings
    embeddings_path = models_dir / "embeddings.npy"
    np.save(str(embeddings_path), embeddings)
    logger.info(f"Embeddings saved to {embeddings_path}")
    
    # Build FAISS index
    logger.info("Building FAISS index...")
    dimension = embeddings.shape[1]
    
    # Use IndexFlatIP for inner product (cosine similarity with normalized vectors)
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    logger.info(f"Index built with {index.ntotal} vectors")
    
    # Save index
    index_path = models_dir / "index.faiss"
    faiss.write_index(index, str(index_path))
    logger.info(f"Index saved to {index_path}")
    
    logger.info("✓ Indexing completed successfully!")

if __name__ == "__main__":
    build_faiss_index()
