import json
from pathlib import Path

from src.information_extraction.extractor import extract_information


INPUT_DIR = Path("data/synthetic/transcripts_whisper")
OUTPUT_DIR = Path("data/synthetic/annotations")

BATCH_SIZE = 10


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_files = sorted(INPUT_DIR.glob("SC*.json"))

    if not json_files:
        print("Aucune transcription trouvée.")
        return

    pending_files = [
        file for file in json_files
        if not (OUTPUT_DIR / file.name).exists()
    ]

    print(f"Transcriptions trouvées : {len(json_files)}")
    print(f"Transcriptions restantes : {len(pending_files)}")

    for start in range(0, len(pending_files), BATCH_SIZE):
        batch = pending_files[start:start + BATCH_SIZE]

        print(f"\nTraitement du lot {start // BATCH_SIZE + 1}")

        for input_path in batch:
            try:
                with input_path.open("r", encoding="utf-8") as file:
                    data = json.load(file)

                transcript = data["transcript"]

                report = extract_information(transcript)

                output_path = OUTPUT_DIR / input_path.name

                with output_path.open("w", encoding="utf-8") as file:
                    json.dump(
                        report.model_dump(),
                        file,
                        ensure_ascii=False,
                        indent=2,
                    )

                print(f"Terminé : {input_path.name}")

            except Exception as error:
                print(f"Erreur pour {input_path.name} : {error}")

    print("\nTraitement terminé.")


if __name__ == "__main__":
    main()