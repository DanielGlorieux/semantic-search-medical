from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging

from app.services.search_engine import SemanticSearchEngine
from app.services.metrics import MetricsCollector
from app.services.rag_service import RAGService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Semantic Search API",
    description="API de recherche sémantique avec FAISS et embeddings",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_engine = None
metrics_collector = MetricsCollector()
rag_service = None

class QueryRequest(BaseModel):
    query: str
    top_k: int = 10
    use_reranking: bool = True
    hybrid: bool = False
    use_rag: bool = False  # Nouveau paramètre pour activer RAG

class SearchResult(BaseModel):
    doc_id: str
    text: str
    score: float
    rank: int

class QueryResponse(BaseModel):
    query: str
    results: List[SearchResult]
    latency: float
    total_docs: int
    rag_response: Optional[str] = None  # Réponse générée par RAG
    rag_summary: Optional[str] = None  # Résumé des documents

@app.on_event("startup")
async def startup_event():
    global search_engine, rag_service
    logger.info("Loading search engine...")
    try:
        search_engine = SemanticSearchEngine()
        search_engine.load()
        logger.info("Search engine loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load search engine: {e}")
    
    logger.info("Initializing RAG service with Gemini...")
    try:
        rag_service = RAGService()
        if rag_service.is_available():
            logger.info("RAG service initialized successfully")
        else:
            logger.warning("RAG service initialized but Gemini API not configured")
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")

@app.get("/")
async def root():
    return {
        "message": "Semantic Search API",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if search_engine is None:
        raise HTTPException(status_code=503, detail="Search engine not ready")
    
    try:
        results, latency = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            use_reranking=request.use_reranking,
            hybrid=request.hybrid
        )
        
        metrics_collector.add_query(request.query, latency)
        
        search_results = [
            SearchResult(
                doc_id=r["doc_id"],
                text=r["text"],
                score=r["score"],
                rank=i+1
            )
            for i, r in enumerate(results)
        ]
        
        # Générer une réponse RAG si demandé
        rag_response_text = None
        rag_summary_text = None
        
        if request.use_rag and rag_service and rag_service.is_available():
            logger.info("Generating RAG response...")
            rag_result = rag_service.generate_response(
                query=request.query,
                retrieved_docs=results,
                max_docs=3
            )
            rag_response_text = rag_result.get("response")
            
            # Générer aussi un résumé court
            if len(results) > 0:
                rag_summary_text = rag_service.generate_summary(results, top_n=3)
        
        return QueryResponse(
            query=request.query,
            results=search_results,
            latency=latency,
            total_docs=len(results),
            rag_response=rag_response_text,
            rag_summary=rag_summary_text
        )
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/docs/{doc_id}")
async def get_document(doc_id: str):
    if search_engine is None:
        raise HTTPException(status_code=503, detail="Search engine not ready")
    
    doc = search_engine.get_document(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return doc

@app.get("/metrics")
async def get_metrics():
    return metrics_collector.get_summary()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "search_engine_loaded": search_engine is not None,
        "rag_service_available": rag_service is not None and rag_service.is_available()
    }

@app.post("/rag/answer")
async def rag_answer(request: QueryRequest):
    """Endpoint dédié pour obtenir uniquement la réponse RAG"""
    if search_engine is None:
        raise HTTPException(status_code=503, detail="Search engine not ready")
    
    if rag_service is None or not rag_service.is_available():
        raise HTTPException(status_code=503, detail="RAG service not available")
    
    try:
        # Rechercher les documents pertinents
        results, latency = search_engine.search(
            query=request.query,
            top_k=request.top_k,
            use_reranking=request.use_reranking,
            hybrid=request.hybrid
        )
        
        # Générer la réponse RAG
        rag_result = rag_service.generate_response(
            query=request.query,
            retrieved_docs=results,
            max_docs=5
        )
        
        return {
            "query": request.query,
            "answer": rag_result.get("response"),
            "sources": rag_result.get("sources_used"),
            "num_sources": rag_result.get("num_sources"),
            "latency": latency,
            "error": rag_result.get("error")
        }
        
    except Exception as e:
        logger.error(f"RAG answer error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
