
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def generate_report(
    transcript: str,
    extracted_data: dict,
    retrieved_documents: list[dict],
) -> str:
    """
    Génère un compte rendu de maintenance à partir
    de la transcription, des données extraites et des manuels.
    """

    documents_text = "\n\n".join(
        f"Source : {doc['source']}\n"
        f"Page : {doc['page']}\n"
        f"Extrait : {doc['text']}"
        for doc in retrieved_documents
    )

    prompt = f"""
Tu es un assistant spécialisé dans la rédaction de comptes rendus
de maintenance industrielle.

Rédige un compte rendu professionnel en français à partir
des informations suivantes.

TRANSCRIPTION :
{transcript}

INFORMATIONS EXTRAITES :
{extracted_data}

EXTRAITS DES MANUELS TECHNIQUES :
{documents_text}

RÈGLES STRICTES :
- N'invente aucune information.
- Ne transforme pas une hypothèse en diagnostic confirmé.
- Ne présente jamais une recommandation du manuel comme une action déjà réalisée.
- Si une information manque, indique « Non renseigné ».
- Distingue clairement les faits rapportés et les informations issues des manuels.
- Cite les sources documentaires avec leur nom et leur page.
- Si les manuels ne contiennent pas d'information pertinente, indique-le.

STRUCTURE DU COMPTE RENDU :

1. Équipement concerné
2. Problème signalé
3. Symptômes et observations
4. Actions réalisées
5. Informations techniques issues des manuels
6. Informations manquantes
7. Synthèse
"""

    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=3000,
        thinking={"type": "disabled"},
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    if response.stop_reason == "max_tokens":
        raise ValueError("Le compte rendu a été tronqué.")

    text_blocks = [
        block.text
        for block in response.content
        if block.type == "text"
    ]

    if not text_blocks:
        raise ValueError("Claude n'a retourné aucun texte.")

    return "\n".join(text_blocks).strip()
