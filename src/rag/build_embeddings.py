
import json
import numpy as np
from pathlib import Path

from src.rag.embeddings import (
    load_embedding_model,
    generate_embeddings,
)


INPUT_PATH = Path("data/synthetic/chunks.json")
OUTPUT_DIR = Path("data/synthetic/embeddings")
OUTPUT_PATH = OUTPUT_DIR / "vectors.npy"


def main():
    if not INPUT_PATH.exists():
        print("Fichier chunks.json introuvable.")
        return

    with INPUT_PATH.open("r", encoding="utf-8") as file:
        chunks = json.load(file)

    if not chunks:
        print("Aucun chunk trouvé.")
        return

    texts = [chunk["text"] for chunk in chunks]

    print(f"Nombre de chunks : {len(texts)}")
    print("Chargement du modèle...")

    model = load_embedding_model()

    print("Génération des embeddings...")

    embeddings = generate_embeddings(model, texts)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.save(OUTPUT_PATH, embeddings)

    print("\nGénération terminée.")
    print(f"Nombre de vecteurs : {embeddings.shape[0]}")
    print(f"Dimensions par vecteur : {embeddings.shape[1]}")
    print(f"Fichier enregistré : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
