"""Utilidades de lectura y exportación de Excel."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd

from .config import SHEET_PARTICIPANT, SHEET_PREDICTIONS_BY_STAGE, SHEET_RESULTS_BY_STAGE


def read_excel_sheet(uploaded_file, sheet_name: str) -> pd.DataFrame:
    """Lee una hoja de Excel desde un uploader de Streamlit o una ruta local."""
    try:
        return pd.read_excel(uploaded_file, sheet_name=sheet_name)
    except ValueError as exc:
        raise ValueError(f"No se encontró la hoja '{sheet_name}'.") from exc
    except Exception as exc:
        raise ValueError(f"No fue posible leer el archivo Excel: {exc}") from exc


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas y elimina filas totalmente vacías."""
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    df = df.dropna(how="all")

    if "match_id" in df.columns:
        df["match_id"] = df["match_id"].astype(str).str.strip()

    if "etapa" in df.columns:
        df["etapa"] = df["etapa"].astype(str).str.strip().str.lower()

    return df


def extract_participant_name(uploaded_file) -> str:
    """Obtiene el nombre del participante desde la hoja PARTICIPANTE o desde el nombre del archivo."""
    participant_name = Path(getattr(uploaded_file, "name", "participante.xlsx")).stem

    try:
        participant_df = read_excel_sheet(uploaded_file, SHEET_PARTICIPANT)
        participant_df.columns = [str(col).strip().lower() for col in participant_df.columns]

        if {"campo", "valor"}.issubset(participant_df.columns):
            mask = participant_df["campo"].astype(str).str.lower().str.strip().eq("nombre_participante")
            row = participant_df.loc[mask]
            if not row.empty and pd.notna(row.iloc[0]["valor"]):
                candidate = str(row.iloc[0]["valor"]).strip()
                if candidate:
                    participant_name = candidate
    except Exception:
        pass

    return participant_name


def read_predictions_file(uploaded_file, stage: str) -> tuple[pd.DataFrame, str]:
    """Lee predicciones según la etapa seleccionada."""
    sheet_name = SHEET_PREDICTIONS_BY_STAGE[stage]
    predictions = clean_dataframe(read_excel_sheet(uploaded_file, sheet_name))
    participant_name = extract_participant_name(uploaded_file)
    predictions["participante"] = participant_name
    predictions["etapa"] = stage
    return predictions, participant_name


def read_results_file(uploaded_file, stage: str) -> pd.DataFrame:
    """Lee resultados reales según la etapa seleccionada."""
    sheet_name = SHEET_RESULTS_BY_STAGE[stage]
    results = clean_dataframe(read_excel_sheet(uploaded_file, sheet_name))
    results["etapa"] = stage
    return results


def dataframe_to_excel_bytes(sheets: dict[str, pd.DataFrame] | pd.DataFrame, sheet_name: str = "ranking") -> bytes:
    """Convierte uno o varios DataFrames a bytes de Excel para descarga."""
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if isinstance(sheets, pd.DataFrame):
            sheets.to_excel(writer, index=False, sheet_name=sheet_name[:31])
        else:
            for name, df in sheets.items():
                safe_name = str(name)[:31]
                df.to_excel(writer, index=False, sheet_name=safe_name)

    output.seek(0)
    return output.getvalue()
