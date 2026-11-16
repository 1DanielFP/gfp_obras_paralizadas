from pathlib import Path
from textwrap import dedent
from html import escape

import pandas as pd
import streamlit as st

from src.nombres_variables import nombre_variable


# ======================================================================================
# 0. AUXILIAR HTML
# ======================================================================================

def limpiar_html(contenido):

    return "\n".join(
        line.strip()
        for line in dedent(contenido).splitlines()
        if line.strip()
    )


# ======================================================================================
# 1. CONFIGURACIÓN GENERAL
# ======================================================================================

st.set_page_config(
    page_title="Riesgo de paralización de obras públicas",
    page_icon="🏗️",
    layout="wide"
)


# ======================================================================================
# 2. ESTILO VISUAL
# ======================================================================================

st.markdown(
    limpiar_html(
        """
        <style>

        /* ------------------------------------------------------------------ */
        /* CONTENEDOR GENERAL                                                  */
        /* ------------------------------------------------------------------ */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }


        /* ------------------------------------------------------------------ */
        /* TÍTULO                                                              */
        /* ------------------------------------------------------------------ */

        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #244C73;
            margin-bottom: 0.20rem;
        }

        .subtitle {
            color: #6B7280;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }


        /* ------------------------------------------------------------------ */
        /* TARJETAS                                                            */
        /* ------------------------------------------------------------------ */

        .info-card {
            background-color: #F8FAFC;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1rem 1.15rem;
            margin-bottom: 0.8rem;
        }

        .risk-card {
            background-color: #EEF5FB;
            border-radius: 16px;
            border-left: 5px solid #2F6F9F;
            padding: 1.5rem;
            text-align: center;
            min-height: 165px;
        }

        .risk-label {
            color: #64748B;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }

        .risk-value {
            color: #1F4E79;
            font-size: 2.7rem;
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 0.5rem;
        }

        .risk-level {
            color: #334155;
            font-size: 1rem;
        }


        /* ------------------------------------------------------------------ */
        /* ESTADO ADMINISTRATIVO                                               */
        /* ------------------------------------------------------------------ */

        .estado-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 0.80rem 1rem;
            margin-top: 0.75rem;
        }

        .estado-label {
            color: #64748B;
            font-size: 0.80rem;
            margin-bottom: 0.15rem;
        }

        .estado-value {
            color: #273142;
            font-size: 1rem;
            font-weight: 650;
        }


        /* ------------------------------------------------------------------ */
        /* ALERTAS DEL MODELO                                                   */
        /* ------------------------------------------------------------------ */

        .model-warning {
            background-color: #FFF4E5;
            border: 1px solid #F5C77A;
            border-left: 5px solid #D98B22;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-top: 0.8rem;
            color: #8A5715;
            font-size: 0.92rem;
            font-weight: 600;
        }

        .model-confirm {
            background-color: #F3F7FB;
            border: 1px solid #D8E3ED;
            border-left: 5px solid #5D7E9D;
            border-radius: 10px;
            padding: 0.70rem 1rem;
            margin-top: 0.8rem;
            color: #4A6178;
            font-size: 0.88rem;
        }


        /* ------------------------------------------------------------------ */
        /* FACTOR PRINCIPAL                                                     */
        /* ------------------------------------------------------------------ */

        .main-factor-card {
            background-color: #F8FAFC;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        .main-factor-label {
            color: #64748B;
            font-size: 0.82rem;
            margin-bottom: 0.15rem;
        }

        .main-factor-title {
            color: #273142;
            font-size: 1.08rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .main-factor-meta {
            color: #64748B;
            font-size: 0.87rem;
        }


        /* ------------------------------------------------------------------ */
        /* FACTORES SHAP                                                        */
        /* ------------------------------------------------------------------ */

        .factor-positive {
            background-color: #FCEAEC;
            border-left: 4px solid #B84A55;
            border-radius: 10px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.7rem;
        }

        .factor-negative {
            background-color: #EAF4ED;
            border-left: 4px solid #3B7A57;
            border-radius: 10px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.7rem;
        }

        .factor-title {
            font-size: 1rem;
            font-weight: 650;
            color: #273142;
            margin-bottom: 0.25rem;
        }

        .factor-meta {
            color: #6B7280;
            font-size: 0.85rem;
        }

        .factor-shap-positive {
            color: #B13E4A;
            font-weight: 600;
        }

        .factor-shap-negative {
            color: #287A4B;
            font-weight: 600;
        }


        /* ------------------------------------------------------------------ */
        /* TÍTULOS                                                             */
        /* ------------------------------------------------------------------ */

        .section-title {
            font-size: 1.45rem;
            font-weight: 700;
            color: #273142;
            margin-top: 0.5rem;
            margin-bottom: 0.8rem;
        }


        /* ------------------------------------------------------------------ */
        /* ETIQUETAS                                                           */
        /* ------------------------------------------------------------------ */

        .label-small {
            color: #64748B;
            font-size: 0.82rem;
            margin-bottom: 0;
        }

        .value-main {
            color: #1F2937;
            font-size: 1rem;
            font-weight: 600;
        }


        /* ------------------------------------------------------------------ */
        /* BOTÓN LATERAL                                                       */
        /* ------------------------------------------------------------------ */

        .sidebar-jump {
            display: block;
            width: 100%;
            box-sizing: border-box;
            text-decoration: none !important;

            background-color: #244C73;
            color: white !important;

            border-radius: 8px;

            padding: 0.72rem 0.85rem;

            margin-top: 0.4rem;
            margin-bottom: 1rem;

            text-align: center;

            font-weight: 600;
            font-size: 0.9rem;

            transition: background-color 0.15s ease;
        }

        .sidebar-jump:hover {
            background-color: #1B3E5E;
            color: white !important;
        }

        </style>
        """
    ),
    unsafe_allow_html=True
)


# ======================================================================================
# 3. RUTAS
# ======================================================================================

BASE_DIR = Path(__file__).resolve().parent


RUTA_PREDICCIONES = (
    BASE_DIR
    / "datos"
    / "predicciones_cui.parquet"
)


RUTA_SHAP = (
    BASE_DIR
    / "datos"
    / "explicaciones_shap.parquet"
)


RUTA_BLOQUES = (
    BASE_DIR
    / "datos"
    / "shap_por_bloque.parquet"
)


# ======================================================================================
# 4. FORMATO DE VALORES
# ======================================================================================

def formatear_valor(valor):

    if pd.isna(valor):

        return "Sin información"


    texto = str(
        valor
    ).strip()


    if texto.lower() in [
        "nan",
        "none",
        "<na>",
        ""
    ]:

        return "Sin información"


    try:

        numero = float(
            texto
        )


        if pd.isna(
            numero
        ):

            return "Sin información"


        if numero.is_integer():

            return f"{int(numero)}"


        return f"{numero:.2f}"


    except (
        ValueError,
        TypeError
    ):

        pass


    return texto


# ======================================================================================
# 5. FORMATO ESPECIAL PARA CÓDIGOS
#
# Evita que aparezcan cosas como:
#
# 1234567.0
#
# ======================================================================================

def formatear_codigo(
    valor
):

    if pd.isna(
        valor
    ):

        return None


    texto = str(
        valor
    ).strip()


    if texto.lower() in [
        "",
        "nan",
        "none",
        "<na>"
    ]:

        return None


    try:

        numero = float(
            texto
        )


        if numero.is_integer():

            return str(
                int(
                    numero
                )
            )


    except (
        ValueError,
        TypeError
    ):

        pass


    return texto


# ======================================================================================
# 6. ESTADO ADMINISTRATIVO
# ======================================================================================

def obtener_estado_administrativo(
    fila
):

    candidatos = [

        "op_estado_ejecucion_infobras",

        "op_opb_estado_final",

        "op_ESTADO"

    ]


    for variable in candidatos:

        if variable not in fila.index:

            continue


        valor = fila.get(
            variable
        )


        if pd.isna(
            valor
        ):

            continue


        texto = str(
            valor
        ).strip()


        if texto.lower() in [
            "",
            "nan",
            "none",
            "<na>"
        ]:

            continue


        return (
            texto,
            variable
        )


    return (
        "Sin información",
        None
    )


# ======================================================================================
# 7. CARGA DE DATOS
# ======================================================================================

@st.cache_data(show_spinner="Cargando información de obras...")
def cargar_datos():
    predicciones = pd.read_parquet(RUTA_PREDICCIONES)
    shap = pd.read_parquet(RUTA_SHAP)
    bloques = pd.read_parquet(RUTA_BLOQUES)
    for tabla in (predicciones, shap, bloques):
        tabla["id_cui_std"] = tabla["id_cui_std"].astype("string")
    return predicciones, shap, bloques


predicciones, shap_largo, shap_bloques = cargar_datos()


@st.cache_data(show_spinner=False)
def preparar_indices(predicciones, shap_largo, shap_bloques):
    # Se calculan una sola vez; no se filtran tablas enteras por cada opción.
    ids = predicciones["_id_fila_shap"].dropna().drop_duplicates().tolist()
    primera_fila = predicciones.drop_duplicates("_id_fila_shap").set_index("_id_fila_shap")
    etiquetas = {}
    for id_fila in ids:
        fila = primera_fila.loc[id_fila]
        cui = formatear_codigo(fila.get("id_cui_std"))
        infobras = formatear_codigo(fila.get("id_codigo_infobras"))
        etiquetas[id_fila] = " · ".join(
            x for x in (f"CUI {cui}" if cui else "", f"INFOBRAS {infobras}" if infobras else "") if x
        ) or f"Registro {id_fila}"
    pos_pred = {k: v for k, v in predicciones.groupby("_id_fila_shap", sort=False).indices.items()}
    pos_shap = {k: v for k, v in shap_largo.groupby("_id_fila_shap", sort=False).indices.items()}
    pos_bloques = {k: v for k, v in shap_bloques.groupby("_id_fila_shap", sort=False).indices.items()}
    return ids, etiquetas, pos_pred, pos_shap, pos_bloques


# ======================================================================================
# 8. VALIDACIONES
# ======================================================================================

columnas_necesarias_predicciones = [

    "id_cui_std",

    "prob_paralizacion",

    "prediccion_clase",

    "_id_fila_shap"

]


faltantes_predicciones = [

    columna

    for columna
    in columnas_necesarias_predicciones

    if columna
    not in
    predicciones.columns

]


if faltantes_predicciones:

    st.error(
        "Faltan columnas necesarias en predicciones_cui.parquet: "
        f"{faltantes_predicciones}"
    )

    st.stop()


# ======================================================================================
# 9. NORMALIZACIÓN REALIZADA EN LA CARGA CACHEADA
# ======================================================================================


# 10. BARRA LATERAL
# ======================================================================================

with st.sidebar:
    st.markdown("## Navegación")
    st.markdown(
        '[Ver variables sustantivas y contextuales](#variables-sustantivas-y-contextuales)'
    )
    st.caption("Ir a la comparación de factores sustantivos y contextuales.")


# ======================================================================================
# 11. TÍTULO
# ======================================================================================

st.markdown(
    limpiar_html(
        """
        <div class="main-title">
            Riesgo de paralización de obras públicas
        </div>
        """
    ),
    unsafe_allow_html=True
)


st.markdown(
    limpiar_html(
        """
        <div class="subtitle">
            Explorador predictivo basado en características de la inversión,
            capacidad de ejecución, proceso de selección, contratistas,
            gestión institucional y avance físico-financiero.
        </div>
        """
    ),
    unsafe_allow_html=True
)


# ======================================================================================
# 12. ETIQUETA DEL SELECTOR
#
# IMPORTANTE:
#
# El usuario solamente ve:
#
# CUI: XXXXX
# Código INFOBRAS: XXXXX
#
# No mostramos el nombre de la obra.
#
# Como el selectbox permite búsqueda:
#
# - puede escribir el CUI
# - puede escribir el Código INFOBRAS
# ======================================================================================

lista_ids, etiquetas_obras, pos_pred, pos_shap, pos_bloques = preparar_indices(
    predicciones, shap_largo, shap_bloques
)

id_seleccionado = st.selectbox(
    "Buscar obra por CUI o Código INFOBRAS",
    options=lista_ids,
    format_func=etiquetas_obras.__getitem__,
    help="Escriba el CUI o el Código INFOBRAS para localizar una obra.",
)


# ======================================================================================
# 14. FILTRAR OBRA
# ======================================================================================

obra = predicciones.iloc[pos_pred[id_seleccionado][0]]


cui_seleccionado = formatear_codigo(
    obra.get(
        "id_cui_std"
    )
)


# ======================================================================================
# 15. FILTRAR SHAP
# ======================================================================================

shap_obra = shap_largo.iloc[pos_shap.get(id_seleccionado, [])].copy()
bloques_obra = shap_bloques.iloc[pos_bloques.get(id_seleccionado, [])].copy()


# ======================================================================================
# 16. NOMBRES LEGIBLES
# ======================================================================================

shap_obra[
    "nombre_variable"
] = (

    shap_obra[
        "variable"
    ]

    .apply(
        nombre_variable
    )

)


# ======================================================================================
# 17. PROBABILIDAD
# ======================================================================================

probabilidad = float(
    obra[
        "prob_paralizacion"
    ]
)


prediccion_clase = int(
    obra[
        "prediccion_clase"
    ]
)


if probabilidad >= 0.70:

    nivel_riesgo = "Alto"


elif probabilidad >= 0.40:

    nivel_riesgo = "Medio"


else:

    nivel_riesgo = "Bajo"


# ======================================================================================
# 18. CLASIFICACIÓN OBSERVADA
# ======================================================================================

estado_real = obra.get(
    "op_estado_dummy",
    None
)


try:

    estado_real = int(
        float(
            estado_real
        )
    )


except (
    TypeError,
    ValueError
):

    estado_real = None


# ======================================================================================
# 19. ESTADO INFOBRAS
# ======================================================================================

estado_administrativo, fuente_estado = (

    obtener_estado_administrativo(
        obra
    )

)


# ======================================================================================
# 20. CABECERA
# ======================================================================================

st.divider()


col_info, col_riesgo = st.columns(
    [
        2.1,
        1
    ]
)


# ======================================================================================
# 21. INFORMACIÓN PRINCIPAL
# ======================================================================================

with col_info:

    nombre_obra = obra.get(
        "op_nombre_obra",
        None
    )


    if pd.isna(
        nombre_obra
    ):

        nombre_obra = obra.get(
            "op_nombre_obra_op",
            "Obra seleccionada"
        )


    # ----------------------------------------------------------------------------------
    # AQUÍ SÍ MOSTRAMOS EL NOMBRE COMPLETO
    # ----------------------------------------------------------------------------------

    st.subheader(
        formatear_valor(
            nombre_obra
        )
    )


    codigo_infobras = formatear_codigo(
        obra.get(
            "id_codigo_infobras",
            None
        )
    )


    entidad = obra.get(
        "op_entidad_op",
        None
    )


    if pd.isna(
        entidad
    ):

        entidad = obra.get(
            "sea_entidad",
            None
        )


    st.markdown(
        limpiar_html(
            f"""
            <div class="info-card">

                <div class="label-small">
                    CUI
                </div>

                <div class="value-main">
                    {formatear_valor(cui_seleccionado)}
                </div>

                <br>

                <div class="label-small">
                    Código INFOBRAS
                </div>

                <div class="value-main">
                    {formatear_valor(codigo_infobras)}
                </div>

                <br>

                <div class="label-small">
                    Entidad
                </div>

                <div class="value-main">
                    {formatear_valor(entidad)}
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True
    )


    # ----------------------------------------------------------------------------------
    # ESTADO INFOBRAS
    # ----------------------------------------------------------------------------------

    st.markdown(
        limpiar_html(
            f"""
            <div class="estado-card">

                <div class="estado-label">
                    Estado de ejecución registrado
                </div>

                <div class="estado-value">
                    {formatear_valor(estado_administrativo)}
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True
    )


# ======================================================================================
# 22. RIESGO
# ======================================================================================

with col_riesgo:

    st.markdown(
        limpiar_html(
            f"""
            <div class="risk-card">

                <div class="risk-label">
                    Probabilidad estimada de paralización
                </div>

                <div class="risk-value">
                    {probabilidad:.1%}
                </div>

                <div class="risk-level">
                    Nivel de riesgo:
                    <b>{nivel_riesgo}</b>
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True
    )


    # ----------------------------------------------------------------------------------
    # NO PARALIZADA OBSERVADA + MODELO PREDICE PARALIZACIÓN
    # ----------------------------------------------------------------------------------

    if (
        estado_real == 0
        and
        prediccion_clase == 1
    ):

        st.markdown(
            limpiar_html(
                """
                <div class="model-warning">
                    ⚠ El modelo identifica que esta obra puede paralizarse.
                </div>
                """
            ),
            unsafe_allow_html=True
        )


    # ----------------------------------------------------------------------------------
    # COINCIDENCIA EN PARALIZACIÓN
    # ----------------------------------------------------------------------------------

    elif (
        estado_real == 1
        and
        prediccion_clase == 1
    ):

        st.markdown(
            limpiar_html(
                """
                <div class="model-confirm">
                    La predicción del modelo coincide con la condición
                    observada de paralización.
                </div>
                """
            ),
            unsafe_allow_html=True
        )


# ======================================================================================
# 23. INFORMACIÓN DE LA OBRA
# ======================================================================================

st.markdown(
    limpiar_html(
        """
        <div class="section-title">
            Información de la obra
        </div>
        """
    ),
    unsafe_allow_html=True
)


c1, c2, c3, c4 = st.columns(
    4
)


with c1:

    st.markdown(
        "**Departamento**"
    )

    st.write(
        formatear_valor(
            obra.get(
                "op_departamento",
                None
            )
        )
    )


with c2:

    st.markdown(
        "**Provincia**"
    )

    st.write(
        formatear_valor(
            obra.get(
                "op_provincia",
                None
            )
        )
    )


with c3:

    st.markdown(
        "**Distrito**"
    )

    st.write(
        formatear_valor(
            obra.get(
                "op_distrito",
                None
            )
        )
    )


with c4:

    st.markdown(
        "**Año de convocatoria**"
    )

    st.write(
        formatear_valor(
            obra.get(
                "sea_anio_convocatoria",
                None
            )
        )
    )


# ======================================================================================
# 24. SEGUNDA LÍNEA
# ======================================================================================

c5, c6, c7, c8 = st.columns(
    4
)


with c5:

    st.markdown(
        "**Nivel de gobierno**"
    )

    st.write(
        formatear_valor(
            obra.get(
                "op_nivel_gobierno",
                None
            )
        )
    )


with c6:

    st.markdown(
        "**Sector**"
    )

    st.write(
        formatear_valor(
            obra.get(
                "op_sector",
                None
            )
        )
    )


with c7:

    st.markdown(
        "**Clasificación observada**"
    )


    if estado_real == 1:

        st.write(
            "Paralizada"
        )


    elif estado_real == 0:

        st.write(
            "No paralizada"
        )


    else:

        st.write(
            "Sin información"
        )


with c8:

    st.markdown(
        "**Predicción del modelo**"
    )


    if prediccion_clase == 1:

        st.write(
            "Paralizada"
        )


    else:

        st.write(
            "No paralizada"
        )


# ======================================================================================
# 25. PRINCIPAL FACTOR
# ======================================================================================

st.divider()


st.markdown(
    limpiar_html(
        """
        <div class="section-title">
            Principal factor identificado por el modelo
        </div>
        """
    ),
    unsafe_allow_html=True
)


factor_principal = obra.get(
    "factor_principal",
    None
)


bloque_factor_principal = obra.get(
    "bloque_factor_principal",
    None
)


direccion_factor_principal = obra.get(
    "direccion_factor_principal",
    None
)


valor_factor_principal = obra.get(
    "valor_factor_principal",
    None
)


if pd.notna(
    factor_principal
):

    st.markdown(
        limpiar_html(
            f"""
            <div class="main-factor-card">

                <div class="main-factor-label">
                    Factor con mayor contribución sustantiva local
                </div>

                <div class="main-factor-title">
                    {nombre_variable(factor_principal)}
                </div>

                <div class="main-factor-meta">

                    Bloque:
                    {formatear_valor(bloque_factor_principal)}

                    &nbsp;·&nbsp;

                    Valor observado:
                    {formatear_valor(valor_factor_principal)}

                    &nbsp;·&nbsp;

                    Dirección:
                    {formatear_valor(direccion_factor_principal)}

                </div>

            </div>
            """
        ),
        unsafe_allow_html=True
    )


# ======================================================================================
# 26. FACTORES SHAP
# ======================================================================================

st.markdown(
    limpiar_html(
        """
        <div class="section-title">
            ¿Qué factores explican esta predicción?
        </div>
        """
    ),
    unsafe_allow_html=True
)


shap_sustantivo = (

    shap_obra[
        shap_obra[
            "tipo"
        ]
        ==
        "Sustantiva"
    ]

    .copy()

)


# ======================================================================================
# 27. TOP POSITIVOS
# ======================================================================================

aumentan = (

    shap_sustantivo[
        shap_sustantivo[
            "shap"
        ]
        >
        0
    ]

    .sort_values(
        "shap",
        ascending=False
    )

    .head(
        10
    )

)


# ======================================================================================
# 28. TOP NEGATIVOS
# ======================================================================================

reducen = (

    shap_sustantivo[
        shap_sustantivo[
            "shap"
        ]
        <
        0
    ]

    .sort_values(
        "shap",
        ascending=True
    )

    .head(
        10
    )

)


col_aumentan, col_reducen = st.columns(
    2
)


# ======================================================================================
# 29. FACTORES QUE AUMENTAN
# ======================================================================================

with col_aumentan:

    st.markdown(
        "### ↑ Factores que aumentan el riesgo"
    )


    if len(
        aumentan
    ) == 0:

        st.write(
            "No se identificaron aportes positivos relevantes."
        )


    else:

        for _, fila in aumentan.iterrows():

            nombre = fila[
                "nombre_variable"
            ]


            valor = formatear_valor(
                fila[
                    "valor_original"
                ]
            )


            shap_valor = float(
                fila[
                    "shap"
                ]
            )


            bloque = fila[
                "bloque"
            ]


            st.markdown(
                limpiar_html(
                    f"""
                    <div class="factor-positive">

                        <div class="factor-title">
                            {nombre}
                        </div>

                        <div class="factor-meta">

                            Bloque: {bloque}

                            &nbsp;·&nbsp;

                            Valor observado: {valor}

                            &nbsp;·&nbsp;

                            <span class="factor-shap-positive">
                                SHAP: +{shap_valor:.3f}
                            </span>

                        </div>

                    </div>
                    """
                ),
                unsafe_allow_html=True
            )


# ======================================================================================
# 30. FACTORES QUE REDUCEN
# ======================================================================================

with col_reducen:

    st.markdown(
        "### ↓ Factores que reducen el riesgo"
    )


    if len(
        reducen
    ) == 0:

        st.write(
            "No se identificaron aportes negativos relevantes."
        )


    else:

        for _, fila in reducen.iterrows():

            nombre = fila[
                "nombre_variable"
            ]


            valor = formatear_valor(
                fila[
                    "valor_original"
                ]
            )


            shap_valor = float(
                fila[
                    "shap"
                ]
            )


            bloque = fila[
                "bloque"
            ]


            st.markdown(
                limpiar_html(
                    f"""
                    <div class="factor-negative">

                        <div class="factor-title">
                            {nombre}
                        </div>

                        <div class="factor-meta">

                            Bloque: {bloque}

                            &nbsp;·&nbsp;

                            Valor observado: {valor}

                            &nbsp;·&nbsp;

                            <span class="factor-shap-negative">
                                SHAP: {shap_valor:.3f}
                            </span>

                        </div>

                    </div>
                    """
                ),
                unsafe_allow_html=True
            )


# ======================================================================================
# 31. APORTE POR BLOQUE
# ======================================================================================

st.divider()


st.markdown(
    limpiar_html(
        """
        <div class="section-title">
            Aporte agregado por bloque
        </div>
        """
    ),
    unsafe_allow_html=True
)


columnas_bloques = [

    "bloque",

    "shap_bloque",

    "shap_abs_bloque",

    "direccion_bloque"

]


if (
    "importancia_relativa_bloque_pct"
    in bloques_obra.columns
):

    columnas_bloques.append(
        "importancia_relativa_bloque_pct"
    )


bloques_tabla = (

    bloques_obra[
        columnas_bloques
    ]

    .copy()

)


bloques_tabla[
    "shap_bloque"
] = (

    bloques_tabla[
        "shap_bloque"
    ]

    .round(
        3
    )

)


bloques_tabla[
    "shap_abs_bloque"
] = (

    bloques_tabla[
        "shap_abs_bloque"
    ]

    .round(
        3
    )

)


if (
    "importancia_relativa_bloque_pct"
    in bloques_tabla.columns
):

    bloques_tabla[
        "importancia_relativa_bloque_pct"
    ] = (

        bloques_tabla[
            "importancia_relativa_bloque_pct"
        ]

        .round(
            1
        )

    )


rename_bloques = {

    "bloque":
        "Bloque",

    "shap_bloque":
        "Aporte neto",

    "shap_abs_bloque":
        "Magnitud total",

    "direccion_bloque":
        "Dirección",

    "importancia_relativa_bloque_pct":
        "Importancia local (%)"

}


bloques_tabla = (

    bloques_tabla

    .sort_values(
        "shap_abs_bloque",
        ascending=False
    )

    .rename(
        columns=
            rename_bloques
    )

)


st.dataframe(
    bloques_tabla,
    width="stretch",
    hide_index=True
)


# ======================================================================================
# 32. VARIABLES SUSTANTIVAS Y CONTEXTUALES
# ======================================================================================

st.divider()
st.header("Variables sustantivas y contextuales", anchor="variables-sustantivas-y-contextuales")
st.caption(
    "Las variables sustantivas describen características directamente interpretables "
    "de la obra y su ejecución; las contextuales caracterizan su entorno territorial e institucional."
)

columnas_detalle = [
    "tipo", "bloque", "nombre_variable", "valor_original", "shap", "direccion", "ranking_local"
]
tabla_detalle = shap_obra[columnas_detalle].sort_values("ranking_local").rename(columns={
    "tipo": "Tipo", "bloque": "Bloque", "nombre_variable": "Factor predictivo",
    "valor_original": "Valor observado", "shap": "Aporte SHAP",
    "direccion": "Dirección", "ranking_local": "Ranking"
})
tabla_detalle["Valor observado"] = tabla_detalle["Valor observado"].map(formatear_valor)
tabla_detalle["Aporte SHAP"] = pd.to_numeric(tabla_detalle["Aporte SHAP"], errors="coerce").round(3)

config_tabla = {
    "Aporte SHAP": st.column_config.NumberColumn("Aporte SHAP", format="%.3f"),
    "Ranking": st.column_config.NumberColumn("Ranking", format="%d"),
}

st.subheader("Predictores con interpretación sustantiva")
st.caption("Características de inversión, ejecución, contratación y avance de la obra.")
st.dataframe(
    tabla_detalle.loc[tabla_detalle["Tipo"] == "Sustantiva"].drop(columns="Tipo"),
    width="stretch", hide_index=True, column_config=config_tabla,
)

st.subheader("Predictores contextuales")
st.caption("Características del contexto territorial e institucional de la obra.")
st.dataframe(
    tabla_detalle.loc[tabla_detalle["Tipo"] == "Contextual"].drop(columns="Tipo"),
    width="stretch", hide_index=True, column_config=config_tabla,
)


# ======================================================================================
# 36. NOTA METODOLÓGICA
# ======================================================================================

st.divider()


st.info(
    "La probabilidad corresponde a una predicción del modelo XGBoost. "
    "Los valores SHAP muestran qué variables empujan la predicción hacia "
    "un mayor o menor riesgo de paralización. "
    "La clasificación administrativa observada y el estado registrado en INFOBRAS "
    "se muestran únicamente como información descriptiva y no se utilizan como "
    "predictores del modelo. "
    "Los aportes SHAP explican el comportamiento del modelo para cada obra "
    "y no deben interpretarse como efectos causales."
)