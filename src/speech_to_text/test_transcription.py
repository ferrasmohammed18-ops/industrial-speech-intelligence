
from pathlib import Path

from src.speech_to_text.transcribe import (
    load_model,
    transcribe_audio,
)


def main():
    audio_path = Path("data/synthetic/audio/SC001.wav")

    print("Chargement de Whisper...")
    model = load_model()

    print("Transcription en cours...")
    transcript = transcribe_audio(model, audio_path)

    print("\nRésultat de la transcription :")
    print(transcript)


if __name__ == "__main__":
    main()
