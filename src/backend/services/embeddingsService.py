import os
from langchain_openai import OpenAIEmbeddings
from logger import logger

class EmbeddingsService:
    def __init__(self):
        try:
            # Recupera la chiave API e il modello dalle variabili di ambiente
            openai_api_key = os.getenv("OPENAI_API_KEY")
            model_name = os.getenv("OPENAI_EMBEDDING_MODEL_NAME", "text-embedding-3-large")

            if not openai_api_key:
                raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
            
            # Inizializza le OpenAI embeddings
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=openai_api_key,
                model=model_name
            )

            logger.info(f"OpenAIEmbeddings initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAIEmbeddings: {e}")
            raise

    # Converte documenti di testo in vettori di embedding
    def generate_embeddings(self, texts):
        try:
            embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} documents.")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise