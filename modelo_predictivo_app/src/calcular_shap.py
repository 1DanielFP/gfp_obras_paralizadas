# ======================================================================================
# CALCULAR SHAP PARA LA APP
#
# Modelo:
# XGBoost - Especificación S3 final
#
# Fuente:
# datos/df_final_minilab.xlsx
#
# Genera:
#
# datos/explicaciones_shap.parquet
# datos/shap_por_bloque.parquet
# datos/predicciones_cui.parquet
#
# IMPORTANTE:
#
# - Usa exactamente las variables guardadas en configuracion_modelo.json
# - NO vuelve a entrenar el modelo
# - NO usa variables de disponibilidad
# - NO usa op_n_reportes
# - Agrega las dummies categóricas nuevamente a la variable original
# - Conserva estados reales de la obra para mostrarlos en la app
#
# SHAP:
#
# valor positivo -> aumenta predicción hacia PARALIZADA
# valor negativo -> reduce predicción hacia PARALIZADA
# ======================================================================================


# ======================================================================================
# 0. LIBRERÍAS
# ======================================================================================

from pathlib import Path

import json
import joblib
import numpy as np
import pandas as pd
import shap


# ======================================================================================
# 1. RUTAS
# ======================================================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)


RUTA_DATOS = (

    BASE_DIR
    / "datos"
    / "df_final_minilab.xlsx"

)


RUTA_MODELO = (

    BASE_DIR
    / "modelo"
    / "modelo_xgb_pipeline.pkl"

)


RUTA_CONFIG = (

    BASE_DIR
    / "modelo"
    / "configuracion_modelo.json"

)


RUTA_SALIDA = (

    BASE_DIR
    / "datos"

)


RUTA_SALIDA.mkdir(

    parents=True,

    exist_ok=True

)


# ======================================================================================
# 2. CARGAR BASE
# ======================================================================================

df = pd.read_excel(
    RUTA_DATOS
)


print(
    "=" * 100
)

print(
    "BASE PARA SHAP"
)

print(
    "=" * 100
)


print(
    f"Archivo: {RUTA_DATOS}"
)


print(
    f"Filas: {df.shape[0]}"
)


print(
    f"Columnas: {df.shape[1]}"
)


# ======================================================================================
# 3. CARGAR PIPELINE
# ======================================================================================

pipeline = joblib.load(
    RUTA_MODELO
)


print(
    "\nPipeline cargado correctamente."
)


# ======================================================================================
# 4. CARGAR CONFIGURACIÓN
# ======================================================================================

with open(

    RUTA_CONFIG,

    "r",

    encoding="utf-8"

) as f:

    config = json.load(
        f
    )


TARGET = config[
    "target"
]


GROUP = config[
    "group"
]


variables_categoricas = config[
    "variables_categoricas"
]


variables_numericas = config[
    "variables_numericas"
]


variables_modelo = config[
    "variables_modelo"
]


# ======================================================================================
# 5. BLOQUES GUARDADOS EN CONFIGURACIÓN
# ======================================================================================

variables_mef = config.get(
    "variables_mef",
    []
)


variables_ue = config.get(
    "variables_ue",
    []
)


variables_desbalance = config.get(
    "variables_desbalance",
    []
)


variables_sunat = config.get(
    "variables_sunat",
    []
)


variables_renamu = config.get(
    "variables_renamu",
    []
)


variables_igeip = config.get(
    "variables_igeip",
    []
)


variables_seleccion = config.get(
    "variables_seleccion",
    []
)


variables_contractuales = config.get(
    "variables_contractuales",
    []
)


variables_avance = config.get(
    "variables_avance",
    []
)


VARIABLES_ESTADO_APP = config.get(
    "variables_estado_app",
    []
)


VARIABLES_IDENTIFICACION_APP = config.get(
    "variables_identificacion_app",
    []
)


# ======================================================================================
# 6. CONTROLES DE CONFIGURACIÓN
# ======================================================================================

print(
    "\n"
    + "=" * 100
)

print(
    "CONFIGURACIÓN DEL MODELO"
)

print(
    "=" * 100
)


print(
    "Variables categóricas:",
    len(
        variables_categoricas
    )
)


print(
    "Variables numéricas:",
    len(
        variables_numericas
    )
)


print(
    "Variables totales:",
    len(
        variables_modelo
    )
)


assert (
    len(
        variables_categoricas
    )
    ==
    5
)


assert (
    len(
        variables_numericas
    )
    ==
    55
)


assert (
    len(
        variables_modelo
    )
    ==
    60
)


assert (
    "op_n_reportes"
    not in
    variables_modelo
)


print(
    "OK: modelo S3 final de 60 variables."
)


print(
    "OK: op_n_reportes no entra a SHAP."
)


# ======================================================================================
# 7. VALIDAR VARIABLES EN LA BASE
# ======================================================================================

faltantes = [

    variable

    for variable
    in (
        variables_modelo
        +
        [
            GROUP
        ]
    )

    if variable
    not in
    df.columns

]


if faltantes:

    raise ValueError(

        "Faltan variables necesarias en "
        f"df_final_minilab.xlsx: {faltantes}"

    )


# ======================================================================================
# 8. NORMALIZAR CUI
# ======================================================================================

df[
    GROUP
] = (

    pd.to_numeric(

        df[
            GROUP
        ],

        errors="coerce"

    )

    .astype(
        "Int64"
    )

    .astype(
        "string"
    )

)


# ======================================================================================
# 9. NORMALIZAR NIVEL DE GOBIERNO
#
# Exactamente igual que preparar_modelo.py
# ======================================================================================

def normalizar_nivel_gobierno(
    valor
):

    if pd.isna(
        valor
    ):

        return np.nan


    valor = (

        str(valor)
        .strip()
        .upper()

    )


    if any(

        x in valor

        for x in [

            "LOCAL",

            "MUNICIPAL",

            "MUNICIPALIDAD",

            "GOBIERNO LOCAL"

        ]

    ):

        return "LOCAL"


    if any(

        x in valor

        for x in [

            "REGIONAL",

            "REGION",

            "GOBIERNO REGIONAL"

        ]

    ):

        return "REGIONAL"


    if any(

        x in valor

        for x in [

            "NACIONAL",

            "CENTRAL",

            "GOBIERNO NACIONAL"

        ]

    ):

        return "NACIONAL"


    return np.nan


df[
    "op_nivel_gobierno"
] = (

    df[
        "op_nivel_gobierno"
    ]

    .apply(
        normalizar_nivel_gobierno
    )

)


# ======================================================================================
# 10. NORMALIZAR SALDO
# ======================================================================================

def normalizar_saldo(
    valor
):

    if pd.isna(
        valor
    ):

        return np.nan


    valor = (

        str(valor)
        .strip()
        .upper()

    )


    if valor in [

        "SI",

        "SÍ",

        "1",

        "TRUE"

    ]:

        return "SI"


    if valor in [

        "NO",

        "0",

        "FALSE"

    ]:

        return "NO"


    return valor


df[
    "op_es_saldo_obra"
] = (

    df[
        "op_es_saldo_obra"
    ]

    .apply(
        normalizar_saldo
    )

)


# ======================================================================================
# 11. HOMOLOGAR CATEGÓRICAS
#
# Tiene que ser idéntico a preparar_modelo.py.
# ======================================================================================

def homologar_categoricas(
    dataframe,
    variables
):

    resultado = (
        dataframe
        .copy()
    )


    for variable in variables:

        resultado[
            variable
        ] = (

            resultado[
                variable
            ]

            .apply(
                lambda x:
                    str(x).strip()
                    if pd.notna(x)
                    else np.nan
            )

        )


    return resultado


df = homologar_categoricas(

    df,

    variables_categoricas

)


# ======================================================================================
# 12. ASEGURAR NUMÉRICAS
# ======================================================================================

for variable in variables_numericas:

    df[
        variable
    ] = pd.to_numeric(

        df[
            variable
        ],

        errors="coerce"

    )


# ======================================================================================
# 13. FILTRAR CASOS EXPLICABLES
#
# Solo necesitamos CUI válido.
#
# No necesitamos target para generar una predicción.
# ======================================================================================

mask = (

    df[
        GROUP
    ]
    .notna()

)


dm = (

    df.loc[
        mask
    ]

    .copy()

    .reset_index(
        drop=True
    )

)


# ======================================================================================
# 14. IDENTIFICADOR INTERNO DE FILA
#
# Nos permite mantener cada observación perfectamente identificada
# incluso si un CUI apareciera más de una vez.
# ======================================================================================

dm[
    "_id_fila_shap"
] = np.arange(
    len(
        dm
    )
)


print(
    "\nCasos a explicar:",
    len(
        dm
    )
)


# ======================================================================================
# 15. MATRIZ X
# ======================================================================================

X = (

    dm[
        variables_modelo
    ]

    .copy()

)


# ======================================================================================
# 16. PREDICCIÓN
# ======================================================================================

probabilidades = (

    pipeline

    .predict_proba(
        X
    )[
        :,
        1
    ]

)


dm[
    "prob_paralizacion"
] = probabilidades


dm[
    "prediccion_clase"
] = (

    probabilidades
    >=
    0.5

).astype(int)


dm[
    "prediccion_etiqueta"
] = np.where(

    dm[
        "prediccion_clase"
    ]
    ==
    1,

    "Paralizada",

    "No paralizada"

)


# ======================================================================================
# 17. CONDICIÓN REAL
#
# Solo para mostrar en la app.
#
# NO afecta la predicción.
# ======================================================================================

if TARGET in dm.columns:

    target_numeric = pd.to_numeric(

        dm[
            TARGET
        ],

        errors="coerce"

    )


    dm[
        "estado_real_etiqueta"
    ] = np.select(

        [

            target_numeric
            ==
            1,

            target_numeric
            ==
            0

        ],

        [

            "Paralizada",

            "No paralizada"

        ],

        default=
            "Sin clasificación"

    )


# ======================================================================================
# 18. EXTRAER PREPROCESADOR Y XGBOOST
#
# El pipeline nuevo usa:
#
# "prep"
# "modelo"
# ======================================================================================

preprocesador = pipeline.named_steps[
    "prep"
]


modelo = pipeline.named_steps[
    "modelo"
]


# ======================================================================================
# 19. TRANSFORMAR X
# ======================================================================================

X_transformado = (

    preprocesador

    .transform(
        X
    )

)


if hasattr(
    X_transformado,
    "toarray"
):

    X_transformado = (
        X_transformado
        .toarray()
    )


X_transformado = np.asarray(
    X_transformado
)


print(
    "Observaciones:",
    X_transformado.shape[
        0
    ]
)


print(
    "Variables transformadas:",
    X_transformado.shape[
        1
    ]
)


# ======================================================================================
# 20. CALCULAR SHAP
# ======================================================================================

print(
    "\nCalculando SHAP..."
)


explainer = shap.TreeExplainer(
    modelo
)


shap_values = explainer.shap_values(
    X_transformado
)


# --------------------------------------------------------------------------------------
# Compatibilidad SHAP
# --------------------------------------------------------------------------------------

if isinstance(
    shap_values,
    list
):

    if len(
        shap_values
    ) == 2:

        shap_values = shap_values[
            1
        ]

    else:

        shap_values = shap_values[
            -1
        ]


shap_values = np.asarray(
    shap_values
)


# --------------------------------------------------------------------------------------
# Algunas versiones:
#
# observaciones x features x clases
# --------------------------------------------------------------------------------------

if shap_values.ndim == 3:

    if shap_values.shape[
        2
    ] >= 2:

        shap_values = shap_values[
            :,
            :,
            1
        ]

    else:

        shap_values = shap_values[
            :,
            :,
            0
        ]


assert (
    shap_values.ndim
    ==
    2
), (
    f"Shape SHAP inesperado: {shap_values.shape}"
)


print(
    "Shape SHAP:",
    shap_values.shape
)


# ======================================================================================
# 21. MAPEAR DUMMIES A VARIABLE ORIGINAL
# ======================================================================================

onehot = (

    preprocesador

    .named_transformers_[
        "cat"
    ]

    .named_steps[
        "onehot"
    ]

)


categorias = (
    onehot.categories_
)


mapa_columnas = []

posicion = 0


# ======================================================================================
# 22. CATEGÓRICAS
# ======================================================================================

for variable, categorias_variable in zip(

    variables_categoricas,

    categorias

):

    n_categorias = len(
        categorias_variable
    )


    indices = list(

        range(

            posicion,

            posicion
            +
            n_categorias

        )

    )


    mapa_columnas.append(
        {

            "variable":
                variable,

            "indices":
                indices

        }
    )


    posicion += (
        n_categorias
    )


# ======================================================================================
# 23. NUMÉRICAS
# ======================================================================================

for variable in variables_numericas:

    mapa_columnas.append(
        {

            "variable":
                variable,

            "indices":
                [
                    posicion
                ]

        }
    )


    posicion += 1


# ======================================================================================
# 24. CONTROL DE MAPEO
# ======================================================================================

assert (
    posicion
    ==
    shap_values.shape[
        1
    ]
), (
    f"Mapeo incorrecto: {posicion} columnas mapeadas "
    f"vs {shap_values.shape[1]} columnas SHAP."
)


print(
    "OK: mapeo OneHot -> variable original correcto."
)


# ======================================================================================
# 25. AGREGAR SHAP POR VARIABLE ORIGINAL
#
# Las dummies de cada categórica se suman por observación.
# ======================================================================================

shap_original = {}


for elemento in mapa_columnas:

    variable = elemento[
        "variable"
    ]


    indices = elemento[
        "indices"
    ]


    shap_variable = (

        shap_values[
            :,
            indices
        ]

        .sum(
            axis=1
        )

    )


    shap_original[
        variable
    ] = (
        shap_variable
    )


# ======================================================================================
# 26. VARIABLES CONTEXTUALES
#
# Saldo de obra se considera característica sustantiva de la obra,
# no control contextual.
# ======================================================================================

variables_contextuales = [

    "op_nivel_gobierno",

    "op_departamento",

    "modalidad_general",

    "mecanismo_ejecucion"

]


# ======================================================================================
# 27. IDENTIFICAR TIPO
# ======================================================================================

def identificar_tipo(
    variable
):

    if variable in variables_contextuales:

        return "Contextual"


    return "Sustantiva"


# ======================================================================================
# 28. IDENTIFICAR BLOQUE
# ======================================================================================

def identificar_bloque(
    variable
):

    if variable in variables_avance:

        return "AVANCE"


    if variable in variables_contractuales:

        return "CONTRACTUAL"


    if variable in variables_seleccion:

        return "SELECCION"


    if variable in variables_igeip:

        return "IGEIP"


    if variable in variables_renamu:

        return "RENAMU"


    if variable in variables_sunat:

        return "SUNAT"


    if variable in variables_desbalance:

        return "DESBALANCE"


    if variable in variables_ue:

        return "UE"


    if variable in variables_mef:

        return "MEF"


    if variable == "op_es_saldo_obra":

        return "OBRA"


    if variable in variables_contextuales:

        return "CONTEXTO"


    return "OTRO"


# ======================================================================================
# 29. COLUMNAS DE IDENTIFICACIÓN PARA LA APP
# ======================================================================================

columnas_identificacion = [

    "_id_fila_shap",

    "id_codigo_infobras",

    "id_cui_std",

    "id_cui",

    "id_nomenclatura",

    "op_nombre_obra",

    "op_nombre_obra_op",

    "sea_entidad",

    "op_entidad_op",

    "ENTIDAD",

    "NOMBRE_UEI",

    "op_nivel_gobierno",

    "op_sector",

    "op_departamento",

    "op_provincia",

    "op_distrito",

    "sea_anio_convocatoria",

    TARGET,

    "estado_real_etiqueta",

    "op_estado_ejecucion_infobras",

    "op_opb_estado_final",

    "op_ESTADO"

]


columnas_identificacion = [

    columna

    for columna
    in columnas_identificacion

    if columna
    in dm.columns

]


# ======================================================================================
# 30. TABLA SHAP LARGA
#
# Una fila por:
#
# obra x variable
#
# 2996 x 60 ≈ 179 760 filas
# ======================================================================================

filas = []


for i in range(
    len(
        dm
    )
):

    info_base = {

        columna:
            dm.loc[
                i,
                columna
            ]

        for columna
        in columnas_identificacion

    }


    for variable in variables_modelo:

        valor_original = dm.loc[
            i,
            variable
        ]


        valor_shap = shap_original[
            variable
        ][
            i
        ]


        if valor_shap > 0:

            direccion = (
                "Aumenta riesgo"
            )


        elif valor_shap < 0:

            direccion = (
                "Reduce riesgo"
            )


        else:

            direccion = (
                "Neutro"
            )


        filas.append(
            {

                **info_base,

                "prob_paralizacion":
                    dm.loc[
                        i,
                        "prob_paralizacion"
                    ],

                "prediccion_clase":
                    dm.loc[
                        i,
                        "prediccion_clase"
                    ],

                "prediccion_etiqueta":
                    dm.loc[
                        i,
                        "prediccion_etiqueta"
                    ],

                "tipo":
                    identificar_tipo(
                        variable
                    ),

                "bloque":
                    identificar_bloque(
                        variable
                    ),

                "variable":
                    variable,

                "valor_original":
                    valor_original,

                "shap":
                    float(
                        valor_shap
                    ),

                "shap_abs":
                    float(
                        abs(
                            valor_shap
                        )
                    ),

                "direccion":
                    direccion

            }
        )


tabla_shap_larga = pd.DataFrame(
    filas
)


print(
    "\nFilas tabla SHAP larga:",
    len(
        tabla_shap_larga
    )
)


# ======================================================================================
# 31. RANKING LOCAL
#
# Ranking dentro de cada observación.
#
# Usamos _id_fila_shap para evitar problemas si algún CUI aparece repetido.
# ======================================================================================

tabla_shap_larga[
    "ranking_local"
] = (

    tabla_shap_larga

    .groupby(
        "_id_fila_shap"
    )[
        "shap_abs"
    ]

    .rank(
        method="first",
        ascending=False
    )

    .astype(int)

)


# ======================================================================================
# 32. RANKING DENTRO DE VARIABLES SUSTANTIVAS
#
# Útil para la app si queremos mostrar factores explicativos
# sin controles contextuales.
# ======================================================================================

tabla_shap_larga[
    "ranking_sustantivo"
] = pd.NA


mask_sustantiva = (

    tabla_shap_larga[
        "tipo"
    ]
    ==
    "Sustantiva"

)


ranking_sustantivo = (

    tabla_shap_larga.loc[
        mask_sustantiva
    ]

    .groupby(
        "_id_fila_shap"
    )[
        "shap_abs"
    ]

    .rank(
        method="first",
        ascending=False
    )

    .astype(int)

)


tabla_shap_larga.loc[
    mask_sustantiva,
    "ranking_sustantivo"
] = ranking_sustantivo


tabla_shap_larga[
    "ranking_sustantivo"
] = (

    tabla_shap_larga[
        "ranking_sustantivo"
    ]

    .astype(
        "Int64"
    )

)


# ======================================================================================
# 33. RESUMEN POR BLOQUE
#
# shap_bloque:
#     efecto neto del bloque
#
# shap_abs_bloque:
#     magnitud total de las contribuciones individuales del bloque
# ======================================================================================

tabla_bloques = (

    tabla_shap_larga

    .groupby(
        [
            "_id_fila_shap",
            GROUP,
            "bloque"
        ],
        as_index=False
    )

    .agg(

        shap_bloque=(
            "shap",
            "sum"
        ),

        shap_abs_bloque=(
            "shap_abs",
            "sum"
        )

    )

)


# ======================================================================================
# 34. DIRECCIÓN DEL BLOQUE
# ======================================================================================

tabla_bloques[
    "direccion_bloque"
] = np.where(

    tabla_bloques[
        "shap_bloque"
    ]
    >
    0,

    "Aumenta riesgo",

    np.where(

        tabla_bloques[
            "shap_bloque"
        ]
        <
        0,

        "Reduce riesgo",

        "Neutro"

    )

)


# ======================================================================================
# 35. IMPORTANCIA RELATIVA LOCAL DEL BLOQUE
#
# Proporción de |SHAP| explicada por cada bloque
# dentro de la misma obra.
# ======================================================================================

total_abs_por_obra = (

    tabla_bloques

    .groupby(
        "_id_fila_shap"
    )[
        "shap_abs_bloque"
    ]

    .transform(
        "sum"
    )

)


tabla_bloques[
    "importancia_relativa_bloque_pct"
] = np.where(

    total_abs_por_obra
    >
    0,

    tabla_bloques[
        "shap_abs_bloque"
    ]

    /

    total_abs_por_obra

    *

    100,

    0

)


# ======================================================================================
# 36. RANKING DE BLOQUES
# ======================================================================================

tabla_bloques[
    "ranking_bloque"
] = (

    tabla_bloques

    .groupby(
        "_id_fila_shap"
    )[
        "shap_abs_bloque"
    ]

    .rank(
        method="first",
        ascending=False
    )

    .astype(int)

)


# ======================================================================================
# 37. TABLA RESUMEN POR OBRA
# ======================================================================================

columnas_resumen = [

    "_id_fila_shap",

    GROUP,

    "prob_paralizacion",

    "prediccion_clase",

    "prediccion_etiqueta"

]


for columna in [

    TARGET,

    "estado_real_etiqueta",

    "id_codigo_infobras",

    "id_cui",

    "id_nomenclatura",

    "op_nombre_obra",

    "op_nombre_obra_op",

    "sea_entidad",

    "op_entidad_op",

    "ENTIDAD",

    "NOMBRE_UEI",

    "op_nivel_gobierno",

    "op_sector",

    "op_departamento",

    "op_provincia",

    "op_distrito",

    "sea_anio_convocatoria",

    "op_estado_ejecucion_infobras",

    "op_opb_estado_final",

    "op_ESTADO"

]:

    if (

        columna
        in
        dm.columns

        and

        columna
        not in
        columnas_resumen

    ):

        columnas_resumen.append(
            columna
        )


tabla_cui = (

    dm[
        columnas_resumen
    ]

    .copy()

)


# ======================================================================================
# 38. BLOQUES EN FORMATO ANCHO
# ======================================================================================

bloques_ancho = (

    tabla_bloques

    .pivot(

        index=
            "_id_fila_shap",

        columns=
            "bloque",

        values=
            "shap_bloque"

    )

    .reset_index()

)


bloques_ancho.columns = [

    (

        columna

        if columna
        ==
        "_id_fila_shap"

        else
        f"shap_bloque_{str(columna).lower()}"

    )

    for columna
    in bloques_ancho.columns

]


tabla_cui = (

    tabla_cui

    .merge(

        bloques_ancho,

        on=
            "_id_fila_shap",

        how=
            "left"

    )

)


# ======================================================================================
# 39. BLOQUE DOMINANTE
#
# Identifica el bloque con mayor magnitud SHAP en cada obra.
# ======================================================================================

bloque_principal = (

    tabla_bloques

    .sort_values(
        [
            "_id_fila_shap",
            "shap_abs_bloque"
        ],
        ascending=[
            True,
            False
        ]
    )

    .drop_duplicates(
        subset=[
            "_id_fila_shap"
        ]
    )

    [
        [
            "_id_fila_shap",
            "bloque",
            "shap_bloque",
            "shap_abs_bloque",
            "direccion_bloque",
            "importancia_relativa_bloque_pct"
        ]
    ]

    .rename(
        columns=
            {

                "bloque":
                    "bloque_principal",

                "shap_bloque":
                    "shap_bloque_principal",

                "shap_abs_bloque":
                    "shap_abs_bloque_principal",

                "direccion_bloque":
                    "direccion_bloque_principal",

                "importancia_relativa_bloque_pct":
                    "importancia_bloque_principal_pct"

            }
    )

)


tabla_cui = (

    tabla_cui

    .merge(

        bloque_principal,

        on=
            "_id_fila_shap",

        how=
            "left"

    )

)


# ======================================================================================
# 40. FACTOR PRINCIPAL SUSTANTIVO
#
# Esto será muy útil para la ficha de la app.
# ======================================================================================

factor_principal = (

    tabla_shap_larga[
        tabla_shap_larga[
            "tipo"
        ]
        ==
        "Sustantiva"
    ]

    .sort_values(
        [
            "_id_fila_shap",
            "shap_abs"
        ],
        ascending=[
            True,
            False
        ]
    )

    .drop_duplicates(
        subset=[
            "_id_fila_shap"
        ]
    )

    [
        [
            "_id_fila_shap",
            "variable",
            "valor_original",
            "shap",
            "shap_abs",
            "direccion",
            "bloque"
        ]
    ]

    .rename(
        columns=
            {

                "variable":
                    "factor_principal",

                "valor_original":
                    "valor_factor_principal",

                "shap":
                    "shap_factor_principal",

                "shap_abs":
                    "shap_abs_factor_principal",

                "direccion":
                    "direccion_factor_principal",

                "bloque":
                    "bloque_factor_principal"

            }
    )

)


tabla_cui = (

    tabla_cui

    .merge(

        factor_principal,

        on=
            "_id_fila_shap",

        how=
            "left"

    )

)


# ======================================================================================
# 41. ASEGURAR TIPOS PARQUET
#
# valor_original mezcla strings, enteros y floats.
# ======================================================================================

tabla_shap_larga[
    "valor_original"
] = (

    tabla_shap_larga[
        "valor_original"
    ]

    .apply(
        lambda x:
            None
            if pd.isna(x)
            else str(x)
    )

)


if (
    "valor_factor_principal"
    in
    tabla_cui.columns
):

    tabla_cui[
        "valor_factor_principal"
    ] = (

        tabla_cui[
            "valor_factor_principal"
        ]

        .apply(
            lambda x:
                None
                if pd.isna(x)
                else str(x)
        )

    )


# ======================================================================================
# 42. CONTROLES FINALES
# ======================================================================================

print(
    "\n"
    + "=" * 100
)

print(
    "CONTROLES FINALES"
)

print(
    "=" * 100
)


print(
    "Obras explicadas:",
    len(
        dm
    )
)


print(
    "Variables por obra:",
    len(
        variables_modelo
    )
)


print(
    "Filas SHAP esperadas:",
    len(
        dm
    )
    *
    len(
        variables_modelo
    )
)


print(
    "Filas SHAP generadas:",
    len(
        tabla_shap_larga
    )
)


assert (

    len(
        tabla_shap_larga
    )

    ==

    len(
        dm
    )
    *
    len(
        variables_modelo
    )

)


assert (
    "op_n_reportes"
    not in
    tabla_shap_larga[
        "variable"
    ].unique()
)


print(
    "OK: 60 explicaciones por observación."
)


print(
    "OK: op_n_reportes no está presente."
)


# ======================================================================================
# 43. GUARDAR EXPLICACIONES POR VARIABLE
# ======================================================================================

ruta_larga = (

    RUTA_SALIDA
    / "explicaciones_shap.parquet"

)


tabla_shap_larga.to_parquet(

    ruta_larga,

    index=False

)


# ======================================================================================
# 44. GUARDAR SHAP POR BLOQUE
# ======================================================================================

ruta_bloques = (

    RUTA_SALIDA
    / "shap_por_bloque.parquet"

)


tabla_bloques.to_parquet(

    ruta_bloques,

    index=False

)


# ======================================================================================
# 45. GUARDAR RESUMEN POR OBRA
# ======================================================================================

ruta_resumen = (

    RUTA_SALIDA
    / "predicciones_cui.parquet"

)


tabla_cui.to_parquet(

    ruta_resumen,

    index=False

)


# ======================================================================================
# 46. MOSTRAR ARCHIVOS
# ======================================================================================

print(
    "\n"
    + "=" * 100
)

print(
    "ARCHIVOS GENERADOS"
)

print(
    "=" * 100
)


print(
    "\nExplicaciones por variable:"
)

print(
    ruta_larga
)


print(
    "\nSHAP por bloque:"
)

print(
    ruta_bloques
)


print(
    "\nResumen por obra:"
)

print(
    ruta_resumen
)


# ======================================================================================
# 47. EJEMPLO
# ======================================================================================

ejemplo_id = (

    tabla_cui[
        "_id_fila_shap"
    ]

    .iloc[
        0
    ]

)


ejemplo_cui = (

    tabla_cui.loc[
        tabla_cui[
            "_id_fila_shap"
        ]
        ==
        ejemplo_id,
        GROUP
    ]

    .iloc[
        0
    ]

)


print(
    "\n"
    + "=" * 100
)

print(
    "EJEMPLO DE EXPLICACIÓN LOCAL"
)

print(
    "=" * 100
)


print(
    "\nCUI:",
    ejemplo_cui
)


ejemplo = (

    tabla_shap_larga[
        tabla_shap_larga[
            "_id_fila_shap"
        ]
        ==
        ejemplo_id
    ]

    .sort_values(
        "shap_abs",
        ascending=False
    )

    [
        [
            "variable",
            "bloque",
            "tipo",
            "valor_original",
            "shap",
            "direccion",
            "ranking_local"
        ]
    ]

    .head(
        10
    )

)


print(
    ejemplo.to_string(
        index=False
    )
)


print(
    "\nProceso terminado correctamente."
)