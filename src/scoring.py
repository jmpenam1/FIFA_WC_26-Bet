"""Lógica de puntuación para grupos y eliminatorias."""

from __future__ import annotations

import pandas as pd

from .config import POINTS_EXACT_SCORE, POINTS_KNOCKOUT_WINNER, POINTS_RESULT, STAGE_KNOCKOUT


def normalize_team(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().casefold()


def get_result(local_goals, visitor_goals) -> str | None:
    if pd.isna(local_goals) or pd.isna(visitor_goals):
        return None
    if local_goals > visitor_goals:
        return "LOCAL"
    if local_goals < visitor_goals:
        return "VISITANTE"
    return "EMPATE"


def score_row(row: pd.Series, stage: str) -> tuple[int, str, bool]:
    required = ["goles_local_pred", "goles_visitante_pred", "goles_local_real", "goles_visitante_real"]
    if any(pd.isna(row.get(col)) for col in required):
        return 0, "Pendiente", False

    pred_local = int(row["goles_local_pred"])
    pred_visitor = int(row["goles_visitante_pred"])
    real_local = int(row["goles_local_real"])
    real_visitor = int(row["goles_visitante_real"])

    points = 0
    tags: list[str] = []

    if pred_local == real_local and pred_visitor == real_visitor:
        points += POINTS_EXACT_SCORE
        tags.append("Marcador exacto")
    else:
        if get_result(pred_local, pred_visitor) == get_result(real_local, real_visitor):
            points += POINTS_RESULT
            tags.append("Resultado correcto")

    if stage == STAGE_KNOCKOUT:
        if normalize_team(row.get("ganador_llave_pred")) and normalize_team(row.get("ganador_llave_pred")) == normalize_team(row.get("ganador_llave_real")):
            points += POINTS_KNOCKOUT_WINNER
            tags.append("Ganador de llave")

    return points, " + ".join(tags) if tags else "Sin acierto", True


def score_predictions(predictions_df: pd.DataFrame, results_df: pd.DataFrame, stage: str) -> pd.DataFrame:
    """Une predicciones con resultados reales y calcula puntos."""
    predictions = predictions_df.copy()
    results = results_df.copy()

    for col in ["goles_local_pred", "goles_visitante_pred"]:
        predictions[col] = pd.to_numeric(predictions[col], errors="coerce")
    for col in ["goles_local_real", "goles_visitante_real"]:
        results[col] = pd.to_numeric(results[col], errors="coerce")

    result_cols = [
        "match_id",
        "goles_local_real",
        "goles_visitante_real",
    ]
    if "ganador_llave_real" in results.columns:
        result_cols.append("ganador_llave_real")

    merged = predictions.merge(results[result_cols], on="match_id", how="left")

    scored = merged.apply(lambda row: score_row(row, stage), axis=1, result_type="expand")
    merged["puntos"] = scored[0]
    merged["tipo_acierto"] = scored[1]
    merged["partido_puntuado"] = scored[2]

    merged["prediccion"] = (
        merged["goles_local_pred"].apply(lambda x: "" if pd.isna(x) else str(int(x)))
        + " - "
        + merged["goles_visitante_pred"].apply(lambda x: "" if pd.isna(x) else str(int(x)))
    )
    merged["resultado_real"] = (
        merged["goles_local_real"].apply(lambda x: "" if pd.isna(x) else str(int(x)))
        + " - "
        + merged["goles_visitante_real"].apply(lambda x: "" if pd.isna(x) else str(int(x)))
    )

    return merged
