"""
Algoritmo de CORRECCIÓN de errores: Código de Hamming - lado RECEPTOR.
Réplica de la lógica de codificación del Emisor (Go) del compañero
(emisor/main.go -> calcularHamming): bits indexados desde 1, las
posiciones potencia de 2 son de paridad, el resto son datos.

Nota: esta implementación corrige un único bit erróneo (limitación
estándar de Hamming simple). Si hay 2+ errores, puede "corregir" en la
posición equivocada o fallar en detectarlo -> se documenta como debilidad
en el reporte.
"""


def _es_potencia_de_dos(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def calcular_integridad(mensaje_bin: str) -> str:
    """
    EMISOR (referencia, ya implementado en Go por el compañero):
    intercala bits de datos y bits de paridad, calcula cada paridad con XOR.
    Se incluye aquí solo como referencia/documentación.
    """
    m = len(mensaje_bin)
    r = 0
    while (m + r + 1) > 2 ** r:
        r += 1
    n = m + r
    trama = [0] * (n + 1)  # índice 0 sin uso

    j = 0
    for i in range(1, n + 1):
        if _es_potencia_de_dos(i):
            trama[i] = 0
        else:
            trama[i] = int(mensaje_bin[j])
            j += 1

    i = 0
    while (1 << i) <= n:
        p = 1 << i
        paridad = 0
        for k in range(1, n + 1):
            if k & p:
                paridad ^= trama[k]
        trama[p] = paridad
        i += 1

    return "".join(str(b) for b in trama[1:])


def verificar_y_corregir(trama_bin: str):
    """
    RECEPTOR: recalcula los bits de paridad (síndrome) sobre la trama
    recibida. Si el síndrome != 0, esa es la posición del bit dañado
    (1-indexado); se corrige invirtiéndolo. Luego se extraen los bits de
    datos (posiciones que NO son potencia de 2).

    Devuelve: (hubo_error, corregido, posicion_error, mensaje_limpio_bin)
    """
    n = len(trama_bin)
    trama = [0] + [int(b) for b in trama_bin]  # índice 0 sin uso

    posicion_error = 0
    i = 0
    while (1 << i) <= n:
        p = 1 << i
        paridad = 0
        for k in range(1, n + 1):
            if k & p:
                paridad ^= trama[k]
        if paridad != 0:
            posicion_error += p
        i += 1

    hubo_error = posicion_error != 0
    corregido = False
    if hubo_error and 1 <= posicion_error <= n:
        trama[posicion_error] ^= 1
        corregido = True

    datos = [
        str(trama[k]) for k in range(1, n + 1) if not _es_potencia_de_dos(k)
    ]
    mensaje_limpio = "".join(datos)

    return hubo_error, corregido, (posicion_error if hubo_error else None), mensaje_limpio


if __name__ == "__main__":
    # Validado contra la salida real del Emisor en Go (mensaje "Hi", sin ruido)
    trama_referencia = "010010011000011001001"

    # sanity check: nuestra propia codificación debe coincidir con la del Go
    mensaje = "0100100001101001"  # "Hi" en ASCII binario (16 bits)
    propia = calcular_integridad(mensaje)
    print("trama propia :", propia)
    print("trama Go     :", trama_referencia)
    assert propia == trama_referencia, "No coincide con el Emisor en Go"
    print("OK: coincide con el Emisor en Go")

    print("\nverificar_y_corregir (sin error):", verificar_y_corregir(trama_referencia))

    # forzar 1 error
    t_err = list(trama_referencia)
    t_err[5] = "1" if t_err[5] == "0" else "0"
    t_err = "".join(t_err)
    print("verificar_y_corregir (1 error):", verificar_y_corregir(t_err))