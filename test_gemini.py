import google.generativeai as genai
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

print("=" * 60)
print("🧪 TEST DE L'API GEMINI")
print("=" * 60)
print()

# Configurer Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY non trouvée dans .env")
    print("Créez un fichier .env avec:")
    print("GEMINI_API_KEY=votre_cle_api_ici")
    exit(1)

print(f"✅ Clé API trouvée: {api_key[:15]}...")
print()

# Tester l'API
try:
    print("🔄 Configuration de Gemini...")
    genai.configure(api_key=api_key)
    
    print("🔄 Création du modèle...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    print("🔄 Génération d'une réponse de test...")
    print()
    
    response = model.generate_content("Dis bonjour en français en une phrase courte")
    
    print("=" * 60)
    print("✅ RÉPONSE DE GEMINI:")
    print("=" * 60)
    print(response.text)
    print("=" * 60)
    print()
    print("🎉 Gemini fonctionne correctement !")
    print()
    
    # Test médical
    print("=" * 60)
    print("🏥 TEST MÉDICAL")
    print("=" * 60)
    print()
    
    medical_prompt = """Réponds en français à cette question médicale en 2-3 phrases:
    
Question: Quels sont les symptômes du diabète?

Contexte: Le diabète est une maladie chronique qui affecte la régulation du glucose.

Réponds de manière simple et conviviale."""

    response = model.generate_content(medical_prompt)
    print("Réponse:")
    print(response.text)
    print()
    print("🎉 Test médical réussi !")
    
except Exception as e:
    print("=" * 60)
    print("❌ ERREUR:")
    print("=" * 60)
    print(str(e))
    print()
    
    if "API_KEY_INVALID" in str(e) or "API key not valid" in str(e):
        print("💡 Solution: Votre clé API n'est pas valide.")
        print("   1. Allez sur: https://makersuite.google.com/app/apikey")
        print("   2. Créez une nouvelle clé API")
        print("   3. Mettez-la dans le fichier .env")
    elif "quota" in str(e).lower() or "exhausted" in str(e).lower():
        print("💡 Solution: Vous avez dépassé le quota gratuit.")
        print("   1. Attendez quelques minutes")
        print("   2. Ou créez une nouvelle clé API")
    else:
        print("💡 Erreur inconnue. Vérifiez:")
        print("   1. Connexion internet")
        print("   2. Clé API dans .env")
        print("   3. google-generativeai installé")
