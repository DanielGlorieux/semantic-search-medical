"""
Test de vitesse du RAG après optimisations
"""
import time
import os
import sys
from dotenv import load_dotenv

# Ajouter le backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.rag_service import RAGService

load_dotenv()

def test_rag_speed():
    """Teste la vitesse du service RAG"""
    print("=" * 70)
    print("⚡ TEST DE VITESSE DU RAG (Après Optimisations)")
    print("=" * 70)
    print()
    
    # Initialiser le service
    print("🔧 Initialisation du service RAG...")
    rag = RAGService()
    
    if not rag.is_available():
        print("❌ Service RAG non disponible!")
        print("   Vérifiez que GEMINI_API_KEY est configurée dans .env")
        return
    
    print("✅ Service RAG initialisé")
    print()
    
    # Préparer des documents de test
    test_docs = [
        {
            "doc_id": "1",
            "text": "Diabetes is a chronic condition that affects how your body processes blood sugar (glucose). Type 1 diabetes occurs when your immune system attacks insulin-producing cells. Type 2 diabetes occurs when your body becomes resistant to insulin or doesn't produce enough insulin. Common symptoms include increased thirst, frequent urination, fatigue, and blurred vision.",
            "source": "NIH Medical Database",
            "score": 0.92
        },
        {
            "doc_id": "2",
            "text": "Managing diabetes requires a combination of lifestyle changes and medical treatment. This includes monitoring blood sugar levels regularly, maintaining a healthy diet low in sugar and refined carbohydrates, regular physical exercise, and taking prescribed medications or insulin as directed by your healthcare provider.",
            "source": "CDC Health Guidelines",
            "score": 0.88
        },
        {
            "doc_id": "3",
            "text": "Complications of untreated or poorly managed diabetes can include cardiovascular disease, nerve damage (neuropathy), kidney damage (nephropathy), eye damage (retinopathy), and foot problems. Early detection and proper management are crucial for preventing these serious complications.",
            "source": "Medical Journal",
            "score": 0.85
        }
    ]
    
    test_query = "What are the symptoms of diabetes?"
    
    # Test 1: Génération de réponse
    print("━" * 70)
    print("📝 TEST 1: Génération de Réponse RAG")
    print("━" * 70)
    print()
    print(f"Question: {test_query}")
    print()
    print("⏱️  Génération en cours...")
    
    start_time = time.time()
    try:
        result = rag.generate_response(test_query, test_docs, max_docs=3)
        elapsed = time.time() - start_time
        
        print(f"✅ Réponse générée en {elapsed:.2f}s")
        print()
        print("🤖 Réponse:")
        print("-" * 70)
        print(result['response'])
        print("-" * 70)
        print()
        
        # Évaluation de la vitesse
        if elapsed < 5:
            status = "🟢 EXCELLENT"
        elif elapsed < 10:
            status = "🟡 BON"
        elif elapsed < 20:
            status = "🟠 ACCEPTABLE"
        else:
            status = "🔴 LENT"
        
        print(f"Performance: {status} ({elapsed:.2f}s)")
        print()
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ ERREUR après {elapsed:.2f}s: {e}")
        print()
    
    # Test 2: Génération de résumé
    print("━" * 70)
    print("📝 TEST 2: Génération de Résumé")
    print("━" * 70)
    print()
    print("⏱️  Génération en cours...")
    
    start_time = time.time()
    try:
        summary = rag.generate_summary(test_docs, top_n=3)
        elapsed = time.time() - start_time
        
        print(f"✅ Résumé généré en {elapsed:.2f}s")
        print()
        print("📋 Résumé:")
        print("-" * 70)
        print(summary)
        print("-" * 70)
        print()
        
        # Évaluation
        if elapsed < 3:
            status = "🟢 EXCELLENT"
        elif elapsed < 6:
            status = "🟡 BON"
        elif elapsed < 10:
            status = "🟠 ACCEPTABLE"
        else:
            status = "🔴 LENT"
        
        print(f"Performance: {status} ({elapsed:.2f}s)")
        print()
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ ERREUR après {elapsed:.2f}s: {e}")
        print()
    
    # Résumé final
    print("=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    print()
    print("✅ Optimisations Appliquées:")
    print("   • Prompt raccourci (moins de tokens)")
    print("   • Contexte limité (1000 chars/doc max)")
    print("   • Limite de génération (512 tokens max)")
    print("   • Timeout API (60s)")
    print("   • Configuration température/top_p optimisée")
    print()
    print("🎯 Objectifs de Performance:")
    print("   • Réponse RAG    : < 5s  (EXCELLENT)")
    print("   • Résumé         : < 3s  (EXCELLENT)")
    print("   • Taux de succès : > 95%")
    print()
    print("💡 Si les timeouts persistent:")
    print("   1. Vérifiez votre connexion internet")
    print("   2. Vérifiez le quota de votre clé API Gemini")
    print("   3. Essayez de réduire max_output_tokens dans rag_service.py")
    print("   4. Essayez de réduire max_docs (de 3 à 2)")
    print()

if __name__ == "__main__":
    test_rag_speed()
