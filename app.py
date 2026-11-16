import streamlit as st
import tempfile
from pathlib import Path

from src.pipeline import run_pipeline
from src.pdf_generation.generator import generate_pdf


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Industrial Speech Intelligence",
    page_icon="🏭",
    layout="wide",
)


# --------------------------------------------------
# DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F4F6FA;
    }

    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }

    .main-header {
        background: linear-gradient(120deg, #14243A, #244B70);
        padding: 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
    }

    .main-header h1 {
        color: white;
        font-size: 30px;
        margin-bottom: 8px;
    }

    .main-header p {
        color: #D5E3F1;
        font-size: 15px;
        margin-bottom: 0;
    }

    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
    }
</style>

<div class="main-header">
    <h1>🏭 Industrial Speech Intelligence</h1>
    <p>AI-powered industrial maintenance assistant</p>
</div>
""", unsafe_allow_html=True)

st.caption("AI-powered analysis and maintenance report generation")

st.divider()


# --------------------------------------------------
# AUDIO UPLOAD
# --------------------------------------------------

st.subheader("1. Audio Upload")

st.write(
    "Upload an audio recording to generate "
    "a transcription and a structured maintenance report."
)

audio_file = st.file_uploader(
    "Select an audio file",
    type=["wav", "mp3", "m4a"],
)


# --------------------------------------------------
# AUDIO ANALYSIS
# --------------------------------------------------

if audio_file is not None:

    st.audio(audio_file)

    if st.button("Analyze Recording", type="primary"):

        suffix = Path(audio_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(audio_file.getvalue())
            temp_path = temp_file.name

        try:
            with st.spinner("Processing audio..."):
                results = run_pipeline(temp_path)

            st.session_state["results"] = results
            st.success("Analysis completed successfully!")

        except Exception as error:
            st.error(f"An error occurred: {error}")

        finally:
            Path(temp_path).unlink(missing_ok=True)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()
    st.subheader("2. Analysis Results")

    # Processing indicators
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Audio", "Uploaded", "✓")

    with col2:
        st.metric("Transcription", "Completed", "✓")

    with col3:
        st.metric("RAG Retrieval", "Completed", "✓")

    with col4:
        st.metric("Report", "Generated", "✓")

    # Speech transcription
    with st.expander("View Whisper Transcription"):
        st.write(results["transcript"])

    # Extracted information
    with st.expander("View Extracted Information", expanded=True):

        data = results["extracted_data"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Equipment**")
            st.info(data.get("equipment") or "Not specified")

            st.markdown("**Equipment Type**")
            st.info(data.get("equipment_type") or "Not specified")

            st.markdown("**Reported Problem**")
            st.info(data.get("problem") or "Not specified")

            st.markdown("**Priority**")
            st.info(data.get("priority") or "Not specified")

        with col2:
            st.markdown("**Symptoms**")
            symptoms = data.get("symptoms") or []

            if symptoms:
                for item in symptoms:
                    st.markdown(f"- {item}")
            else:
                st.write("No symptoms reported")

            st.markdown("**Observations**")
            observations = data.get("observations") or []

            if observations:
                for item in observations:
                    st.markdown(f"- {item}")
            else:
                st.write("No observations reported")

            st.markdown("**Actions Performed**")
            actions = data.get("actions_performed") or []

            if actions:
                for item in actions:
                    st.markdown(f"- {item}")
            else:
                st.write("No actions reported")

        st.markdown("**Missing Information**")
        missing = data.get("missing_information") or []

        if missing:
            for item in missing:
                st.markdown(f"- {item}")
        else:
            st.success("No missing information reported")

    # Retrieved technical references
    with st.expander("View Retrieved Technical References"):

        for document in results["retrieved_documents"]:

            st.markdown(
                f"**Source:** {document['source']}  \n"
                f"**Page:** {document['page']}  \n"
                f"**Similarity Score:** {document['similarity']:.3f}"
            )

            st.write(document["text"])
            st.divider()

    # Generated maintenance report
    st.divider()
    st.subheader("3. Generated Maintenance Report")

    report = results["report"]

    with st.container(border=True):
        st.markdown(report)

    # TXT download
    st.download_button(
        label="📄 Download Report (.txt)",
        data=report,
        file_name="maintenance_report.txt",
        mime="text/plain",
        type="primary",
    )

    # PDF download
    pdf_file = generate_pdf(report)

    st.download_button(
        label="📕 Download Report (.pdf)",
        data=pdf_file,
        file_name="maintenance_report.pdf",
        mime="application/pdf",
    )

else:
    st.info(
        "👋 Welcome! Upload an audio file above "
        "to start analyzing your maintenance intervention."
    )