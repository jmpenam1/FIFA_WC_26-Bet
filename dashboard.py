"""Funciones para construir tablas del dashboard."""

from __future__ import annotations

import pandas as pd


def build_ranking(scored_df: pd.DataFrame) -> pd.DataFrame:
    if scored_df.empty:
        return pd.DataFrame()

    ranking = (
        scored_df.groupby(["participante", "etapa"], as_index=False)
        .agg(
            puntos=("puntos", "sum"),
            partidos_puntuados=("partido_puntuado", "sum"),
            exactos=("tipo_acierto", lambda s: s.astype(str).str.contains("Marcador exacto", regex=False).sum()),
            resultados_correctos=("tipo_acierto", lambda s: s.astype(str).str.contains("Resultado correcto", regex=False).sum()),
            ganadores_llave=("tipo_acierto", lambda s: s.astype(str).str.contains("Ganador de llave", regex=False).sum()),
        )
        .sort_values(["puntos", "exactos", "ganadores_llave"], ascending=[False, False, False])
        .reset_index(drop=True)
    )
    ranking.insert(0, "posición", range(1, len(ranking) + 1))
    return ranking


def build_total_ranking(scored_df: pd.DataFrame) -> pd.DataFrame:
    if scored_df.empty:
        return pd.DataFrame()

    total = (
        scored_df.groupby("participante", as_index=False)
        .agg(
            puntos_totales=("puntos", "sum"),
            partidos_puntuados=("partido_puntuado", "sum"),
            exactos=("tipo_acierto", lambda s: s.astype(str).str.contains("Marcador exacto", regex=False).sum()),
            resultados_correctos=("tipo_acierto", lambda s: s.astype(str).str.contains("Resultado correcto", regex=False).sum()),
            ganadores_llave=("tipo_acierto", lambda s: s.astype(str).str.contains("Ganador de llave", regex=False).sum()),
        )
        .sort_values(["puntos_totales", "exactos", "ganadores_llave"], ascending=[False, False, False])
        .reset_index(drop=True)
    )
    total.insert(0, "posición", range(1, len(total) + 1))
    return total


def build_stage_pivot(scored_df: pd.DataFrame) -> pd.DataFrame:
    if scored_df.empty:
        return pd.DataFrame()

    pivot = scored_df.pivot_table(
        index="participante",
        columns="etapa",
        values="puntos",
        aggfunc="sum",
        fill_value=0,
    ).reset_index()
    stage_cols = [col for col in pivot.columns if col != "participante"]
    pivot["Total"] = pivot[stage_cols].sum(axis=1)
    pivot = pivot.sort_values("Total", ascending=False).reset_index(drop=True)
    pivot.insert(0, "posición", range(1, len(pivot) + 1))
    return pivot


def build_match_detail(scored_df: pd.DataFrame, participante: str | None = None) -> pd.DataFrame:
    if scored_df.empty:
        return pd.DataFrame()

    detail = scored_df.copy()
    if participante and participante != "Todos":
        detail = detail[detail["participante"] == participante]

    cols = [
        "participante",
        "etapa",
        "match_id",
        "match_number",
        "fase",
        "grupo",
        "fecha",
        "hora_et",
        "sede",
        "equipo_local",
        "equipo_visitante",
        "prediccion",
        "resultado_real",
        "ganador_llave_pred",
        "ganador_llave_real",
        "puntos",
        "tipo_acierto",
    ]
    existing = [col for col in cols if col in detail.columns]
    return detail[existing].sort_values(["participante", "etapa", "match_number"], ascending=True)
