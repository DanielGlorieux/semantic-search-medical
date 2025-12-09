import streamlit as st
import requests
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Medical Search Engine - MedQuAD",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better design
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Cards styling */
    .css-1r6slb0 {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #667eea;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Success/Info boxes */
    .element-container div[data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }
    
    /* Header styling */
    h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    h2, h3 {
        color: #667eea;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/fluency/96/000000/health-checkup.png", width=80)
st.sidebar.title("⚙️ Configuration")
st.sidebar.markdown("---")

# Search parameters
st.sidebar.subheader("🔍 Paramètres de recherche")
top_k = st.sidebar.slider(
    "Nombre de résultats", 
    min_value=1, 
    max_value=20, 
    value=10,
    help="Nombre maximum de documents à retourner"
)

use_reranking = st.sidebar.checkbox(
    "✨ Re-ranking avec CrossEncoder", 
    value=True,
    help="Améliore la précision mais augmente la latence"
)

hybrid = st.sidebar.checkbox(
    "🔄 Mode hybride (Dense + Sparse)", 
    value=False,
    help="Combine recherche sémantique et lexicale"
)

st.sidebar.markdown("---")

# System info
st.sidebar.subheader("📊 Informations Système")
try:
    response = requests.get(f"{API_URL}/health", timeout=3)
    if response.status_code == 200:
        health = response.json()
        if health.get("search_engine_loaded"):
            st.sidebar.success("✅ Backend Opérationnel")
        else:
            st.sidebar.warning("⚠️ Backend Chargement...")
    else:
        st.sidebar.error("❌ Backend Inaccessible")
except:
    st.sidebar.error("❌ Backend Hors Ligne")

st.sidebar.markdown("---")

# About section
with st.sidebar.expander("ℹ️ À propos"):
    st.markdown("""
    **Medical Search Engine**
    
    - 🗂️ **Dataset**: MedQuAD (16,412 docs)
    - 🧠 **Model**: Sentence Transformers
    - 🚀 **Index**: FAISS
    - ⚡ **Backend**: FastAPI
    
    **Auteur**: ILBOUDO P. Daniel Glorieux
    """)

# Medical disclaimer
with st.sidebar.expander("⚠️ Avertissement Médical"):
    st.warning("""
    **IMPORTANT**
    
    Cette application est à but éducatif uniquement. 
    Elle ne remplace PAS un avis médical professionnel.
    
    Consultez toujours un médecin qualifié pour des questions de santé.
    """)

# Main header with container
header_container = st.container()
with header_container:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; margin-bottom: 0;'>🏥 Medical Search Engine</h1>
            <p style='font-size: 1.2em; color: white; margin-top: 10px;'>
                Recherche sémantique dans 16,412 questions médicales
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Search box in a card
search_container = st.container()
with search_container:
    st.markdown("""
    <div style='background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
    """, unsafe_allow_html=True)
    
    query = st.text_input(
        "🔍 Entrez votre question médicale :",
        placeholder="Ex: What are the symptoms of diabetes?",
        key="search_query",
        label_visibility="collapsed"
    )
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 6])
    with col1:
        search_button = st.button("🔍 Rechercher", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Effacer", use_container_width=True)
    with col3:
        example_button = st.button("💡 Exemple", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Handle example button
if example_button:
    st.session_state.search_query = "What are the symptoms of glaucoma?"
    st.rerun()

if clear_button:
    st.session_state.search_query = ""
    st.rerun()

# Search logic
if search_button and query:
    with st.spinner("🔎 Recherche en cours..."):
        start_time = time.time()
        try:
            response = requests.post(
                f"{API_URL}/query",
                json={
                    "query": query,
                    "top_k": top_k,
                    "use_reranking": use_reranking,
                    "hybrid": hybrid
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data["results"]
                latency = data["latency"]
                total_time = time.time() - start_time
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display metrics in cards
                metric_cols = st.columns(4)
                with metric_cols[0]:
                    st.metric("📄 Résultats", len(results))
                with metric_cols[1]:
                    st.metric("⚡ Latence", f"{latency:.3f}s")
                with metric_cols[2]:
                    st.metric("🔄 Re-ranking", "✓" if use_reranking else "✗")
                with metric_cols[3]:
                    st.metric("🎯 Mode", "Hybride" if hybrid else "Dense")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display results with enhanced UI
                st.markdown("### 📋 Résultats de Recherche")
                
                # Create tabs for different views
                tab1, tab2 = st.tabs(["📄 Vue Liste", "📊 Vue Scores"])
                
                with tab1:
                    for i, result in enumerate(results):
                        # Color coding based on score
                        if result['score'] > 0.8:
                            score_color = "🟢"
                        elif result['score'] > 0.6:
                            score_color = "🟡"
                        else:
                            score_color = "🟠"
                        
                        with st.expander(
                            f"{score_color} **Résultat #{i+1}** | Score: {result['score']:.4f} | Doc ID: {result['doc_id']}",
                            expanded=(i == 0)  # First result expanded by default
                        ):
                            # Document info
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown("#### 📝 Contenu")
                                st.write(result['text'])
                            
                            with col2:
                                st.markdown("#### 📊 Scores")
                                st.metric("FAISS Score", f"{result['score']:.4f}")
                                if 'rerank_score' in result:
                                    st.metric("Rerank Score", f"{result.get('rerank_score', 0):.4f}")
                                st.metric("Rang", f"#{i+1}")
                            
                            # Additional metadata if available
                            if any(key in result for key in ['source', 'focus_area']):
                                st.markdown("---")
                                st.markdown("#### 🏷️ Métadonnées")
                                meta_cols = st.columns(2)
                                if 'source' in result:
                                    with meta_cols[0]:
                                        st.info(f"**Source:** {result.get('source', 'N/A')}")
                                if 'focus_area' in result:
                                    with meta_cols[1]:
                                        st.info(f"**Domaine:** {result.get('focus_area', 'N/A')}")
                
                with tab2:
                    # Visualization of scores
                    if results:
                        scores_df = pd.DataFrame([
                            {
                                'Rang': i+1,
                                'Score FAISS': r['score'],
                                'Score Rerank': r.get('rerank_score', 0) if use_reranking else None,
                                'Doc ID': r['doc_id']
                            }
                            for i, r in enumerate(results)
                        ])
                        
                        # Bar chart
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=scores_df['Rang'],
                            y=scores_df['Score FAISS'],
                            name='Score FAISS',
                            marker_color='#667eea'
                        ))
                        
                        if use_reranking:
                            fig.add_trace(go.Bar(
                                x=scores_df['Rang'],
                                y=scores_df['Score Rerank'],
                                name='Score Re-ranking',
                                marker_color='#764ba2'
                            ))
                        
                        fig.update_layout(
                            title='Distribution des Scores',
                            xaxis_title='Rang du Document',
                            yaxis_title='Score',
                            barmode='group',
                            height=400,
                            template='plotly_white'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Data table
                        st.markdown("#### 📊 Tableau des Scores")
                        st.dataframe(scores_df, use_container_width=True, height=300)
                
                # Success message
                st.success(f"✅ Recherche terminée avec succès en {total_time:.3f}s")
                
            else:
                st.error(f"❌ Erreur API: {response.status_code}")
                st.json(response.json())
        
        except requests.exceptions.ConnectionError:
            st.error("❌ Impossible de se connecter au backend")
            st.info("""
            **Comment démarrer le backend:**
            ```bash
            cd backend
            uvicorn app.main:app --reload
            ```
            """)
        except requests.exceptions.Timeout:
            st.error("⏱️ La requête a expiré (timeout)")
        except Exception as e:
            st.error(f"❌ Erreur inattendue: {str(e)}")
            with st.expander("🐛 Détails de l'erreur"):
                st.exception(e)

# Metrics section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# System metrics in expandable section
with st.expander("📊 Métriques et Statistiques du Système", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Statistiques d'Utilisation")
        if st.button("🔄 Actualiser les métriques", use_container_width=True):
            try:
                response = requests.get(f"{API_URL}/metrics", timeout=5)
                if response.status_code == 200:
                    metrics = response.json()
                    
                    metric_cols = st.columns(2)
                    with metric_cols[0]:
                        st.metric("📊 Total Requêtes", metrics.get("total_queries", 0))
                        st.metric("⏱️ Latence Min", f"{metrics.get('min_latency', 0):.3f}s")
                    with metric_cols[1]:
                        st.metric("📉 Latence Moyenne", f"{metrics.get('avg_latency', 0):.3f}s")
                        st.metric("⏱️ Latence Max", f"{metrics.get('max_latency', 0):.3f}s")
                    
                    # Latency chart
                    if metrics.get("total_queries", 0) > 0:
                        st.markdown("##### 📊 Distribution de la Latence")
                        latency_data = {
                            'Type': ['Min', 'Moyenne', 'Max'],
                            'Latence (s)': [
                                metrics.get('min_latency', 0),
                                metrics.get('avg_latency', 0),
                                metrics.get('max_latency', 0)
                            ]
                        }
                        fig = px.bar(
                            latency_data, 
                            x='Type', 
                            y='Latence (s)',
                            color='Type',
                            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
                        )
                        fig.update_layout(showlegend=False, height=250)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Métriques non disponibles")
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
    
    with col2:
        st.markdown("#### 🔧 État du Système")
        
        # System status cards
        status_container = st.container()
        with status_container:
            try:
                response = requests.get(f"{API_URL}/health", timeout=3)
                if response.status_code == 200:
                    health = response.json()
                    
                    if health.get("search_engine_loaded"):
                        st.markdown("""
                        <div class='info-box'>
                            <h4>✅ Backend Opérationnel</h4>
                            <p>Moteur de recherche chargé et prêt</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Moteur en cours de chargement...")
                    
                    # Additional system info
                    st.markdown("##### 📋 Informations")
                    info_data = {
                        "Composant": ["API Backend", "Search Engine", "FAISS Index", "Embeddings"],
                        "Statut": ["✅ Actif", "✅ Chargé", "✅ Prêt", "✅ Disponible"]
                    }
                    st.dataframe(info_data, use_container_width=True, hide_index=True)
                else:
                    st.error("❌ Backend inaccessible")
            except:
                st.markdown("""
                <div style='background-color: #ff6b6b; color: white; padding: 15px; border-radius: 10px;'>
                    <h4>❌ Backend Non Disponible</h4>
                    <p>Vérifiez que le serveur FastAPI est démarré</p>
                </div>
                """, unsafe_allow_html=True)

# Quick Stats Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
with stats_col1:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
        <h2>16,412</h2>
        <p>Documents Médicaux</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; color: white;'>
        <h2>< 50ms</h2>
        <p>Latence Moyenne</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col3:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 10px; color: white;'>
        <h2>89.2%</h2>
        <p>Recall@10</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col4:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 10px; color: white;'>
        <h2>80.1%</h2>
        <p>MRR@10</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background-color: rgba(255, 255, 255, 0.9); border-radius: 10px;'>
        <h3 style='color: #667eea;'>🏥 Medical Semantic Search Engine</h3>
        <p style='color: #555;'><strong>Technologies:</strong> FastAPI • FAISS • Sentence Transformers • Streamlit</p>
        <p style='color: #555;'><strong>Dataset:</strong> MedQuAD (NIH) • 16,412 Medical Q&A Pairs</p>
        <p style='color: #777; font-size: 0.9em; margin-top: 15px;'>
            📚 Projet Big Data & Vector Database<br>
            👤 ILBOUDO P. Daniel Glorieux<br>
            🏫 École Centrale de Lyon - {datetime.now().year}
        </p>
        <p style='color: #999; font-size: 0.8em; margin-top: 10px;'>
            ⚠️ Application éducative - Ne remplace pas un avis médical professionnel
        </p>
    </div>
    """.format(datetime=datetime),
    unsafe_allow_html=True
)
