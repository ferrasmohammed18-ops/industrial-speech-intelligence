# Industrial Speech Intelligence

AI-powered speech intelligence for industrial maintenance reporting.

## 1. Project Overview

Industrial Speech Intelligence is a prototype application designed to help industrial maintenance technicians create structured intervention reports from spoken descriptions.

Instead of manually writing lengthy reports, technicians can provide an audio recording describing their intervention. The application processes the audio, extracts relevant maintenance information, retrieves supporting technical documentation, and generates a structured report.

The project explores how speech recognition and large language models can support maintenance reporting workflows.

## 2. Main Features

- **Speech-to-Text:** Transcribes French audio recordings using Faster-Whisper.
- **Information Extraction:** Extracts structured maintenance information from transcripts using Claude and Pydantic.
- **Technical Document Retrieval:** Retrieves relevant passages from technical manuals using a local Retrieval-Augmented Generation (RAG) pipeline.
- **Report Generation:** Generates structured maintenance reports using the transcript, extracted information, and retrieved documentation.
- **PDF and TXT Export:** Allows users to download generated reports in PDF and text formats.
- **Local Web Interface:** Provides an interactive interface through Streamlit.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.12 |
| Speech recognition | Faster-Whisper |
| Large Language Model | Anthropic Claude API |
| Data validation | Pydantic |
| Embeddings | FastEmbed |
| Numerical computing | NumPy |
| PDF extraction | PyMuPDF |
| PDF generation | ReportLab |
| Web interface | Streamlit |
| Configuration | YAML, python-dotenv |
| Dependency management | uv |

## 4. Project Architecture

The application follows a sequential processing pipeline:

1. Audio input: a technician provides a French audio recording.
2. Speech recognition: Faster-Whisper converts the audio into text.
3. Information extraction: Claude extracts structured maintenance information.
4. Document retrieval: the RAG pipeline retrieves relevant passages from technical manuals.
5. Report generation: Claude generates a structured report using the available information and retrieved references.
6. Export: the report can be downloaded as a TXT or PDF file.

### RAG Workflow

The retrieval pipeline includes:

- PDF text extraction using PyMuPDF.
- Text chunking with configurable chunk size and overlap.
- Embedding generation using FastEmbed.
- Similarity-based retrieval to identify relevant document passages.

## 5. Installation and Setup

### Requirements

- Python 3.12 or later.
- Git.
- uv.
- An Anthropic API key.
- Technical PDF manuals supplied locally by the user.

### Clone the repository

```bash
git clone https://github.com/ferrasmohammed18-ops/industrial-speech-intelligence.git
cd industrial-speech-intelligence
```

### Install dependencies

```bash
uv sync
```

### Configure environment variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

Replace the placeholder with your own Anthropic API key.

### Add technical manuals

Place your authorized technical PDF manuals in:

```text
data/documents/manuals/
```

The manuals and generated datasets are not included in the repository.

### Run the application

```bash
uv run python -m streamlit run app.py
```

Open the local application in your browser:

```text
http://localhost:8501
```

## 6. Project Structure

```text
industrial-speech-intelligence/
│
├── app.py
├── config.yaml
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
│
├── data/
│   └── documents/
│       └── manuals/
│
├── scripts/
│   ├── run_pipeline.py
│   └── test_claude.py
│
└── src/
    ├── data_generation/
    ├── information_extraction/
    ├── pdf_generation/
    ├── rag/
    ├── report_generation/
    ├── speech_to_text/
    └── pipeline.py
```

Generated datasets, audio files, embeddings, downloaded models, and technical manuals are kept outside version control.

## 7. Limitations and Future Improvements

This project is an experimental portfolio prototype and is not intended for production use.

Current limitations include:

- Speech recognition accuracy may vary depending on audio quality and technical vocabulary.
- Report generation depends on the quality of the transcript and extracted information.
- RAG retrieval quality depends on the available technical documentation.
- Claude API requests require an internet connection and an API key.
- Generated reports must be reviewed and validated by a qualified maintenance professional.

Potential future improvements:

- More robust evaluation of speech recognition performance.
- Improved retrieval and ranking strategies.
- Expanded industrial equipment coverage.
- Additional validation and automated testing.
- Further improvements to the user interface and reporting workflow.

## 8. Screenshots and Demo

Screenshots and demonstration materials will be added as the project documentation evolves.

---

**Project status:** Experimental prototype  
**Interface:** Streamlit  
**Language:** French audio input and report generation  
**Repository:** GitHub