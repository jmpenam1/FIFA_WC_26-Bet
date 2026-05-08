from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st

from src.config import STAGE_GROUPS, STAGE_KNOCKOUT
from src.dashboard import build_match_detail, build_ranking, build_stage_pivot, build_total_ranking
from src.io_utils import dataframe_to_excel_bytes, read_predictions_file, read_results_file
from src.scoring import score_predictions
from src.validation import validate_predictions, validate_results

st.set_page_config(page_title="FIFA WC 26 Tracker", page_icon="⚽", layout="wide")

STAGE_LABELS = {
    STAGE_GROUPS: "Fase de grupos",
    STAGE_KNOCKOUT: "Fase eliminatoria",
}

st.title("⚽ FIFA World Cup 2026 - Tracker de predicciones")
st.caption("Carga predicciones por etapa, compara contra resultados reales y genera rankings independientes y acumulados.")

with st.sidebar:
    st.header("Plantillas")
    st.markdown("Descarga la plantilla que corresponda a cada etapa.")
    for file_name, label in [
        ("plantilla_grupos.xlsx", "Descargar plantilla grupos"),
        ("plantilla_eliminatorias.xlsx", "Descargar plantilla eliminatorias"),
    ]:
        file_path = ROOT_DIR / "data" / file_name
        if file_path.exists():
            st.download_button(
                label=label,
                data=file_path.read_bytes(),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

st.info(
    "La quiniela está separada en dos oportunidades: fase de grupos y fase eliminatoria. "
    "La eliminatoria se llena después de conocer los cruces reales."
)

all_scored_frames: list[pd.DataFrame] = []

for stage, label in STAGE_LABELS.items():
    st.header(label)
    col1, col2 = st.columns([1, 1])

    with col1:
        results_file = st.file_uploader(
            f"Resultados reales - {label}",
            type=["xlsx"],
            key=f"results_{stage}",
        )
    with col2:
        prediction_files = st.file_uploader(
            f"Predicciones participantes - {label}",
            type=["xlsx"],
            accept_multiple_files=True,
            key=f"predictions_{stage}",
        )

    if results_file and prediction_files:
        try:
            results_df = read_results_file(results_file, stage)
            result_errors = validate_results(results_df, stage)
            if result_errors:
                for error in result_errors:
                    st.error(error)
                continue

            stage_scored_frames = []
            for uploaded_file in prediction_files:
                predictions_df, participant_name = read_predictions_file(uploaded_file, stage)
                prediction_errors = validate_predictions(predictions_df, stage)
                if prediction_errors:
                    st.warning(f"Errores en archivo de {participant_name}:")
                    for error in prediction_errors:
                        st.error(error)
                    continue

                scored_df = score_predictions(predictions_df, results_df, stage)
                stage_scored_frames.append(scored_df)

            if stage_scored_frames:
                scored_stage = pd.concat(stage_scored_frames, ignore_index=True)
                all_scored_frames.append(scored_stage)

                st.subheader(f"Ranking - {label}")
                ranking_stage = build_ranking(scored_stage)
                st.dataframe(ranking_stage, use_container_width=True)

                st.subheader(f"Detalle - {label}")
                participants = ["Todos"] + sorted(scored_stage["participante"].dropna().unique().tolist())
                selected_participant = st.selectbox(
                    f"Participante a revisar - {label}",
                    participants,
                    key=f"participant_detail_{stage}",
                )
                st.dataframe(build_match_detail(scored_stage, selected_participant), use_container_width=True)
        except Exception as exc:
            st.exception(exc)
    else:
        st.caption(f"Carga el archivo de resultados reales y al menos un archivo de predicciones para calcular {label.lower()}.")

st.divider()
st.header("Ranking acumulado")

if all_scored_frames:
    all_scored = pd.concat(all_scored_frames, ignore_index=True)
    total_ranking = build_total_ranking(all_scored)
    stage_pivot = build_stage_pivot(all_scored)
    detail = build_match_detail(all_scored)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Tabla acumulada")
        st.dataframe(total_ranking, use_container_width=True)
    with c2:
        st.subheader("Puntos por etapa")
        st.dataframe(stage_pivot, use_container_width=True)

    export_bytes = dataframe_to_excel_bytes(
        {
            "ranking_acumulado": total_ranking,
            "ranking_por_etapa": stage_pivot,
            "detalle": detail,
        }
    )
    st.download_button(
        "Descargar resultados consolidados",
        data=export_bytes,
        file_name="ranking_mundial_2026.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.caption("Cuando cargues archivos de grupos y/o eliminatorias, aquí aparecerá el ranking total.")
