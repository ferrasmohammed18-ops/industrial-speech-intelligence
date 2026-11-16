
import json
from pathlib import Path
from jiwer import wer

REFERENCE_PATH = Path("data/synthetic/transcripts/SC001.json")

reference = json.loads(
    REFERENCE_PATH.read_text(encoding="utf-8")
)["transcript"]

hypothesis = """
Un bruit vinaubituel a été signalé sur la pompe industrielle.
S.2. Le symptôme relevé est constitué de vibrations.
Les caves ont été constatées pans.
"""

score = wer(reference, hypothesis)

print(f"WER : {score:.2%}")
print(f"Référence : {reference}")
print(f"Whisper    : {hypothesis}")
