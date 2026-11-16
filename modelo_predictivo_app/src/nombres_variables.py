# ======================================================================================
# NOMBRES DE VARIABLES PARA LA INTERFAZ
# ======================================================================================
#
# Clave = nombre original de la variable en df_final_minilab.xlsx
# Valor = nombre técnico/legible mostrado en la aplicación
#
# IMPORTANTE:
#
# Este archivo SOLO define nombres para la interfaz.
# NO determina qué variables entran al modelo.
#
# Por eso también pueden aparecer aquí variables exclusivamente informativas,
# como el estado de ejecución de la obra.
# ======================================================================================


NOMBRES_VARIABLES = {


    # ==================================================================================
    # IDENTIFICACIÓN DE LA OBRA
    # ==================================================================================

    "id_codigo_infobras":
        "Código INFOBRAS",

    "id_cui":
        "Código Único de Inversión (CUI)",

    "id_cui_std":
        "Código Único de Inversión (CUI)",

    "cod_snip":
        "Código SNIP",

    "id_nomenclatura":
        "Nomenclatura del proceso",

    "op_nombre_obra":
        "Nombre de la obra",

    "op_nombre_obra_op":
        "Nombre de la obra",

    "sea_entidad":
        "Entidad convocante",

    "op_entidad_op":
        "Entidad ejecutora",

    "ENTIDAD":
        "Entidad",

    "NOMBRE_UEI":
        "Unidad Ejecutora de Inversiones",

    "sec_ejec":
        "Código de Unidad Ejecutora",


    # ==================================================================================
    # ESTADO DE LA OBRA
    #
    # SOLO PARA LA INTERFAZ.
    # NO SON PREDICTORES DEL MODELO.
    # ==================================================================================

    "op_estado_ejecucion_infobras":
        "Estado de ejecución de la obra",

    "op_opb_estado_final":
        "Estado final de la obra",

    "op_ESTADO":
        "Estado registrado de la obra",

    "op_estado_dummy":
        "Condición de paralización",


    # ==================================================================================
    # CONTEXTO DE LA OBRA
    # ==================================================================================

    "sea_anio_convocatoria":
        "Año de convocatoria",

    "op_nivel_gobierno":
        "Nivel de gobierno",

    "op_sector":
        "Sector funcional",

    "op_departamento":
        "Departamento",

    "op_provincia":
        "Provincia",

    "op_distrito":
        "Distrito",

    "op_es_saldo_obra":
        "Condición de saldo de obra",

    "modalidad_general":
        "Modalidad de ejecución",

    "mecanismo_ejecucion":
        "Mecanismo de ejecución",


    # ==================================================================================
    # MEF / CARACTERÍSTICAS DE LA INVERSIÓN
    # ==================================================================================

    "ratio_costo_viable":
        "Variación del costo actualizado respecto al costo viable",

    "costo_actualizado_mayor_30":
        "Incremento del costo actualizado superior al 30%",

    "ratio_costo_et":
        "Relación entre costo actualizado y expediente técnico",

    "devengado_acumulado_total":
        "Devengado acumulado",

    "ratio_devengado_costo":
        "Ejecución financiera acumulada respecto al costo de inversión",

    "share_saldo_ejecutar":
        "Proporción del costo pendiente de ejecución",

    "avance_financiero_mef":
        "Avance financiero registrado por el MEF",


    # ==================================================================================
    # UNIDAD EJECUTORA
    # ==================================================================================

    "n_pi_ue":
        "Número de inversiones de la Unidad Ejecutora",

    "pim_total_ue":
        "PIM total de la Unidad Ejecutora",

    "devengado_total_ue":
        "Devengado total de la Unidad Ejecutora",

    "costo_total_cartera_ue":
        "Costo total de la cartera de inversiones",

    "ejecucion_pim_ue":
        "Ejecución presupuestal de la Unidad Ejecutora",

    "pct_pi_sin_devengado_ue":
        "Proporción de inversiones sin devengado en la Unidad Ejecutora",

    "pct_pi_baja_ejecucion_ue":
        "Proporción de inversiones con baja ejecución presupuestal",

    "ratio_pim_pia_ue":
        "Relación PIM/PIA de la Unidad Ejecutora",

    "incremento_pim_pia_ue":
        "Incremento presupuestal PIM respecto al PIA",

    "share_saldo_cartera_ue":
        "Proporción de saldo pendiente en la cartera de inversiones",

    "pct_pi_caida_ejecucion_ue":
        "Proporción de inversiones con caída interanual de ejecución",

    "pct_pi_sin_devengado_actual_con_historial_ue":
        "Inversiones sin devengado actual con historial de ejecución",


    # ==================================================================================
    # DESBALANCE PATRIMONIAL
    # ==================================================================================

    "cui_tiene_desbalance":
        "Presencia de funcionarios con desbalance patrimonial",

    "max_desbalance_cui":
        "Máximo desbalance patrimonial identificado",

    "share_funcionarios_con_desbalance_cui":
        "Proporción de funcionarios con desbalance patrimonial",

    "desbalance_acumulado_funcionarios_cui":
        "Desbalance patrimonial acumulado de funcionarios",


    # ==================================================================================
    # SUNAT / CARACTERÍSTICAS DE LOS CONTRATISTAS
    # ==================================================================================

    "sun_log_trabajadores_prom_12m_cui":
        "Número promedio de trabajadores de los contratistas",

    "sun_min_log_trabajadores_prom_12m_cui":
        "Menor número de trabajadores entre contratistas",

    "sun_antiguedad_al_proceso_cui":
        "Antigüedad empresarial de los contratistas",

    "sun_min_antiguedad_al_proceso_cui":
        "Antigüedad mínima entre contratistas",

    "sun_share_empresas_activas_cui":
        "Proporción de empresas con estado activo",

    "sun_share_empresas_habidas_cui":
        "Proporción de empresas con condición habida",

    "sun_share_empresas_deuda_coactiva_cui":
        "Proporción de empresas con deuda coactiva",

    "sun_share_empresas_omisiones_cui":
        "Proporción de empresas con omisiones tributarias",

    "sun_alguna_empresa_deuda_coactiva_cui":
        "Presencia de contratistas con deuda coactiva",

    "sun_alguna_empresa_omisiones_cui":
        "Presencia de contratistas con omisiones tributarias",


    # ==================================================================================
    # RENAMU / CAPACIDAD MUNICIPAL
    # ==================================================================================

    "renamu_personal_total":
        "Personal municipal total",

    "renamu_share_profesional":
        "Proporción de personal profesional",

    "renamu_share_tecnico":
        "Proporción de personal técnico",

    "renamu_share_calificado":
        "Proporción de personal calificado",

    "renamu_n_instrumentos_gestion":
        "Número de instrumentos de gestión municipal",

    "renamu_n_sistemas_estado":
        "Número de sistemas administrativos del Estado utilizados",

    "renamu_n_sistemas_gestion":
        "Número de sistemas de gestión utilizados",

    "renamu_tiene_internet":
        "Disponibilidad de conexión a internet institucional",

    "renamu_tiene_maquinaria_operativa":
        "Disponibilidad de maquinaria municipal operativa",

    "renamu_pct_maquinaria_operativa":
        "Proporción de maquinaria municipal operativa",


    # ==================================================================================
    # IGEIP
    #
    # Solo quedaron 03, 04 y 07 en el modelo final.
    # ==================================================================================

    "ejec_03":
        "Indicador IGEIP de ejecución 03",

    "ejec_04":
        "Indicador IGEIP de ejecución 04",

    "ejec_07":
        "Indicador IGEIP de ejecución 07",


    # ==================================================================================
    # PROCESO DE SELECCIÓN
    # ==================================================================================

    "sea_comite_seleccion_cantidad_integrantes":
        "Número de integrantes del comité de selección",

    "con_numero_postores":
        "Número de postores",

    "con_numero_proveedores":
        "Número de proveedores",

    "con_numero_consorcios":
        "Número de consorcios",

    "postor_unico":
        "Proceso con postor único",

    "baja_competencia_proceso":
        "Proceso con baja competencia",


    # ==================================================================================
    # CARACTERÍSTICA CONTRACTUAL
    # ==================================================================================

    "op_plazo_dias":
        "Plazo contractual de la obra",


    # ==================================================================================
    # AVANCE FÍSICO Y FINANCIERO
    #
    # Estas cuatro variables sí forman parte de S3.
    # ==================================================================================

    "op_periodos_sin_avance_fisico":
        "Periodos sin avance físico",

    "op_periodos_sin_avance_financiero":
        "Periodos sin avance financiero",

    "op_ultimo_avance_fisico":
        "Último avance físico registrado",

    "op_ultimo_avance_financiero":
        "Último avance financiero registrado",


    # ==================================================================================
    # VARIABLES SOLO INFORMATIVAS
    #
    # Pueden utilizarse en la interfaz, pero NO como predictores.
    # ==================================================================================

    "op_n_reportes":
        "Número de reportes de avance",

    "op_naturaleza_obra":
        "Naturaleza de la obra",

    "op_marca_rcc":
        "Marca RCC",

    "op_marca_reactivacion":
        "Marca de reactivación",

    "op_otra_marca":
        "Otra clasificación de la obra",

}


# ======================================================================================
# FUNCIÓN AUXILIAR
# ======================================================================================

def nombre_variable(variable):

    return NOMBRES_VARIABLES.get(
        variable,
        variable
    )