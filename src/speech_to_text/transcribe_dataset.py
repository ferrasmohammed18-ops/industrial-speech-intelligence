
import json
from pathlib import Path

from src.speech_to_text.transcribe import (
    load_model,
    transcribe_audio,
)

AUDIO_DIR = Path("data/synthetic/audio")
OUTPUT_DIR = Path("data/synthetic/transcripts_whisper")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Chargement de Whisper...")
    model = load_model()

    audio_files = sorted(AUDIO_DIR.glob("SC*.wav"))

    if not audio_files:
        print("Aucun fichier audio trouvé.")
        return

    for audio_path in audio_files:
        output_path = OUTPUT_DIR / f"{audio_path.stem}.json"

        if output_path.exists():
            print(f"Déjà transcrit, ignoré : {audio_path.name}")
            continue

        print(f"Transcription : {audio_path.name}")

        transcript = transcribe_audio(model, audio_path)

        output = {
            "scenario_id": audio_path.stem,
            "transcript": transcript,
        }

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(output, file, ensure_ascii=False, indent=2)

        print(f"Transcription enregistrée : {output_path}")


if __name__ == "__main__":
    main()
