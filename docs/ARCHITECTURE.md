# Architecture du Système

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        Interface Utilisateur                     │
│                    (Streamlit / React + FastAPI)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend API (FastAPI)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐    │
│  │   Routes     │  │   Services   │  │   Metrics         │    │
│  │  /query      │─▶│  SearchEngine│  │   Collector       │    │
│  │  /docs/{id}  │  │  Metrics     │  │                   │    │
│  │  /metrics    │  └──────────────┘  └───────────────────┘    │
│  └──────────────┘                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                          IA Pipeline                             │
│  ┌────────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ SentenceT      │  │    FAISS     │  │  CrossEncoder     │  │
│  │ Encoder        │─▶│    Index     │─▶│   Reranker        │  │
│  │ (Embeddings)   │  │  (Search)    │  │  (Optional)       │  │
│  └────────────────┘  └──────────────┘  └───────────────────┘  │
│                                                                  │
│  ┌────────────────┐                                             │
│  │     BM25       │  (Hybrid Search - Optional)                 │
│  │   (Sparse)     │                                             │
│  └────────────────┘                                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Base de Données / Stockage                    │
│  ┌────────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Documents     │  │  Embeddings  │  │   FAISS Index     │  │
│  │  (CSV/DB)      │  │   (.npy)     │  │    (.faiss)       │  │
│  │  + Metadata    │  │              │  │                   │  │
│  └────────────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Composants Principaux

### 1. Interface Utilisateur

#### Option A : Streamlit
- Application Python simple
- Interface interactive rapide
- Visualisations intégrées

#### Option B : React + FastAPI
- Frontend React moderne
- Backend API REST séparé
- Plus de flexibilité

### 2. Backend API (FastAPI)

#### Endpoints principaux:
- `POST /query` : Recherche de documents
- `GET /docs/{id}` : Récupération d'un document
- `GET /metrics` : Métriques de performance
- `GET /health` : Vérification de santé

#### Services:
- **SearchEngine** : Gestion de la recherche
- **MetricsCollector** : Collection des métriques

### 3. Pipeline IA

#### Encodage:
- **SentenceTransformer** : Conversion texte → embeddings
- Modèle : `all-MiniLM-L6-v2` (384 dimensions)

#### Recherche:
- **FAISS Index** : Recherche vectorielle rapide
- Types d'index : FlatIP, IVFFlat, IVFPQ

#### Re-ranking (optionnel):
- **CrossEncoder** : Amélioration du classement
- Modèle : `ms-marco-MiniLM-L-6-v2`

#### Recherche hybride (optionnel):
- **BM25** : Recherche lexicale
- Combinaison avec recherche dense

### 4. Stockage

#### Documents:
- Format : CSV / Base de données
- Champs : doc_id, text, metadata

#### Embeddings:
- Format : NumPy arrays (.npy)
- Dimensions : (n_docs, embedding_dim)

#### Index FAISS:
- Format : .faiss
- Optimisé pour recherche rapide

## Flux de Données

### Indexation (Offline)

```
Raw Documents → Cleaning → Tokenization → Embedding → FAISS Index
     (CSV)         ↓          ↓              ↓            ↓
                Processed   Normalized    Vectors      Indexed
                  Docs       Tokens      (384-dim)    (Searchable)
```

### Recherche (Online)

```
User Query → Encode → FAISS Search → Top-K Results → Reranking → Final Results
    ↓          ↓          ↓               ↓              ↓            ↓
  "text"   [0.1, ...]  Similarity    [doc1, doc2...]  Reordered   Displayed
                       Scores
```

## Technologies Utilisées

### Backend:
- **FastAPI** : Framework web moderne
- **Python 3.8+** : Langage principal

### ML/AI:
- **Sentence Transformers** : Encodage sémantique
- **FAISS** : Recherche vectorielle
- **PyTorch** : Framework ML

### Data Processing:
- **Pandas** : Manipulation de données
- **NumPy** : Calculs numériques
- **Scikit-learn** : Outils ML

### Frontend:
- **Streamlit** : Interface rapide
- **React** : Alternative moderne

### Visualisation:
- **Matplotlib** : Graphiques
- **Plotly** : Graphiques interactifs
- **UMAP/t-SNE** : Réduction de dimensionnalité

## Optimisations Possibles

### 1. Performance:
- Utiliser IndexIVFPQ pour compression
- Caching des requêtes fréquentes
- Batch processing

### 2. Qualité:
- Fine-tuning du modèle d'encodage
- Optimisation des poids hybrides
- Filtrage par metadata

### 3. Scalabilité:
- Sharding de l'index FAISS
- Load balancing
- Distributed search

## Métriques de Performance

### Qualité:
- **Recall@K** : Couverture
- **MRR@K** : Pertinence
- **NDCG@K** : Classement

### Vitesse:
- **Latence moyenne** : Temps de réponse
- **Throughput** : Requêtes/seconde
- **P95, P99** : Percentiles

### Ressources:
- **Mémoire** : Usage RAM
- **CPU/GPU** : Utilisation
- **Stockage** : Espace disque
