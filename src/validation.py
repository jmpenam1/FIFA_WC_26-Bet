"""Validaciones de estructura y contenido."""

from __future__ import annotations

import pandas as pd

from .config import (
    POINTS_KNOCKOUT_WINNER,
    PREDICTION_REQUIRED_COLUMNS_BY_STAGE,
    RESULTS_REQUIRED_COLUMNS_BY_STAGE,
    STAGE_KNOCKOUT,
)


def _missing_columns(df: pd.DataFrame, required_columns: list[str]) -> list[str]:
    return [col for col in required_columns if col not in df.columns]


def validate_predictions(df: pd.DataFrame, stage: str) -> list[str]:
    errors: list[str] = []
    required_columns = PREDICTION_REQUIRED_COLUMNS_BY_STAGE[stage]
    missing = _missing_columns(df, required_columns)
    if missing:
        errors.append(f"Faltan columnas obligatorias en predicciones: {', '.join(missing)}")
        return errors

    if df["match_id"].duplicated().any():
        duplicates = df.loc[df["match_id"].duplicated(), "match_id"].unique().tolist()
        errors.append(f"Hay match_id duplicados en predicciones: {duplicates[:10]}")

    for col in ["goles_local_pred", "goles_visitante_pred"]:
        invalid = pd.to_numeric(df[col], errors="coerce").dropna().lt(0).any()
        if invalid:
            errors.append(f"La columna {col} no puede tener valores negativos.")

    if stage == STAGE_KNOCKOUT:
        filled_scores = df[["goles_local_pred", "goles_visitante_pred"]].notna().all(axis=1)
        missing_winner = filled_scores & df["ganador_llave_pred"].isna()
        if missing_winner.any() and POINTS_KNOCKOUT_WINNER > 0:
            errors.append("En eliminatorias, ganador_llave_pred es obligatorio cuando el marcador está diligenciado.")

        valid_winner = df["ganador_llave_pred"].isna() | (
            df["ganador_llave_pred"].astype(str).str.strip().eq(df["equipo_local"].astype(str).str.strip())
            | df["ganador_llave_pred"].astype(str).str.strip().eq(df["equipo_visitante"].astype(str).str.strip())
        )
        if not valid_winner.all():
            errors.append("En eliminatorias, ganador_llave_pred debe coincidir con equipo_local o equipo_visitante.")

    return errors


def validate_results(df: pd.DataFrame, stage: str) -> list[str]:
    errors: list[str] = []
    required_columns = RESULTS_REQUIRED_COLUMNS_BY_STAGE[stage]
    missing = _missing_columns(df, required_columns)
    if missing:
        errors.append(f"Faltan columnas obligatorias en resultados reales: {', '.join(missing)}")
        return errors

    if df["match_id"].duplicated().any():
        duplicates = df.loc[df["match_id"].duplicated(), "match_id"].unique().tolist()
        errors.append(f"Hay match_id duplicados en resultados reales: {duplicates[:10]}")

    for col in ["goles_local_real", "goles_visitante_real"]:
        invalid = pd.to_numeric(df[col], errors="coerce").dropna().lt(0).any()
        if invalid:
            errors.append(f"La columna {col} no puede tener valores negativos.")

    if stage == STAGE_KNOCKOUT:
        filled_scores = df[["goles_local_real", "goles_visitante_real"]].notna().all(axis=1)
        missing_winner = filled_scores & df["ganador_llave_real"].isna()
        if missing_winner.any():
            errors.append("En resultados de eliminatorias, ganador_llave_real es obligatorio para partidos ya jugados.")

    return errors
