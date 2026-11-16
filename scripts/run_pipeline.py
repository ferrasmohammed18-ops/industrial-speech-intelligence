
from src.pipeline import run_pipeline


if __name__ == "__main__":
    report = run_pipeline(
        "data/synthetic/audio/SC001.wav"
    )

    print("\n========== COMPTE RENDU FINAL ==========\n")
    print(report)
