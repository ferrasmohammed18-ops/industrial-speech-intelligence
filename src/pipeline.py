
from pathlib import Path

from src.speech_to_text.transcribe import (
    load_model,
    transcribe_audio,
)
from src.information_extraction.extractor import extract_information
from src.rag.retriever import retrieve_documents
from src.report_generation.generator import generate_report


def run_pipeline(audio_path: str) -> str:
    """
    Exécute le pipeline complet à partir d'un fichier audio.
    """

    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

    print("\n1. Chargement de Whisper...")
    whisper_model = load_model()

    print("\n2. Transcription audio...")
    transcript = transcribe_audio(whisper_model, audio_path)
    print(transcript)

    print("\n3. Extraction des informations...")
    extracted_report = extract_information(transcript)
    extracted_data = extracted_report.model_dump()
    print(extracted_data)

    print("\n4. Recherche dans les manuels...")
    query = transcript
    retrieved_documents = retrieve_documents(query, top_k=3)

    print("\n5. Génération du compte rendu...")
    report = generate_report(
        transcript=transcript,
        extracted_data=extracted_data,
        retrieved_documents=retrieved_documents,
    )

    print("\nPipeline terminé.")

    return {
        "transcript": transcript,
        "extracted_data": extracted_data,
        "retrieved_documents": retrieved_documents,
        "report": report,
    }

