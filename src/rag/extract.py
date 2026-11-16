
from pathlib import Path
import fitz


def extract_text_from_pdf(pdf_path: Path) -> list[dict]:
    """
    Extrait le texte d'un PDF page par page.

    Retourne une liste de pages avec leur contenu
    et leurs métadonnées.
    """
    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append({
                "source": pdf_path.name,
                "page": page_number,
                "text": text,
            })

    document.close()

    return pages
