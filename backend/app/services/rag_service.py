import os
import logging
from typing import List, Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class RAGService:
    """Service RAG utilisant Google Gemini pour générer des réponses conviviales"""
    
    def __init__(self):
        """Initialise le service RAG avec Gemini"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                # Utiliser gemini-2.5-flash (rapide, gratuit, performant)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("Gemini model initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
                self.model = None
    
    def is_available(self) -> bool:
        """Vérifie si le service RAG est disponible"""
        return self.model is not None
    
    def generate_response(
        self,
        query: str,
        retrieved_docs: List[Dict],
        max_docs: int = 3
    ) -> Dict[str, any]:
        """
        Génère une réponse conviviale en français basée sur les documents récupérés
        
        Args:
            query: Question de l'utilisateur
            retrieved_docs: Liste des documents récupérés par la recherche sémantique
            max_docs: Nombre maximum de documents à utiliser pour le contexte
            
        Returns:
            Dict contenant la réponse générée et les métadonnées
        """
        if not self.is_available():
            return {
                "response": "Le service RAG n'est pas disponible. Voici les documents trouvés.",
                "error": "Gemini API not configured",
                "sources_used": []
            }
        
        try:
            # Préparer le contexte avec les meilleurs documents
            context_docs = retrieved_docs[:max_docs]
            context = self._build_context(context_docs)
            
            # Créer le prompt
            prompt = self._create_prompt(query, context)
            
            # Générer la réponse avec configuration optimisée pour la vitesse
            logger.info(f"Generating RAG response for query: {query}")
            
            # Configuration de génération pour réponses complètes
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.9,
                "top_k": 40,
                "max_output_tokens": 2048,  # Augmenté pour réponses complètes
                "stop_sequences": None,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                request_options={'timeout': 90}  # Timeout augmenté à 90 secondes
            )
            
            return {
                "response": response.text,
                "sources_used": [
                    {
                        "doc_id": doc.get("doc_id"),
                        "score": doc.get("score"),
                        "excerpt": doc.get("text", "")[:200] + "..."
                    }
                    for doc in context_docs
                ],
                "num_sources": len(context_docs),
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            return {
                "response": f"Désolé, une erreur s'est produite lors de la génération de la réponse. Voici les documents pertinents que j'ai trouvés.",
                "error": str(e),
                "sources_used": [{"doc_id": doc.get("doc_id")} for doc in context_docs]
            }
    
    def _build_context(self, docs: List[Dict]) -> str:
        """Construit le contexte à partir des documents récupérés"""
        context_parts = []
        for i, doc in enumerate(docs, 1):
            text = doc.get("text", "")
            # Augmenter la limite pour avoir plus de contexte
            if len(text) > 2000:
                text = text[:2000] + "..."
            source = doc.get("source", "Source inconnue")
            
            context_parts.append(
                f"[Document {i} - Source: {source}]\n{text}"
            )
        
        return "\n\n" + "="*50 + "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Crée le prompt pour Gemini - version optimisée pour réponses complètes"""
        prompt = f"""Tu es un assistant médical expert. Réponds en français à la question médicale en utilisant UNIQUEMENT les informations contenues dans ces documents.

DOCUMENTS DE RÉFÉRENCE:
{context}

QUESTION DE L'UTILISATEUR: {query}

INSTRUCTIONS:
1. Réponds de manière claire et complète en français
2. Utilise SEULEMENT les informations des documents fournis
3. Structure ta réponse en paragraphes lisibles
4. Termine par un avertissement: "⚠️ Note: Cette information est à but éducatif. Consultez toujours un professionnel de santé qualifié."
5. Si la réponse n'est pas dans les documents, dis-le clairement

RÉPONSE COMPLÈTE EN FRANÇAIS:"""
        
        return prompt
    
    def generate_summary(self, docs: List[Dict], top_n: int = 5) -> str:
        """Génère un résumé des top documents"""
        if not self.is_available():
            return "Service de résumé non disponible."
        
        try:
            context = self._build_context(docs[:top_n])
            
            prompt = f"""Résume en 2 phrases (français) ces documents médicaux:

{context}

Résumé:"""
            
            generation_config = {
                "temperature": 0.5,
                "max_output_tokens": 150,
            }
            
            response = self.model.generate_content(
                prompt, 
                generation_config=generation_config,
                request_options={'timeout': 30}
            )
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Impossible de générer un résumé pour le moment."
    
    def translate_and_simplify(self, text: str) -> str:
        """Traduit et simplifie un texte médical technique en français accessible"""
        if not self.is_available():
            return text
        
        try:
            prompt = f"""Traduis et simplifie ce texte médical en français facile à comprendre pour le grand public.
Garde les informations importantes mais rends-les accessibles.

TEXTE ORIGINAL:
{text}

TRADUCTION SIMPLIFIÉE EN FRANÇAIS:"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error translating: {e}")
            return text
