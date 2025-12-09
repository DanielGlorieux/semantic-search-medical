import pytest
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.services.search_engine import SemanticSearchEngine

@pytest.fixture
def search_engine():
    """Fixture for search engine"""
    engine = SemanticSearchEngine()
    return engine

def test_encode_query(search_engine):
    """Test query encoding"""
    query = "test query"
    embedding = search_engine.encode_query(query)
    
    assert embedding is not None
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape[1] == 384  # MiniLM dimension

def test_search_returns_results(search_engine):
    """Test that search returns results"""
    # This test requires loaded index
    # Implement based on your setup
    pass

def test_get_document(search_engine):
    """Test document retrieval"""
    # Implement based on your setup
    pass

def test_compute_metrics(search_engine):
    """Test metrics computation"""
    # Implement based on your setup
    pass
