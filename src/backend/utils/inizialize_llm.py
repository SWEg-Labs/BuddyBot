import os
from langchain_openai import ChatOpenAI
from utils.logger import logger  # Usa il logger che ti ho fornito in precedenza

def initialize_llm():
    """
    Initializes the language model using the OpenAI API key and model name.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI language model.

    Raises:
        ValueError: If the OPENAI_API_KEY is not set in the environment variables.
    """
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini") # Valore di default per il modello LLM: gpt-4o-mini

        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        
        llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
        )

        logger.info(f"LLM initialized with model: {model_name}")
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise