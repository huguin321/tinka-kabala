TINKA_CONFIG = {
    "name": "Tinka",
    "table": "TblTinka",

    # Juego
    "min_number": 1,
    "max_number": 53,
    "numbers_count": 6,

    # Historial
    "last_draws_limit": 5,

    # Distancia euclidiana mínima vs últimos sorteos
    # Formato: número decimal con punto (NO coma)
    # Ejemplos válidos:   5.0 | 5.11 | 5.9425 | 4.1234
    # Ejemplos inválidos: 5,0 | "5.0" | cinco | 5,9425
    # Precisión: hasta 4 decimales recomendado
    # Mayor valor = más restrictivo | Menor valor = más permisivo
    "min_distance": 4.5,

    # Similitud Jaccard mínima para rechazar (0.0 a 1.0)
    # Mide cuántos números comparten dos combinaciones
    # Ejemplo: {1,2,3,4,5,6} vs {1,2,3,4,5,7} = 5/7 = 0.71
    # Ejemplo: {1,2,3,4,5,6} vs {7,8,9,10,11,12} = 0/12 = 0.0
    # Mayor valor = más restrictivo | Menor valor = más permisivo
    # Recomendado: 0.6 a 0.8
    "max_jaccard_similarity": 0.7,

    # Máximo de consecutivos permitidos
    "max_consecutive": 2,

    # Rango mínimo entre menor y mayor número
    "min_range": 18,

    # Máximo de pares e impares permitidos
    "max_even": 4,
    "max_odd": 4,

    # Máximo de repeticiones recientes permitidas
    "max_repeated_recent": 2,

    # Máxima coincidencia con sorteos históricos
    "max_shared_history_numbers": 4,  # maximo -1 caliente de numero permitido

    # Margen desde el punto medio para rechazar combinaciones muy bajas o muy altas
    # Ejemplo: midpoint=27, spread=3 → rechaza si max<=24 o si min>=30
    "midpoint_spread": 3,

    # Activar/desactivar reglas
    "block_double_sequences": True,
    "block_triple_double_sequences": True,
    "block_difference_pattern": True
}

KABALA_CONFIG = {
    "name": "Kabala",
    "table": "TblKabala",

    # Juego
    "min_number": 1,
    "max_number": 40,
    "numbers_count": 6,

    # Historial
    "last_draws_limit": 7,

    # Distancia euclidiana mínima vs últimos sorteos
    # Formato: número decimal con punto (NO coma)
    # Ejemplos válidos:   5.0 | 5.11 | 5.9425 | 4.1234
    # Ejemplos inválidos: 5,0 | "5.0" | cinco | 5,9425
    # Precisión: hasta 4 decimales recomendado
    # Mayor valor = más restrictivo | Menor valor = más permisivo
    "min_distance": 4.5,

    # Similitud Jaccard mínima para rechazar (0.0 a 1.0)
    # Mide cuántos números comparten dos combinaciones
    # Ejemplo: {1,2,3,4,5,6} vs {1,2,3,4,5,7} = 5/7 = 0.71
    # Ejemplo: {1,2,3,4,5,6} vs {7,8,9,10,11,12} = 0/12 = 0.0
    # Mayor valor = más restrictivo | Menor valor = más permisivo
    # Recomendado: 0.6 a 0.8
    "max_jaccard_similarity": 0.7,

    # Máximo de consecutivos permitidos
    "max_consecutive": 2,

    # Rango mínimo entre menor y mayor número
    "min_range": 18,

    # Máximo de pares e impares permitidos
    "max_even": 4,
    "max_odd": 4,

    # Máximo de repeticiones recientes permitidas
    "max_repeated_recent": 2,

    # Máxima coincidencia con sorteos históricos
    "max_shared_history_numbers": 4,  # maximo -1 caliente de numero permitido

    # Margen desde el punto medio para rechazar combinaciones muy bajas o muy altas
    # Ejemplo: midpoint=20, spread=3 → rechaza si max<=17 o si min>=23
    "midpoint_spread": 3,

    # Activar/desactivar reglas
    "block_double_sequences": True,
    "block_triple_double_sequences": True,
    "block_difference_pattern": True
}