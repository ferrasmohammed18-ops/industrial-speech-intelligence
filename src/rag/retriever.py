
import json
from pathlib import Path

import numpy as np

from src.rag.embeddings import (
    load_embedding_model,
    generate_embeddings,
)


CHUNKS_PATH = Path("data/synthetic/chunks.json")
VECTORS_PATH = Path("data/synthetic/embeddings/vectors.npy")


def retrieve_documents(query: str, top_k: int = 3) -> list[dict]:
    """
    Recherche les passages les plus proches d'une description de panne.
    """

    if not query.strip():
        raise ValueError("La requête ne peut pas être vide.")

    if not CHUNKS_PATH.exists() or not VECTORS_PATH.exists():
        raise FileNotFoundError("Les chunks ou les embeddings sont introuvables.")

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    vectors = np.load(VECTORS_PATH)

    if len(chunks) != len(vectors):
        raise ValueError("Le nombre de chunks ne correspond pas au nombre de vecteurs.")

    model = load_embedding_model()

    query_vector = generate_embeddings(model, [query])[0]

    # Les vecteurs du corpus et la requête sont normalisés
    # pour calculer leur similarité cosinus avec le produit scalaire.
    corpus_norms = np.linalg.norm(vectors, axis=1)
    query_norm = np.linalg.norm(query_vector)

    if query_norm == 0 or np.any(corpus_norms == 0):
        raise ValueError("Un embedding nul empêche le calcul de similarité.")

    similarities = np.dot(vectors, query_vector) / (
        corpus_norms * query_norm
    )

    best_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in best_indices:
        result = chunks[int(index)].copy()
        result["similarity"] = float(similarities[index])
        results.append(result)

    return results
