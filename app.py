
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

st.caption(
    "Plateforme d'analyse et de génération de rapports de maintenance"
)

st.divider()


# --------------------------------------------------
# IMPORT AUDIO
# --------------------------------------------------

st.subheader("1. Importer un enregistrement")

st.write(
    "Importez un enregistrement audio pour obtenir "
    "une transcription et un compte rendu de maintenance."
)

audio_file = st.file_uploader(
    "Sélectionnez un fichier audio",
    type=["wav", "mp3", "m4a"],
)


# --------------------------------------------------
# ANALYSE AUDIO
# --------------------------------------------------

if audio_file is not None:

    st.audio(audio_file)

    if st.button("Analyser l'enregistrement", type="primary"):

        suffix = Path(audio_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(audio_file.getvalue())
            temp_path = temp_file.name

        try:
            with st.spinner("Analyse en cours..."):
                results = run_pipeline(temp_path)

            st.session_state["results"] = results
            st.success("Analyse terminée avec succès !")

        except Exception as error:
            st.error(f"Une erreur est survenue : {error}")

        finally:
            Path(temp_path).unlink(missing_ok=True)


# --------------------------------------------------
# RÉSULTATS
# --------------------------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]

    st.divider()
    st.subheader("2. Résultats de l'analyse")

    # Indicateurs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Audio", "Chargé", "✓")

    with col2:
        st.metric("Transcription", "Terminée", "✓")

    with col3:
        st.metric("Recherche RAG", "Terminée", "✓")

    with col4:
        st.metric("Rapport", "Généré", "✓")

    # Transcription
    with st.expander("Voir la transcription Whisper"):
        st.write(results["transcript"])

    # Informations extraites
    with st.expander("Voir les informations extraites", expanded=True):

        data = results["extracted_data"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Équipement**")
            st.info(data.get("equipment") or "Non renseigné")

            st.markdown("**Type d'équipement**")
            st.info(data.get("equipment_type") or "Non renseigné")

            st.markdown("**Problème signalé**")
            st.info(data.get("problem") or "Non renseigné")

            st.markdown("**Priorité**")
            st.info(data.get("priority") or "Non renseignée")

        with col2:
            st.markdown("**Symptômes**")
            symptoms = data.get("symptoms") or []

            if symptoms:
                for item in symptoms:
                    st.markdown(f"- {item}")
            else:
                st.write("Aucun symptôme renseigné")

            st.markdown("**Observations**")
            observations = data.get("observations") or []

            if observations:
                for item in observations:
                    st.markdown(f"- {item}")
            else:
                st.write("Aucune observation renseignée")

            st.markdown("**Actions réalisées**")
            actions = data.get("actions_performed") or []

            if actions:
                for item in actions:
                    st.markdown(f"- {item}")
            else:
                st.write("Aucune action renseignée")

        st.markdown("**Informations manquantes**")
        missing = data.get("missing_information") or []

        if missing:
            for item in missing:
                st.markdown(f"- {item}")
        else:
            st.success("Aucune information manquante signalée")

    # Sources documentaires
    with st.expander("Voir les sources documentaires"):

        for document in results["retrieved_documents"]:

            st.markdown(
                f"**Source :** {document['source']}  \n"
                f"**Page :** {document['page']}  \n"
                f"**Similarité :** {document['similarity']:.3f}"
            )

            st.write(document["text"])
            st.divider()

    # Compte rendu final
    st.divider()
    st.subheader("3. Compte rendu de maintenance")

    report = results["report"]

    with st.container(border=True):
        st.markdown(report)

    # Téléchargement TXT
    st.download_button(
        label="📄 Télécharger le compte rendu (.txt)",
        data=report,
        file_name="compte_rendu_maintenance.txt",
        mime="text/plain",
        type="primary",
    )

    # Téléchargement PDF
    pdf_file = generate_pdf(report)

    st.download_button(
        label="📕 Télécharger le compte rendu (.pdf)",
        data=pdf_file,
        file_name="compte_rendu_maintenance.pdf",
        mime="application/pdf",
    )

else:
    st.info(
        "👋 Bienvenue ! Importez un fichier audio ci-dessus "
        "pour commencer l'analyse de votre intervention."
    )
