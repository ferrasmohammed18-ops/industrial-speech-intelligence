
import wave
import json
from pathlib import Path

from piper import PiperVoice


TRANSCRIPTS_DIR = Path("data/synthetic/transcripts")
AUDIO_DIR = Path("data/synthetic/audio")

MODELS_DIR = Path("models/piper")

VOICE_MODELS = [
    MODELS_DIR / "fr_FR-mls-medium.onnx",
    MODELS_DIR / "fr_FR-siwis-medium.onnx",
    MODELS_DIR / "fr_FR-tom-medium.onnx",
]


def generate_audio(voice, text, output_path):
    with wave.open(str(output_path), "wb") as audio_file:
        voice.synthesize_wav(text, audio_file)


def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    voices = [
        PiperVoice.load(str(model_path))
        for model_path in VOICE_MODELS
    ]

    json_files = sorted(TRANSCRIPTS_DIR.glob("SC*.json"))

    if not json_files:
        print("Aucun compte rendu trouvé.")
        return

    for index, json_file in enumerate(json_files):
        with json_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        transcript = data["transcript"]

        output_path = AUDIO_DIR / f"{json_file.stem}.wav"

        voice_index = index % len(voices)
        voice = voices[voice_index]

        generate_audio(voice, transcript, output_path)

        print(f"Audio généré : {output_path}")


if __name__ == "__main__":
    main()
