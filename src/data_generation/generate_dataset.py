import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from src.data_generation.scenarios import SCENARIOS

load_dotenv()

client = anthropic.Anthropic()


def generate_report(scenario):
    prompt = f"""
    Tu es un assistant spécialisé dans la maintenance industrielle.

    À partir du scénario suivant, rédige un compte rendu
    d'intervention naturel en français.

    Règles impératives :
- Utilise exclusivement les informations présentes dans le scénario.
- N'ajoute aucune date, circonstance ou contexte.
- N'invente aucun symptôme, diagnostic, action ou priorité.
- Ne transforme pas une information inconnue en information certaine.
- Ne mentionne pas les champs vides ou les valeurs null.
- Ne déduis aucune cause technique.
- Conserve les identifiants des équipements exactement.
- Rédige un seul paragraphe en français professionnel.
- Retourne uniquement le compte rendu, sans introduction ni commentaire.

    Scénario :
    {json.dumps(scenario, ensure_ascii=False, indent=2)}
    """

    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    print("Stop reason :", response.stop_reason)
    print("Types de blocs :", [block.type for block in response.content])
    print(
        f"Tokens utilisés — entrée : {response.usage.input_tokens}, "
        f"sortie : {response.usage.output_tokens}"
    )

    report = next(
        (
            block.text
            for block in response.content
            if block.type == "text"
        ),
        None,
    )

    if not report:
        raise ValueError("Claude n'a renvoyé aucun texte.")

    return report.strip()


def main():
    output_dir = Path("data/synthetic/transcripts")
    output_dir.mkdir(parents=True, exist_ok=True)

    MAX_REPORTS = 2
    generated_count = 0

    for scenario in SCENARIOS:
        output_file = output_dir / f"{scenario['scenario_id']}.json"

        if output_file.exists():
            print(f"Déjà généré, ignoré : {output_file}")
            continue

        report = generate_report(scenario)

        output = {
            "scenario": scenario,
            "transcript": report,
        }

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(output, file, ensure_ascii=False, indent=2)

        generated_count += 1
        print(f"Compte rendu généré : {output_file}")

        if generated_count >= MAX_REPORTS:
            print(f"Limite atteinte : {generated_count} comptes rendus.")
            break


if __name__ == "__main__":
    main()