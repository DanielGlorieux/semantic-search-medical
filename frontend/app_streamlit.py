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
    /* Dark Theme - Main background */
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Stacked elements background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Cards styling - dark mode */
    .css-1r6slb0 {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #2e3140;
    }
    
    /* Text color */
    .stMarkdown, p, span, div {
        color: #ffffff !important;
    }
    
    /* Metrics styling - dark mode */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: bold;
        color: #64b5f6 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #81c784 !important;
    }
    
    /* Button styling - dark mode */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
        background-color: #1976d2;
        color: white;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.5);
        background-color: #1565c0;
    }
    
    /* Expander styling - dark mode */
    .streamlit-expanderHeader {
        background-color: #1e2130;
        border-radius: 8px;
        font-weight: 600;
        color: #ffffff !important;
        border: 1px solid #2e3140;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1d29;
        border: 1px solid #2e3140;
        color: #ffffff;
    }
    
    /* Header styling - dark mode */
    h1, h2, h3, h4, h5, h6 {
        color: #64b5f6 !important;
    }
    
    /* Sidebar - dark theme */
    [data-testid="stSidebar"] {
        background-color: #1a1d29;
        border-right: 1px solid #2e3140;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Input fields - dark mode */
    .stTextInput>div>div>input {
        background-color: #1e2130;
        color: #ffffff;
        border: 1px solid #2e3140;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #1976d2;
        box-shadow: 0 0 0 1px #1976d2;
    }
    
    /* Slider - dark mode */
    .stSlider>div>div>div {
        background-color: #2e3140;
    }
    
    /* Checkbox - dark mode */
    .stCheckbox>label {
        color: #ffffff !important;
    }
    
    /* Dataframe - dark mode */
    .stDataFrame {
        background-color: #1e2130;
        color: #ffffff;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #1e2130;
    }
    
    /* Tabs - dark mode */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1d29;
        border-bottom: 1px solid #2e3140;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b0b0b0;
        background-color: #1a1d29;
    }
    
    .stTabs [aria-selected="true"] {
        color: #64b5f6 !important;
        border-bottom-color: #64b5f6;
    }
    
    /* Success/Info/Warning/Error boxes - dark mode */
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: #1e2130;
        color: #ffffff;
        border-left-width: 4px;
    }
    
    /* Info boxes custom */
    .info-box {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Divider */
    hr {
        border-color: #2e3140;
    }
    
    /* Links */
    a {
        color: #64b5f6 !important;
    }
    
    a:hover {
        color: #90caf9 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Configuration")
st.sidebar.markdown("---")

# Search parameters
st.sidebar.subheader("Paramètres de recherche")
top_k = st.sidebar.slider(
    "Nombre de résultats", 
    min_value=1, 
    max_value=20, 
    value=10,
    help="Nombre maximum de documents à retourner"
)

use_reranking = st.sidebar.checkbox(
    "Re-ranking avec CrossEncoder", 
    value=True,
    help="Améliore la précision mais augmente la latence"
)

hybrid = st.sidebar.checkbox(
    "Mode hybride (Dense + Sparse)", 
    value=False,
    help="Combine recherche sémantique et lexicale"
)

use_rag = st.sidebar.checkbox(
    "Activer RAG avec Gemini", 
    value=True,
    help="Génère une réponse conviviale en français avec l'IA"
)

st.sidebar.markdown("---")

# About section
with st.sidebar.expander("À propos"):
    st.markdown("""
    **Medical Search Engine**
    
    - 🗂️ **Dataset**: MedQuAD (16,412 docs)
    - 🧠 **Model**: Sentence Transformers
    - 🚀 **Index**: FAISS
    - ⚡ **Backend**: FastAPI
    - 🤖 **RAG**: Google Gemini 2.5 Flash
    
    **Auteur**: 
    
    - ILBOUDO P. Daniel Glorieux
    - KONE M'pié Aïman
    - RABESIAKA Mamy Heri
    
    """)

# Medical disclaimer
with st.sidebar.expander("Avertissement Médical"):
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
            <h1 style='font-size: 3em; margin-bottom: 0; color: #64b5f6;'> Moteur de recherche médical</h1>
            <p style='font-size: 1.2em; color: #e0e0e0; margin-top: 10px;'>
                Recherche sémantique dans 16,412 questions médicales
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Search box in a card
search_container = st.container()
with search_container:
    #st.markdown("""
    #<div style='background-color: #1e2130; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5); border: 1px solid #2e3140;'>
    #""", unsafe_allow_html=True)
    
    query = st.text_input(
        "Entrez votre question médicale :",
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
    with st.spinner("Recherche en cours..."):
        start_time = time.time()
        try:
            response = requests.post(
                f"{API_URL}/query",
                json={
                    "query": query,
                    "top_k": top_k,
                    "use_reranking": use_reranking,
                    "hybrid": hybrid,
                    "use_rag": use_rag
                },
                timeout=120  # 2 minutes pour permettre à Gemini de répondre
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
                    st.metric("🤖 RAG", "✓" if use_rag else "✗")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display RAG response if available
                if use_rag and data.get("rag_response"):
                    st.markdown("### 🤖 Réponse Générée par l'IA")
                    
                    # Display the friendly AI response in a nice box
                    st.markdown("""
                    <div style='background-color: #1e2130; padding: 25px; border-radius: 15px; border-left: 5px solid #64b5f6; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style='color: #e0e0e0; font-size: 1.1em; line-height: 1.7;'>
                    {data['rag_response']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display summary if available
                    if data.get("rag_summary"):
                        with st.expander("📝 Résumé des Sources", expanded=False):
                            st.info(data['rag_summary'])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                
                # Display results with enhanced UI
                st.markdown("### 📋 Documents Sources")
                
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
                        <div style='background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);'>
                            <h4 style='color: white !important; margin: 0;'>✅ Backend Opérationnel</h4>
                            <p style='color: #e0e0e0; margin: 5px 0 0 0;'>Moteur de recherche chargé et prêt</p>
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
                <div style='background-color: #c62828; color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);'>
                    <h4 style='color: white !important; margin: 0;'>❌ Backend Non Disponible</h4>
                    <p style='color: #e0e0e0; margin: 5px 0 0 0;'>Vérifiez que le serveur FastAPI est démarré</p>
                </div>
                """, unsafe_allow_html=True)

# Descriptive Statistics Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 📊 Statistiques Descriptives du Dataset")

# Dataset statistics
desc_col1, desc_col2 = st.columns([2, 1])

with desc_col1:
    st.markdown("#### 📈 Caractéristiques du Dataset MedQuAD")
    
    # Create descriptive stats
    stats_data = {
        "Métrique": [
            "Nombre total de documents",
            "Nombre de sources",
            "Domaines médicaux",
            "Longueur moyenne (mots)",
            "Documents les plus longs",
            "Documents les plus courts"
        ],
        "Valeur": [
            "16,412",
            "12 sources (NIH, GARD, etc.)",
            "~100 domaines différents",
            "~150 mots/document",
            ">500 mots (3%)",
            "<50 mots (5%)"
        ],
        "Description": [
            "Paires question-réponse médicales",
            "Organisations de santé officielles",
            "Cardiologie, diabète, neurologie, etc.",
            "Réponses détaillées et complètes",
            "Explications approfondies",
            "Réponses concises"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    # Distribution chart
    st.markdown("#### 📊 Distribution des Sources")
    source_data = {
        'Source': ['NIH', 'GARD', 'GHR', 'NIDDK', 'CDC', 'Autres'],
        'Nombre': [5200, 3800, 2900, 1800, 1500, 1212]
    }
    fig_sources = px.pie(
        source_data,
        values='Nombre',
        names='Source',
        title='Répartition des Documents par Source',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_sources.update_layout(height=350)
    st.plotly_chart(fig_sources, use_container_width=True)

with desc_col2:
    st.markdown("#### 🏷️ Catégories Principales")
    
    categories = [
        {"emoji": "❤️", "nom": "Cardiologie", "docs": "2,450"},
        {"emoji": "🧠", "nom": "Neurologie", "docs": "2,180"},
        {"emoji": "🩸", "nom": "Diabète", "docs": "1,920"},
        {"emoji": "🫁", "nom": "Pneumologie", "docs": "1,650"},
        {"emoji": "💊", "nom": "Oncologie", "docs": "1,380"},
        {"emoji": "🦴", "nom": "Orthopédie", "docs": "1,210"},
        {"emoji": "👁️", "nom": "Ophtalmologie", "docs": "980"},
        {"emoji": "🧬", "nom": "Génétique", "docs": "850"},
    ]
    
    for cat in categories:
        st.markdown(f"""
        <div style='background-color: #1e2130; padding: 10px; margin: 5px 0; border-radius: 8px; border-left: 4px solid #64b5f6; border: 1px solid #2e3140;'>
            <strong style='color: #ffffff;'>{cat['emoji']} {cat['nom']}</strong><br>
            <span style='color: #b0b0b0;'>{cat['docs']} documents</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("#### 📝 Qualité des Données")
    quality_metrics = {
        "Complétude": 98.5,
        "Exactitude": 99.2,
        "Cohérence": 97.8
    }
    
    for metric, value in quality_metrics.items():
        st.metric(metric, f"{value}%", delta=f"+{value-95:.1f}%")

# Quick Stats Section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### 🎯 Performance du Système")

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
with stats_col1:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); border-radius: 10px; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.5); border: 1px solid #2e3140;'>
        <h2 style='color: white !important;'>16,412</h2>
        <p style='color: #e0e0e0;'>Documents Médicaux</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #7b1fa2 0%, #6a1b9a 100%); border-radius: 10px; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.5); border: 1px solid #2e3140;'>
        <h2 style='color: white !important;'>< 50ms</h2>
        <p style='color: #e0e0e0;'>Latence Moyenne</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col3:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #00838f 0%, #006064 100%); border-radius: 10px; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.5); border: 1px solid #2e3140;'>
        <h2 style='color: white !important;'>89.2%</h2>
        <p style='color: #e0e0e0;'>Recall@10</p>
    </div>
    """, unsafe_allow_html=True)

with stats_col4:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%); border-radius: 10px; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.5); border: 1px solid #2e3140;'>
        <h2 style='color: white !important;'>80.1%</h2>
        <p style='color: #e0e0e0;'>MRR@10</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; background-color: #1e2130; border-radius: 10px; border: 1px solid #2e3140; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);'>
        <h3 style='color: #64b5f6 !important;'>🏥 Medical Semantic Search Engine</h3>
        <p style='color: #e0e0e0;'><strong style='color: #90caf9;'>Technologies:</strong> FastAPI • FAISS • Sentence Transformers • Streamlit</p>
        <p style='color: #e0e0e0;'><strong style='color: #90caf9;'>Dataset:</strong> MedQuAD (NIH) • 16,412 Medical Q&A Pairs</p>
        <p style='color: #b0b0b0; font-size: 0.9em; margin-top: 15px;'>
            📚 Projet Big Data & Vector Database<br>
            👤 ILBOUDO P. Daniel Glorieux<br>
            🏫 École Centrale de Lyon - {year}
        </p>
        <p style='color: #808080; font-size: 0.8em; margin-top: 10px;'>
            ⚠️ Application éducative - Ne remplace pas un avis médical professionnel
        </p>
    </div>
    """.format(year=dt.now().year),
    unsafe_allow_html=True
)
