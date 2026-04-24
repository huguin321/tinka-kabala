import math

from scipy.spatial import distance


def calculate_entropy(combination):
    valores = list(set(combination))
    probabilidades = [combination.count(v) / len(combination) for v in valores]
    entropia = -sum(p * math.log2(p) for p in probabilidades)
    return entropia


def validate_repetitions(combination, winning_combinations):
    for previous_combination, fecha in winning_combinations.items():
        coincidentes = sorted([num for num in combination if num in previous_combination])
        coincidencias = len(coincidentes)

        if coincidencias > 4:
            return False, (
                f"Demasiados números repetidos "
                f"({coincidencias} coincidencias: {coincidentes}) "
                f"con {previous_combination} del {fecha}"
            )

    return True, "OK"


def calculate_difference_pattern(combination, history):
    def get_differences(nums):
        return [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]

    combinacion_dif = get_differences(combination)

    for hist in history:
        if get_differences(hist) == combinacion_dif:
            return False

    return True


def get_closest_combination(combination, history, winning_combinations):
    if not history:
        return None, "sin historial", float('inf')

    min_dist = float('inf')
    closest = None

    for hist in history:
        dist = distance.euclidean(combination, hist)
        if dist < min_dist:
            min_dist = dist
            closest = hist

    fecha = winning_combinations.get(tuple(sorted(closest)), "fecha desconocida")

    return closest, fecha, min_dist


def validate_combination(combination, history, winning_combinations):
    # Repeticiones históricas
    is_valid, reason = validate_repetitions(combination, winning_combinations)
    if not is_valid:
        return False, reason

    # Consecutivos
    consecutivos = sum(1 for i in range(5) if combination[i] + 1 == combination[i + 1])
    if consecutivos >= 3:
        return False, "Demasiados consecutivos"

    # Rango agrupado
    if combination[-1] - combination[0] <= 17:
        return False, "Amontonados"

    # Muy bajos / muy altos
    if combination[-1] <= 23:
        return False, "Muy menores"
    if combination[0] >= 27:
        return False, "Muy mayores"

    # Pares / impares
    pares = sum(1 for n in combination if n % 2 == 0)
    impares = 6 - pares

    if pares >= 5:
        return False, "Muchos números pares"
    if impares >= 5:
        return False, "Muchos números impares"

    # Repeticiones en últimos 4 sorteos
    if len(history) >= 4:
        ultimos_4 = history[:4]

        apariciones = {}
        for sorteo in ultimos_4:
            for num in sorteo:
                apariciones[num] = apariciones.get(num, 0) + 1

        repetidos = [n for n in combination if apariciones.get(n, 0) > 2]

        if repetidos:
            return False, f"Números repetidos 2+ veces: {repetidos}"

    # Dobles consecutivos
    cont1 = 0
    if combination[0] == combination[1] - 1 and combination[1] == combination[2] - 1:
        cont1 += 1
    if combination[3] == combination[4] - 1 and combination[4] == combination[5] - 1:
        cont1 += 1
    if cont1 == 2:
        return False, "Dobles consecutivos detectados"

    # Dobles por doquier
    if (combination[0] == combination[1] - 1 and
            combination[2] == combination[3] - 1 and
            combination[4] == combination[5] - 1):
        return False, "Dobles por doquier"

    # Dobles
    if ((combination[2] == combination[3] - 1 and combination[4] == combination[5] - 1) or
            (combination[1] == combination[2] - 1 and combination[3] == combination[4] - 1) or
            (combination[1] == combination[2] - 1 and combination[4] == combination[5] - 1) or
            (combination[0] == combination[1] - 1 and combination[2] == combination[3] - 1) or
            (combination[0] == combination[1] - 1 and combination[3] == combination[4] - 1) or
            (combination[0] == combination[1] - 1 and combination[4] == combination[5] - 1)):
        return False, "Dobles detectados"

    # Distancia (MEJORADA)
    closest, fecha, distancia = get_closest_combination(
        combination,
        history,
        winning_combinations
    )

    if distancia < 5.0:
        return False, (
            f"Demasiado similar a {closest} del {fecha} "
            f"(distancia={round(distancia, 2)})"
        )

    # Patrón
    if not calculate_difference_pattern(combination, history):
        return False, "Patrón repetido"

    return True, "Válida"
