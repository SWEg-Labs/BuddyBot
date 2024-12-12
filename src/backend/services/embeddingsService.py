import os
from langchain_openai import OpenAIEmbeddings

class EmbeddingsService(OpenAIEmbeddings):

    def __init__(self, *args, **kwargs):
        super().__init__(openai_api_key=os.getenv("OPENAI_API_KEY"), *args, **kwargs)
        
    def _embed_documents(self, texts):
        return super().embed_documents(texts)  # <--- use OpenAIEmbedding's embedding function

    def __call__(self, input):
        return self._embed_documents(input)    # <--- get the embeddings