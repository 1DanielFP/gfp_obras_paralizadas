# ======================================================================================
# PREPARAR MODELO FINAL PARA LA APP
#
# Modelo:
# XGBoost - Especificación S3 final del minilab
#
# S1 = características de inversión
# S2 = + factores asociados depurados
# S3 = + variables sustantivas de avance
#
# IMPORTANTE:
#
# - Usa df_final_minilab.xlsx
# - 5 variables categóricas
# - 55 variables numéricas
# - 60 variables originales en total
# - NO usa variables de disponibilidad
# - NO usa *_match
# - NO usa _merge*
# - NO usa op_n_reportes
# - NO usa estados de la obra como predictores
# - SÍ conserva variables de estado en la base para mostrarlas en la app
#
# Clase objetivo:
# 0 = No paralizada
# 1 = Paralizada
# ======================================================================================


# ======================================================================================
# 0. LIBRERÍAS
# ======================================================================================

from pathlib import Path

import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import GroupShuffleSplit

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder

from sklearn.impute import SimpleImputer

from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)

from xgboost import XGBClassifier


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

)


RUTA_MODELO.mkdir(

    parents=True,

    exist_ok=True

)


# ======================================================================================
# 2. CARGAR BASE FINAL
# ======================================================================================

df = pd.read_excel(
    RUTA_DATOS
)


print(
    "=" * 100
)

print(
    "BASE FINAL CARGADA"
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
# 3. VARIABLES GENERALES
# ======================================================================================

TARGET = "op_estado_dummy"

GROUP = "id_cui_std"


# ======================================================================================
# 4. VARIABLES INFORMATIVAS PARA LA APP
#
# Estas pueden mostrarse al usuario.
#
# NO ENTRAN AL MODELO.
# ======================================================================================

VARIABLES_ESTADO_APP = [

    "op_estado_ejecucion_infobras",

    "op_opb_estado_final",

    "op_ESTADO"

]


VARIABLES_IDENTIFICACION_APP = [

    "id_codigo_infobras",

    "id_cui",

    "id_cui_std",

    "op_nombre_obra",

    "op_nombre_obra_op",

    "sea_entidad",

    "op_entidad_op",

    "ENTIDAD",

    "NOMBRE_UEI",

    "op_sector",

    "op_provincia",

    "op_distrito"

]


# ======================================================================================
# 5. NORMALIZAR CUI
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
# 6. NORMALIZAR NIVEL DE GOBIERNO
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
# 7. NORMALIZAR SALDO DE OBRA
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
# 8. VARIABLES CATEGÓRICAS DEL MODELO FINAL
#
# EXACTAMENTE las mismas 5 del minilab final.
# ======================================================================================

variables_categoricas = [

    "op_nivel_gobierno",

    "op_departamento",

    "op_es_saldo_obra",

    "modalidad_general",

    "mecanismo_ejecucion"

]


# ======================================================================================
# 9. MEF
# ======================================================================================

variables_mef = [

    "ratio_costo_viable",

    "costo_actualizado_mayor_30",

    "ratio_costo_et",

    "ratio_devengado_costo",

    "share_saldo_ejecutar"

]


# ======================================================================================
# 10. UNIDAD EJECUTORA
# ======================================================================================

variables_ue = [

    "ejecucion_pim_ue",

    "pct_pi_sin_devengado_ue",

    "pct_pi_baja_ejecucion_ue",

    "ratio_pim_pia_ue",

    "incremento_pim_pia_ue",

    "share_saldo_cartera_ue",

    "pct_pi_caida_ejecucion_ue",

    "pct_pi_sin_devengado_actual_con_historial_ue",

    "n_pi_ue",

    "pim_total_ue",

    "devengado_total_ue",

    "costo_total_cartera_ue"

]


# ======================================================================================
# 11. DESBALANCE PATRIMONIAL
# ======================================================================================

variables_desbalance = [

    "cui_tiene_desbalance",

    "max_desbalance_cui",

    "share_funcionarios_con_desbalance_cui",

    "desbalance_acumulado_funcionarios_cui"

]


# ======================================================================================
# 12. SUNAT
# ======================================================================================

variables_sunat = [

    "sun_log_trabajadores_prom_12m_cui",

    "sun_min_log_trabajadores_prom_12m_cui",

    "sun_antiguedad_al_proceso_cui",

    "sun_min_antiguedad_al_proceso_cui",

    "sun_share_empresas_activas_cui",

    "sun_share_empresas_habidas_cui",

    "sun_share_empresas_deuda_coactiva_cui",

    "sun_share_empresas_omisiones_cui",

    "sun_alguna_empresa_deuda_coactiva_cui",

    "sun_alguna_empresa_omisiones_cui"

]


# ======================================================================================
# 13. RENAMU
# ======================================================================================

variables_renamu = [

    "renamu_personal_total",

    "renamu_share_profesional",

    "renamu_share_tecnico",

    "renamu_share_calificado",

    "renamu_n_instrumentos_gestion",

    "renamu_n_sistemas_estado",

    "renamu_n_sistemas_gestion",

    "renamu_tiene_internet",

    "renamu_tiene_maquinaria_operativa",

    "renamu_pct_maquinaria_operativa"

]


# ======================================================================================
# 14. IGEIP DEPURADO
#
# Solo sobreviven 03, 04 y 07.
# ======================================================================================

variables_igeip = [

    "ejec_03",

    "ejec_04",

    "ejec_07"

]


# ======================================================================================
# 15. PROCESO DE SELECCIÓN
# ======================================================================================

variables_seleccion = [

    "sea_comite_seleccion_cantidad_integrantes",

    "con_numero_postores",

    "con_numero_proveedores",

    "con_numero_consorcios",

    "postor_unico",

    "baja_competencia_proceso"

]


# ======================================================================================
# 16. CONTRACTUAL
#
# Solo plazo contractual sobrevivió a la depuración.
# ======================================================================================

variables_contractuales = [

    "op_plazo_dias"

]


# ======================================================================================
# 17. AVANCE FÍSICO / FINANCIERO
#
# SOLO VARIABLES SUSTANTIVAS.
#
# op_n_reportes queda expresamente fuera.
# ======================================================================================

variables_avance = [

    "op_periodos_sin_avance_fisico",

    "op_periodos_sin_avance_financiero",

    "op_ultimo_avance_fisico",

    "op_ultimo_avance_financiero"

]


# ======================================================================================
# 18. VARIABLES NUMÉRICAS S3 FINAL
# ======================================================================================

variables_numericas = (

    variables_mef

    +

    variables_ue

    +

    variables_desbalance

    +

    variables_sunat

    +

    variables_renamu

    +

    variables_igeip

    +

    variables_seleccion

    +

    variables_contractuales

    +

    variables_avance

)


variables_numericas = list(

    dict.fromkeys(
        variables_numericas
    )

)


# ======================================================================================
# 19. VARIABLES FINALES DEL MODELO
# ======================================================================================

variables_modelo = (

    variables_categoricas

    +

    variables_numericas

)


# ======================================================================================
# 20. CONTROL DE CONTEO
#
# Esperamos:
#
# 5 categóricas
# 55 numéricas
# 60 total
# ======================================================================================

print(
    "\n"
    + "=" * 100
)

print(
    "ESPECIFICACIÓN FINAL"
)

print(
    "=" * 100
)


print(
    "Categóricas:",
    len(
        variables_categoricas
    )
)


print(
    "Numéricas:",
    len(
        variables_numericas
    )
)


print(
    "Total:",
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


# ======================================================================================
# 21. VARIABLES PROHIBIDAS
# ======================================================================================

variables_prohibidas_explicitas = [

    # Target
    TARGET,


    # Disponibilidad / intensidad de información
    "op_n_reportes",

    "desbalance_disponible",

    "conflicto_intereses_disponible",

    "sunat_disponible",

    "n_indicadores_ejec_disponibles",


    # Estados
    "op_estado_ejecucion_infobras",

    "op_opb_estado_final",

    "op_ESTADO",


    # No homologadas
    "op_naturaleza_obra",

    "op_marca_rcc",

    "op_marca_reactivacion",

    "op_otra_marca",


    # Contractuales problemáticas
    "op_n_controversias",

    "tiene_controversias",

    "op_n_modificaciones",

    "op_dias_ampliacion",

    "ratio_ampliacion_plazo",


    # Conflicto
    "cui_tiene_exposicion_conflicto",

    "share_funcionarios_con_exposicion_conflicto_cui",

    "n_tipos_exposicion_conflicto_cui",

    "max_tipos_exposicion_funcionario_cui",


    # Funcionarios
    "n_funcionarios_detalle_cui",

    "cui_tiene_funcionario_multicargo",

    "n_funcionarios_multicargo_cui",

    "share_funcionarios_multicargo_cui",

    "max_cargos_por_funcionario_cui",

    "promedio_cargos_por_funcionario_cui",

    "cui_tiene_funcionario_recurrente",

    "n_funcionarios_recurrentes_cui",

    "share_funcionarios_recurrentes_cui",

    "max_obras_por_funcionario_cui",

    "promedio_obras_por_funcionario_cui",


    # IGEIP excluido
    "ejec_01",

    "ejec_02",

    "ejec_05",

    "ejec_06",

    "ejec_08",


    # Selección excluida
    "dias_buenapro_consentimiento",

    "seleccion_cierre_3d",

    "seleccion_cierre_5d",

    "seleccion_cierre_7d",

    "seleccion_cierre_10d",

    "seleccion_cierre_15d",


    # RENAMU excluida
    "renamu_share_computadoras_internet"

]


patrones_prohibidos = [

    "_disponible",

    "_match",

    "_merge",

    "fuzzy_",

    "score_distrito",

    "tipo_validacion",

    "fuente_ubigeo",

    "ubigeo_recuperado",

    "ubigeo_original_validado",

    "ubigeo_original_existe",

    "ubigeo_renamu_corregido",

    "n_indicadores_ejec_disponibles",

    "n_reportes"

]


# ======================================================================================
# 22. VALIDAR QUE NO HAYA LEAKAGE / DISPONIBILIDAD
# ======================================================================================

sospechosas = []


for variable in variables_modelo:

    variable_lower = (
        str(variable)
        .lower()
    )


    if (
        variable
        in
        variables_prohibidas_explicitas
    ):

        sospechosas.append(
            variable
        )

        continue


    if any(

        patron
        in
        variable_lower

        for patron
        in
        patrones_prohibidos

    ):

        sospechosas.append(
            variable
        )


print(
    "\nVariables prohibidas encontradas:",
    sospechosas
)


assert (
    len(
        sospechosas
    )
    ==
    0
), (
    "Hay variables prohibidas en el modelo: "
    f"{sospechosas}"
)


print(
    "OK: ninguna variable de disponibilidad/leakage entra al modelo."
)


# ======================================================================================
# 23. CONTROL DE op_n_reportes
# ======================================================================================

assert (
    "op_n_reportes"
    not in
    variables_modelo
)


print(
    "OK: op_n_reportes excluida."
)


# ======================================================================================
# 24. CONTROL DE AVANCE
# ======================================================================================

for variable in variables_avance:

    assert (
        variable
        in
        variables_modelo
    )


print(
    "OK: las 4 variables sustantivas de avance están presentes."
)


# ======================================================================================
# 25. VALIDAR VARIABLES EN LA BASE
# ======================================================================================

faltantes = [

    variable

    for variable
    in (
        variables_modelo
        +
        [
            TARGET,
            GROUP
        ]
    )

    if variable
    not in
    df.columns

]


if faltantes:

    raise ValueError(
        f"Faltan variables en df_final_minilab.xlsx: {faltantes}"
    )


# ======================================================================================
# 26. HOMOLOGAR TODAS LAS CATEGÓRICAS
#
# Igual que en el minilab:
#
# - conserva NaN
# - convierte valores observados a string
# - elimina espacios laterales
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
# 27. ASEGURAR NUMÉRICAS
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
# 28. MUESTRA MODELABLE
# ======================================================================================

mask = (

    df[
        TARGET
    ]
    .notna()

    &

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

)


dm[
    TARGET
] = (

    pd.to_numeric(

        dm[
            TARGET
        ],

        errors="coerce"

    )

    .astype(int)

)


print(
    "\n"
    + "=" * 100
)

print(
    "MUESTRA MODELABLE"
)

print(
    "=" * 100
)


print(
    "N:",
    len(
        dm
    )
)


print(
    "\nTarget:"
)


print(
    dm[
        TARGET
    ]
    .value_counts()
    .sort_index()
)


# ======================================================================================
# 29. SPLIT AGRUPADO
#
# MISMO SPLIT DEL MINILAB
#
# random_state = 42
# test_size = 20%
# grupos = CUI
# ======================================================================================

gss = GroupShuffleSplit(

    n_splits=1,

    test_size=0.20,

    random_state=42

)


train_idx, test_idx = next(

    gss.split(

        dm,

        y=
            dm[
                TARGET
            ],

        groups=
            dm[
                GROUP
            ]

    )

)


train = (

    dm.iloc[
        train_idx
    ]

    .copy()

)


test = (

    dm.iloc[
        test_idx
    ]

    .copy()

)


# ======================================================================================
# 30. VERIFICAR QUE NO HAYA CUI EN TRAIN Y TEST
# ======================================================================================

overlap = (

    set(
        train[
            GROUP
        ]
    )

    &

    set(
        test[
            GROUP
        ]
    )

)


assert (
    len(
        overlap
    )
    ==
    0
)


print(
    "\nTrain:",
    len(
        train
    )
)


print(
    "Test:",
    len(
        test
    )
)


print(
    "CUI overlap:",
    len(
        overlap
    )
)


print(
    "\nTarget train:"
)


print(
    train[
        TARGET
    ]
    .value_counts()
    .sort_index()
)


print(
    "\nTarget test:"
)


print(
    test[
        TARGET
    ]
    .value_counts()
    .sort_index()
)


# ======================================================================================
# 31. X / Y
# ======================================================================================

X_train = (

    train[
        variables_modelo
    ]

    .copy()

)


X_test = (

    test[
        variables_modelo
    ]

    .copy()

)


y_train = (

    train[
        TARGET
    ]

    .astype(int)

)


y_test = (

    test[
        TARGET
    ]

    .astype(int)

)


# ======================================================================================
# 32. PREPROCESAMIENTO CATEGÓRICO
# ======================================================================================

pipe_cat = Pipeline(
    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy=
                    "most_frequent"
            )

        ),

        (
            "onehot",

            OneHotEncoder(
                handle_unknown=
                    "ignore"
            )

        )

    ]
)


# ======================================================================================
# 33. PREPROCESAMIENTO NUMÉRICO
# ======================================================================================

pipe_num = Pipeline(
    steps=[

        (
            "imputer",

            SimpleImputer(
                strategy=
                    "median"
            )

        )

    ]
)


# ======================================================================================
# 34. COLUMN TRANSFORMER
#
# El nombre "prep" se usa también en el script SHAP.
# ======================================================================================

preprocesador = ColumnTransformer(
    transformers=[

        (
            "cat",

            pipe_cat,

            variables_categoricas

        ),

        (
            "num",

            pipe_num,

            variables_numericas

        )

    ],

    remainder=
        "drop"
)


# ======================================================================================
# 35. SCALE POS WEIGHT
# ======================================================================================

negativos = (

    y_train
    ==
    0

).sum()


positivos = (

    y_train
    ==
    1

).sum()


scale_pos_weight = (

    negativos

    /

    positivos

    if positivos > 0

    else 1

)


print(
    "\nscale_pos_weight:",
    round(
        scale_pos_weight,
        4
    )
)


# ======================================================================================
# 36. XGBOOST
#
# EXACTAMENTE LA CONFIGURACIÓN DEL MINILAB FINAL
# ======================================================================================

modelo = XGBClassifier(

    n_estimators=
        600,

    learning_rate=
        0.03,

    max_depth=
        4,

    min_child_weight=
        3,

    subsample=
        0.85,

    colsample_bytree=
        0.85,

    reg_alpha=
        0.10,

    reg_lambda=
        1.0,

    scale_pos_weight=
        scale_pos_weight,

    objective=
        "binary:logistic",

    eval_metric=
        "logloss",

    random_state=
        42,

    n_jobs=
        -1

)


# ======================================================================================
# 37. PIPELINE FINAL
#
# IMPORTANTE:
# usamos "prep" para mantener compatibilidad con el script SHAP.
# ======================================================================================

pipeline_final = Pipeline(
    steps=[

        (
            "prep",

            preprocesador

        ),

        (
            "modelo",

            modelo

        )

    ]
)


# ======================================================================================
# 38. ENTRENAR
# ======================================================================================

print(
    "\nEntrenando XGBoost S3 final..."
)


pipeline_final.fit(

    X_train,

    y_train

)


# ======================================================================================
# 39. EVALUAR
#
# Esto permite comprobar que la app está entrenando
# la misma especificación que el minilab.
# ======================================================================================

pred = pipeline_final.predict(
    X_test
)


prob = pipeline_final.predict_proba(
    X_test
)[
    :,
    1
]


metricas = {

    "accuracy":
        accuracy_score(
            y_test,
            pred
        ),

    "balanced_accuracy":
        balanced_accuracy_score(
            y_test,
            pred
        ),

    "precision":
        precision_score(
            y_test,
            pred,
            zero_division=0
        ),

    "recall":
        recall_score(
            y_test,
            pred,
            zero_division=0
        ),

    "f1":
        f1_score(
            y_test,
            pred,
            zero_division=0
        ),

    "roc_auc":
        roc_auc_score(
            y_test,
            prob
        ),

    "average_precision":
        average_precision_score(
            y_test,
            prob
        )

}


print(
    "\n"
    + "=" * 100
)

print(
    "DESEMPEÑO DEL MODELO PARA LA APP"
)

print(
    "=" * 100
)


for metrica, valor in metricas.items():

    print(
        f"{metrica}: {valor:.4f}"
    )


# ======================================================================================
# 40. MATRIZ DE CONFUSIÓN
# ======================================================================================

cm = confusion_matrix(

    y_test,

    pred,

    labels=[
        0,
        1
    ]

)


print(
    "\nMatriz de confusión:"
)


print(
    cm
)


# ======================================================================================
# 41. GUARDAR PIPELINE
# ======================================================================================

ruta_pipeline = (

    RUTA_MODELO
    / "modelo_xgb_pipeline.pkl"

)


joblib.dump(

    pipeline_final,

    ruta_pipeline

)


# ======================================================================================
# 42. CONFIGURACIÓN DEL MODELO
#
# Incluimos además metadata que luego será útil para la app y SHAP.
# ======================================================================================

configuracion = {

    "version_modelo":
        "minilab_s3_final_sin_disponibilidad",

    "archivo_datos":
        "df_final_minilab.xlsx",

    "target":
        TARGET,

    "clase_positiva":
        1,

    "clase_positiva_nombre":
        "Paralizada",

    "clase_negativa":
        0,

    "clase_negativa_nombre":
        "No paralizada",

    "group":
        GROUP,

    "random_state":
        42,

    "test_size":
        0.20,

    "variables_categoricas":
        variables_categoricas,

    "variables_numericas":
        variables_numericas,

    "variables_modelo":
        variables_modelo,

    "variables_mef":
        variables_mef,

    "variables_ue":
        variables_ue,

    "variables_desbalance":
        variables_desbalance,

    "variables_sunat":
        variables_sunat,

    "variables_renamu":
        variables_renamu,

    "variables_igeip":
        variables_igeip,

    "variables_seleccion":
        variables_seleccion,

    "variables_contractuales":
        variables_contractuales,

    "variables_avance":
        variables_avance,

    "variables_estado_app":
        VARIABLES_ESTADO_APP,

    "variables_identificacion_app":
        VARIABLES_IDENTIFICACION_APP,

    "n_variables_categoricas":
        len(
            variables_categoricas
        ),

    "n_variables_numericas":
        len(
            variables_numericas
        ),

    "n_variables_modelo":
        len(
            variables_modelo
        ),

    "metricas_test":
        {
            k:
                float(v)

            for k, v
            in metricas.items()
        },

    "matriz_confusion_test":
        cm.tolist()

}


# ======================================================================================
# 43. GUARDAR CONFIGURACIÓN JSON
# ======================================================================================

ruta_config = (

    RUTA_MODELO
    / "configuracion_modelo.json"

)


with open(

    ruta_config,

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        configuracion,

        f,

        ensure_ascii=False,

        indent=4

    )


# ======================================================================================
# 44. GUARDAR TEST
#
# Conservamos:
#
# - identificador
# - target
# - las 60 variables del modelo
#
# Esto luego sirve para SHAP y validaciones.
# ======================================================================================

ruta_test = (

    RUTA_MODELO
    / "test_modelo.parquet"

)


columnas_test = (

    [
        GROUP,
        TARGET
    ]

    +

    variables_modelo

)


columnas_test = list(

    dict.fromkeys(
        columnas_test
    )

)


test[
    columnas_test
].to_parquet(

    ruta_test,

    index=False

)


# ======================================================================================
# 45. GUARDAR ÍNDICES DE TRAIN Y TEST
#
# Útil para reproducibilidad.
# ======================================================================================

ruta_split = (

    RUTA_MODELO
    / "split_modelo.npz"

)


np.savez(

    ruta_split,

    train_idx=
        train_idx,

    test_idx=
        test_idx

)


# ======================================================================================
# 46. RESUMEN FINAL
# ======================================================================================

print(
    "\n"
    + "=" * 100
)

print(
    "MODELO FINAL PARA LA APP GUARDADO CORRECTAMENTE"
)

print(
    "=" * 100
)


print(
    "\nBase:"
)

print(
    RUTA_DATOS
)


print(
    "\nPipeline:"
)

print(
    ruta_pipeline
)


print(
    "\nConfiguración:"
)

print(
    ruta_config
)


print(
    "\nTest:"
)

print(
    ruta_test
)


print(
    "\nSplit:"
)

print(
    ruta_split
)


print(
    "\nVariables categóricas:",
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


print(
    "\nVariables de avance:"
)


for variable in variables_avance:

    print(
        "-",
        variable
    )


print(
    "\nVariables de estado disponibles para la app:"
)


for variable in VARIABLES_ESTADO_APP:

    if variable in df.columns:

        print(
            "-",
            variable
        )