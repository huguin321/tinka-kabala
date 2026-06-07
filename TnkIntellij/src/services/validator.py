from collections import Counter

from scipy.spatial import distance


# =========================
# VALIDAR REPETICIONES HISTÓRICAS
# =========================
def validate_repetitions(combination, winning_combinations, max_shared_history_numbers):
    """
    Evita combinaciones demasiado similares a sorteos históricos.
    """
    combo_set = set(combination)

    for previous_combination, fecha in winning_combinations.items():
        coincidentes = combo_set & set(previous_combination)
        coincidencias = len(coincidentes)

        if coincidencias > max_shared_history_numbers:
            return False, (
                f"Demasiados números repetidos "
                f"({coincidencias} coincidentes: {sorted(coincidentes)}) "
                f"con {previous_combination} del {fecha}"
            )

    return True, "OK"


# =========================
# VALIDAR PATRÓN DE DIFERENCIAS
# =========================
def calculate_difference_pattern(combination, history):
    """
    Evita repetir exactamente el mismo patrón de diferencias
    entre números consecutivos.
    """
    def get_differences(nums):
        return [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]

    combinacion_dif = get_differences(combination)

    for hist in history:
        if get_differences(hist) == combinacion_dif:
            return False

    return True


# =========================
# SIMILITUD JACCARD
# =========================
def jaccard_similarity(set_a, set_b):
    """
    Calcula similitud Jaccard entre dos conjuntos.
    Resultado entre 0.0 (nada en común) y 1.0 (idénticos).
    """
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)

    if union == 0:
        return 0.0

    return intersection / union


# =========================
# OBTENER COMBINACIÓN MÁS CERCANA
# =========================
def get_closest_combination(combination, history, winning_combinations):
    """
    Busca la combinación histórica más cercana usando
    distancia euclidiana y similitud Jaccard.
    """
    min_dist = float('inf')
    max_jaccard = 0.0
    closest_euclidean = None
    closest_jaccard = None
    combo_set = set(combination)

    for hist in history:
        dist = distance.euclidean(combination, hist)
        if dist < min_dist:
            min_dist = dist
            closest_euclidean = hist

        jac = jaccard_similarity(combo_set, set(hist))
        if jac > max_jaccard:
            max_jaccard = jac
            closest_jaccard = hist

    fecha_euclidean = (
        winning_combinations.get(tuple(sorted(closest_euclidean)), "fecha desconocida")
        if closest_euclidean is not None else "fecha desconocida"
    )

    fecha_jaccard = (
        winning_combinations.get(tuple(sorted(closest_jaccard)), "fecha desconocida")
        if closest_jaccard is not None else "fecha desconocida"
    )

    return closest_euclidean, fecha_euclidean, min_dist, closest_jaccard, fecha_jaccard, max_jaccard


# =========================
# VALIDAR COMBINACIÓN
# =========================
def validate_combination(combination, history, winning_combinations, game_config):
    """
    Valida una combinación según las reglas definidas en game_config.py
    """
    min_number = game_config["min_number"]
    max_number = game_config["max_number"]
    min_distance = game_config["min_distance"]
    max_jaccard_similarity = game_config["max_jaccard_similarity"]
    max_consecutive = game_config["max_consecutive"]
    min_range = game_config["min_range"]
    max_even = game_config["max_even"]
    max_odd = game_config["max_odd"]
    max_repeated_recent = game_config["max_repeated_recent"]
    max_shared_history_numbers = game_config["max_shared_history_numbers"]
    block_double_sequences = game_config["block_double_sequences"]
    block_triple_double_sequences = game_config["block_triple_double_sequences"]
    block_difference_pattern = game_config["block_difference_pattern"]
    numbers_count = game_config["numbers_count"]
    midpoint_spread = game_config["midpoint_spread"]

    # =========================
    # REPETICIONES HISTÓRICAS
    # =========================
    is_valid, reason = validate_repetitions(
        combination, winning_combinations, max_shared_history_numbers
    )
    if not is_valid:
        return False, reason

    # =========================
    # CONSECUTIVOS
    # =========================
    consecutivos = sum(
        1 for i in range(len(combination) - 1)
        if combination[i] + 1 == combination[i + 1]
    )
    if consecutivos >= max_consecutive + 1:
        return False, "Demasiados consecutivos"

    # =========================
    # RANGO
    # =========================
    if combination[-1] - combination[0] <= min_range:
        return False, "Amontonados"

    # =========================
    # MUY BAJOS / MUY ALTOS
    # =========================
    midpoint = (min_number + max_number) // 2
    if combination[-1] <= midpoint - midpoint_spread:
        return False, "Muy menores"
    if combination[0] >= midpoint + midpoint_spread:
        return False, "Muy mayores"

    # =========================
    # PARES / IMPARES
    # =========================
    pares = sum(1 for n in combination if n % 2 == 0)
    impares = numbers_count - pares
    if pares > max_even:
        return False, "Muchos números pares"
    if impares > max_odd:
        return False, "Muchos números impares"

    # =========================
    # REPETIDOS RECIENTES
    # =========================
    if history:
        apariciones = Counter(
            num
            for sorteo in history
            for num in sorteo
        )

        repetidos = [
            n for n in combination
            if apariciones.get(n, 0) > max_repeated_recent
        ]

        if repetidos:
            return False, f"Números repetidos recientes: {repetidos}"

    # =========================
    # DOBLES
    # =========================
    pares_consecutivos = [
        (combination[i], combination[i + 1])
        for i in range(len(combination) - 1)
        if combination[i] + 1 == combination[i + 1]
    ]
    if block_triple_double_sequences and len(pares_consecutivos) >= 3:
        return False, "Dobles por doquier"
    if block_double_sequences and len(pares_consecutivos) >= 2:
        return False, "Dobles detectados"

    # =========================
    # DISTANCIA Y JACCARD
    # =========================
    if history:
        closest_euclidean, fecha_euclidean, distancia, \
            closest_jaccard, fecha_jaccard, similitud_jaccard = get_closest_combination(
            combination, history, winning_combinations
        )

        if distancia < min_distance:
            return False, (
                f"Demasiado similar (euclidiana) a {closest_euclidean} "
                f"del {fecha_euclidean} "
                f"(distancia={round(distancia, 2)})"
            )

        if similitud_jaccard >= max_jaccard_similarity:
            return False, (
                f"Demasiado similar (Jaccard) a {closest_jaccard} "
                f"del {fecha_jaccard} "
                f"(similitud={round(similitud_jaccard, 2)})"
            )

    # =========================
    # PATRÓN
    # =========================
    if block_difference_pattern:
        if not calculate_difference_pattern(combination, history):
            return False, "Patrón repetido"

    return True, "Válida"