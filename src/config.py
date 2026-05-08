"""Configuración central del tracker por etapas."""

STAGE_GROUPS = "grupos"
STAGE_KNOCKOUT = "eliminatorias"
STAGES = [STAGE_GROUPS, STAGE_KNOCKOUT]

SHEET_PARTICIPANT = "PARTICIPANTE"
SHEET_PREDICTIONS_BY_STAGE = {
    STAGE_GROUPS: "PREDICCIONES_GRUPOS",
    STAGE_KNOCKOUT: "PREDICCIONES_ELIMINATORIAS",
}
SHEET_RESULTS_BY_STAGE = {
    STAGE_GROUPS: "RESULTADOS_GRUPOS",
    STAGE_KNOCKOUT: "RESULTADOS_ELIMINATORIAS",
}

KNOCKOUT_PHASES = {
    "Ronda de 32",
    "Dieciseisavos",
    "Octavos",
    "Cuartos",
    "Semifinal",
    "Tercer puesto",
    "Final",
}

GROUP_PREDICTION_REQUIRED_COLUMNS = [
    "match_id",
    "match_number",
    "etapa",
    "fase",
    "grupo",
    "fecha",
    "hora_et",
    "sede",
    "equipo_local",
    "equipo_visitante",
    "goles_local_pred",
    "goles_visitante_pred",
]

GROUP_RESULTS_REQUIRED_COLUMNS = [
    "match_id",
    "match_number",
    "etapa",
    "fase",
    "grupo",
    "fecha",
    "hora_et",
    "sede",
    "equipo_local",
    "equipo_visitante",
    "goles_local_real",
    "goles_visitante_real",
]

KNOCKOUT_PREDICTION_REQUIRED_COLUMNS = GROUP_PREDICTION_REQUIRED_COLUMNS + [
    "ganador_llave_pred",
]

KNOCKOUT_RESULTS_REQUIRED_COLUMNS = GROUP_RESULTS_REQUIRED_COLUMNS + [
    "ganador_llave_real",
]

PREDICTION_REQUIRED_COLUMNS_BY_STAGE = {
    STAGE_GROUPS: GROUP_PREDICTION_REQUIRED_COLUMNS,
    STAGE_KNOCKOUT: KNOCKOUT_PREDICTION_REQUIRED_COLUMNS,
}
RESULTS_REQUIRED_COLUMNS_BY_STAGE = {
    STAGE_GROUPS: GROUP_RESULTS_REQUIRED_COLUMNS,
    STAGE_KNOCKOUT: KNOCKOUT_RESULTS_REQUIRED_COLUMNS,
}

POINTS_EXACT_SCORE = 3
POINTS_RESULT = 1
POINTS_KNOCKOUT_WINNER = 1
