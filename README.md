# FIFA World Cup 2026 - Tracker de predicciones

Aplicación en **Streamlit** para gestionar una quiniela del Mundial 2026 usando archivos Excel.

El proyecto está dividido en dos etapas independientes:

1. **Fase de grupos**: primera oportunidad de predicción.
2. **Fase eliminatoria**: segunda oportunidad, después de conocer los cruces reales.

Esto evita que una mala predicción de clasificados en grupos arruine toda la quiniela.

## Reglas de puntaje

### Fase de grupos

- 3 puntos por marcador exacto.
- 1 punto por resultado correcto: local, empate o visitante.
- 0 puntos si no hay acierto.

### Fase eliminatoria

- 3 puntos por marcador exacto.
- 1 punto por resultado correcto: local, empate o visitante.
- 1 punto adicional por acertar el ganador de la llave.

La columna `ganador_llave_pred` permite manejar partidos definidos por prórroga o penales.

## Estructura del repo

```text
FIFA_WC_26/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── plantilla_grupos.xlsx
│   └── plantilla_eliminatorias.xlsx
├── examples/
└── src/
    ├── __init__.py
    ├── config.py
    ├── dashboard.py
    ├── io_utils.py
    ├── scoring.py
    └── validation.py
```

## Uso local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Uso en Streamlit Cloud

En la configuración de la app usa:

```text
Main file path: app.py
```

## Flujo recomendado

### Antes del torneo

1. Descargar `plantilla_grupos.xlsx`.
2. Enviarla a los participantes.
3. Cada participante diligencia sus marcadores de fase de grupos.
4. Cuando haya resultados reales, cargar el archivo de resultados y las predicciones en la app.

### Después de la fase de grupos

1. Actualizar `plantilla_eliminatorias.xlsx` con los cruces reales.
2. Enviarla a los participantes.
3. Cada participante diligencia marcadores y ganador de llave.
4. Cargar resultados reales y predicciones en la app.

## Fuente del calendario

El calendario base fue construido a partir del calendario oficial de FIFA para el Mundial 2026.

Fuente: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums
