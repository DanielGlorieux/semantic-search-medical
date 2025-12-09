import numpy as np
import faiss
import pickle
import time
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer, CrossEncoder
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class SemanticSearchEngine:
    def __init__(self, config_path: Optional[str] = None):
        self.model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.encoder = None
        self.cross_encoder = None
        self.index = None
        self.doc_ids = None
        self.documents = None
        self.embeddings = None
        
        # Get project root (go up from backend/app/services to project root)
        project_root = Path(__file__).parent.parent.parent.parent
        self.models_dir = project_root / "models"
        self.data_dir = project_root / "data" / "processed"
        
    def load(self):
        """Load all necessary models and data"""
        logger.info("Loading sentence transformer...")
        self.encoder = SentenceTransformer(self.model_name)
        
        logger.info("Loading cross-encoder for reranking...")
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
        logger.info("Loading FAISS index...")
        index_path = self.models_dir / "index.faiss"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
        else:
            logger.warning("FAISS index not found. Please run indexing first.")
        
        logger.info("Loading documents...")
        docs_path = self.data_dir / "docs.csv"
        if docs_path.exists():
            # Force doc_id to be string
            self.documents = pd.read_csv(docs_path)
            self.documents['doc_id'] = self.documents['doc_id'].astype(str)
            self.doc_ids = self.documents['doc_id'].tolist()
            logger.info(f"Loaded {len(self.documents)} documents")
        else:
            logger.warning("Documents file not found.")
        
        logger.info("Loading embeddings...")
        embeddings_path = self.models_dir / "embeddings.npy"
        if embeddings_path.exists():
            self.embeddings = np.load(str(embeddings_path))
        
        logger.info("Search engine loaded successfully")
    
    def encode_query(self, query: str) -> np.ndarray:
        """Encode a query into an embedding"""
        embedding = self.encoder.encode([query], normalize_embeddings=True)
        return embedding.astype('float32')
    
    def search(
        self, 
        query: str, 
        top_k: int = 10, 
        use_reranking: bool = True,
        hybrid: bool = False
    ) -> Tuple[List[Dict], float]:
        """Search for documents matching the query"""
        start_time = time.time()
        
        # Encode query
        query_embedding = self.encode_query(query)
        
        # Search in FAISS
        k = top_k * 3 if use_reranking else top_k
        distances, indices = self.index.search(query_embedding, k)
        
        # Get results
        results = []
        for i, (idx, score) in enumerate(zip(indices[0], distances[0])):
            if idx < len(self.doc_ids):
                doc_id = self.doc_ids[idx]
                doc_row = self.documents[self.documents['doc_id'] == doc_id].iloc[0]
                result = {
                    'doc_id': str(doc_id),  # Ensure doc_id is always string
                    'text': str(doc_row['text']),
                    'score': float(score),
                    'rank': i + 1
                }
                # Add optional metadata if available
                if 'source' in doc_row:
                    result['source'] = str(doc_row['source'])
                if 'focus_area' in doc_row:
                    result['focus_area'] = str(doc_row['focus_area'])
                    
                results.append(result)
        
        # Reranking with CrossEncoder
        if use_reranking and len(results) > 0:
            pairs = [[query, r['text']] for r in results]
            rerank_scores = self.cross_encoder.predict(pairs)
            
            for i, score in enumerate(rerank_scores):
                results[i]['rerank_score'] = float(score)
            
            results = sorted(results, key=lambda x: x['rerank_score'], reverse=True)[:top_k]
            
            for i, r in enumerate(results):
                r['rank'] = i + 1
        else:
            results = results[:top_k]
        
        latency = time.time() - start_time
        
        return results, latency
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Retrieve a specific document by ID"""
        doc_row = self.documents[self.documents['doc_id'] == doc_id]
        if len(doc_row) == 0:
            return None
        
        return doc_row.iloc[0].to_dict()
    
    def compute_metrics(self, queries: List[str], qrels: Dict, k: int = 10) -> Dict:
        """Compute evaluation metrics (Recall@K, MRR@K)"""
        recalls = []
        mrrs = []
        
        for query_id, query in queries:
            if query_id not in qrels:
                continue
            
            relevant_docs = set(qrels[query_id])
            results, _ = self.search(query, top_k=k, use_reranking=False)
            retrieved_docs = [r['doc_id'] for r in results]
            
            # Recall@K
            retrieved_relevant = len(set(retrieved_docs) & relevant_docs)
            recall = retrieved_relevant / len(relevant_docs) if relevant_docs else 0
            recalls.append(recall)
            
            # MRR@K
            mrr = 0
            for i, doc_id in enumerate(retrieved_docs):
                if doc_id in relevant_docs:
                    mrr = 1 / (i + 1)
                    break
            mrrs.append(mrr)
        
        return {
            'recall@10': np.mean(recalls),
            'mrr@10': np.mean(mrrs)
        }
