
import json
from pathlib import Path

from src.rag.extract import extract_text_from_pdf
from src.rag.chunking import split_text


MANUALS_DIR = Path("data/documents/manuals")
OUTPUT_PATH = Path("data/synthetic/chunks.json")


def main():
    pdf_files = sorted(MANUALS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("Aucun manuel PDF trouvé.")
        return

    all_chunks = []

    for pdf_path in pdf_files:
        print(f"Extraction : {pdf_path.name}")

        pages = extract_text_from_pdf(pdf_path)

        for page in pages:
            chunks = split_text(
                page["text"],
                chunk_size=500,
                chunk_overlap=100,
            )

            for chunk_index, chunk in enumerate(chunks):
                all_chunks.append({
                    "source": page["source"],
                    "page": page["page"],
                    "chunk_id": chunk_index,
                    "text": chunk,
                })

        print(f"  Pages extraites : {len(pages)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print("\nIngestion terminée.")
    print(f"Documents traités : {len(pdf_files)}")
    print(f"Total de chunks créés : {len(all_chunks)}")
    print(f"Fichier enregistré : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
