import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY non trouvée")
    exit(1)

print("=" * 60)
print("📋 LISTE DES MODÈLES GEMINI DISPONIBLES")
print("=" * 60)
print()

genai.configure(api_key=api_key)

try:
    print("Modèles disponibles:")
    print()
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            print(f"   Description: {m.description[:100]}...")
            print()
except Exception as e:
    print(f"❌ Erreur: {e}")
