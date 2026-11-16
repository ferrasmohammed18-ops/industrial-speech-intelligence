
import json
from anthropic import Anthropic
from dotenv import load_dotenv

from src.information_extraction.schema import MaintenanceReport


load_dotenv()
client = Anthropic()


def extract_information(transcript: str) -> MaintenanceReport:
    """
    Extrait les informations d'un compte rendu de maintenance
    à partir d'une transcription Whisper.
    """

    prompt = f"""
Tu es un assistant spécialisé dans la maintenance industrielle.

Analyse la transcription suivante et extrais les informations
dans le format JSON demandé.

Règles :
- N'invente jamais d'informations.
- Si une information est absente, utilise null.
- Pour les listes, utilise une liste vide si aucune information
  n'est disponible.
- Distingue les symptômes des actions réalisées.
- La priorité ne doit être renseignée que si elle est explicitement
  mentionnée.
- Les informations incertaines doivent être considérées comme absentes.
- Retourne uniquement un objet JSON valide, sans Markdown ni commentaire.

Transcription :
{transcript}

Champs JSON attendus :
- equipment
- equipment_type
- problem
- symptoms
- observations
- actions_performed
- priority
- missing_information
"""

    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1200,
        thinking={"type": "disabled"},
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    if response.stop_reason == "max_tokens":
        raise ValueError("Réponse Claude tronquée : limite de tokens atteinte.")

    text_blocks = [
        block.text
        for block in response.content
        if block.type == "text"
    ]

    if not text_blocks:
        raise ValueError(
            f"Aucun texte retourné. Stop reason : {response.stop_reason}"
        )

    response_text = "\n".join(text_blocks)

    json_start = response_text.find("{")

    if json_start == -1:
        raise ValueError(
            f"Aucun JSON trouvé : {response_text[:200]}"
        )

    data, _ = json.JSONDecoder().raw_decode(
        response_text[json_start:]
    )

    return MaintenanceReport(**data)
