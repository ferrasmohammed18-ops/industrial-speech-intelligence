
import numpy as np
from fastembed import TextEmbedding


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_embedding_model():
    """
    Charge le modèle d'embeddings multilingue.
    """
    return TextEmbedding(model_name=MODEL_NAME)


def generate_embeddings(model, texts: list[str]) -> np.ndarray:
    """
    Transforme une liste de textes en vecteurs numériques.
    """
    embeddings = list(model.embed(texts))

    return np.asarray(embeddings, dtype=np.float32)
