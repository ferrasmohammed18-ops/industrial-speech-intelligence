
import json
from pathlib import Path


DATA_DIR = Path("data/synthetic/transcripts")

REQUIRED_FIELDS = {
    "scenario_id": str,
    "equipment_type": str,
    "equipment_id": str,
    "problem": str,
    "symptoms": list,
    "observations": list,
    "actions": list,
}


def validate_file(file_path):
    errors = []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        return [f"Fichier illisible : {error}"]

    if not isinstance(data, dict):
        return ["Le contenu JSON doit être un objet."]

    scenario = data.get("scenario")
    transcript = data.get("transcript")

    if not isinstance(scenario, dict):
        return ["Scénario absent ou invalide."]

    if not isinstance(transcript, str) or not transcript.strip():
        errors.append("Compte rendu absent ou vide.")

    for field, expected_type in REQUIRED_FIELDS.items():
        value = scenario.get(field)

        if not isinstance(value, expected_type):
            errors.append(f"Champ invalide : {field}")

    if errors:
        return errors

    if scenario["scenario_id"] != file_path.stem:
        errors.append("Identifiant du scénario différent du nom du fichier.")

    if scenario["equipment_id"] not in transcript:
        errors.append("Identifiant de l'équipement absent du texte.")

    return errors


def main():
    files = sorted(DATA_DIR.glob("SC*.json"))

    if not files:
        print("Aucun fichier trouvé.")
        return

    valid_count = 0

    for file_path in files:
        errors = validate_file(file_path)

        if errors:
            print(f"ERREUR - {file_path.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK - {file_path.name}")
            valid_count += 1

    print(f"\nRésultat : {valid_count}/{len(files)} fichiers valides.")


if __name__ == "__main__":
    main()
