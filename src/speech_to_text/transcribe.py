
from faster_whisper import WhisperModel


def load_model(model_size="small"):
    """
    Charge le modèle Whisper.
    """
    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",
    )
    return model


def transcribe_audio(model, audio_path):
    """
    Transcrit un fichier audio en français.
    """
    segments, info = model.transcribe(
        str(audio_path),
        language="fr",
    )

    transcript = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return transcript
