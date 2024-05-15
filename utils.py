import math
import numpy as np


# Función para calcular la desviación estándar
def calcular_desviacion_estandar(datos):
    media = sum(datos) / len(datos)
    varianza = sum((x - media) ** 2 for x in datos) / len(datos)
    return varianza**0.5


def calcular_mediana(arreglo):
    # Ordena el arreglo
    arreglo_ordenado = sorted(arreglo)
    n = len(arreglo_ordenado)

    # Si la cantidad de elementos es impar
    if n % 2 == 1:
        mediana = arreglo_ordenado[n // 2]
    # Si la cantidad de elementos es par
    else:
        mediana = (arreglo_ordenado[n // 2 - 1] + arreglo_ordenado[n // 2]) / 2

    return mediana


def create_first_solution(
    codification: str,
    limits: int = 0,
    bits_enteros: int = 0,
    bits_decimales: int = 0,
    variables: int = 0,
) -> list[int]:

    first_solution = []

    if codification == "binary":
        first_solution = np.random.choice(
            [0, 1],
            size=(bits_enteros + bits_decimales + 1) * variables,
        )

    if codification == "combination":
        first_solution = np.random.randint(1, limits + 1, size=limits)

    if codification == "permutation":
        first_solution = np.arange(1, limits + 1)
        np.random.shuffle(first_solution)

    return first_solution


def calcular_bits(rango_entero: int, precision: float):
    bits_enteros = math.ceil(math.log2(rango_entero))

    bits_decimales = math.ceil(math.log2(1 / precision))
    return bits_enteros, bits_decimales


def decodificar_solución(solucion, bits_enteros, bits_decimales, precision):
    tamano_soluciones = bits_enteros + bits_decimales + 1
    sub_arreglos = extraer_subarreglos(solucion, tamano_soluciones)
    sub_arreglos = list(
        map(lambda x: validar_decimal(x, bits_decimales, precision), sub_arreglos)
    )
    variables_decodificadas = list(
        map(lambda x: decodificar_arreglo_variable(x, bits_enteros), sub_arreglos)
    )
    return variables_decodificadas


def extraer_subarreglos(arreglo, tamano):
    sub_arreglos = []
    for i in range(0, len(arreglo), tamano):
        sub_arreglo = arreglo[i : i + tamano]
        sub_arreglos.append(sub_arreglo)
    return sub_arreglos


def validar_min_max(delta_E, min_or_max):
    if min_or_max == "max":
        return delta_E > 0
    else:
        return delta_E <= 0


def decodificar_arreglo_variable(num_binario, indice_parte_entera):
    numero_codificado = 0
    entera_binario, decimal_binario = (
        num_binario[1 : indice_parte_entera + 1],
        num_binario[indice_parte_entera + 1 :],
    )
    entera = int("".join(str(c) for c in entera_binario), 2)
    decimal = int("".join(str(c) for c in decimal_binario), 2)

    div = 10 ** len(str(decimal))
    numero_codificado = entera + (decimal / div)

    numero_codificado *= -1 if num_binario[0] == 1 else 1

    return numero_codificado


def validar_decimal(arreglo, indice_inicio_decimal, precision):
    parte_decimal = int("".join(map(str, arreglo[indice_inicio_decimal + 1 :])), 2)
    modulo = calcular_modulo(precision)
    parte_decimal_bin = convert_to_binary(
        parte_decimal % modulo, len(arreglo) - indice_inicio_decimal
    )
    arreglo[indice_inicio_decimal:] = parte_decimal_bin
    return arreglo


def calcular_modulo(precision):
    modulo = int(1 / precision) + 1
    return modulo


def convert_to_binary(numero, num_bits):
    representacion_binaria = bin(numero)[2:]  # Elimina el prefijo '0b'
    arreglo_binario = [int(bit) for bit in representacion_binaria]

    # Asegurar que el arreglo tenga el tamaño especificado
    while len(arreglo_binario) < num_bits:
        arreglo_binario.insert(0, 0)  # Agregar ceros al principio

    return arreglo_binario
