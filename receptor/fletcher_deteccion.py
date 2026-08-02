"""
Algoritmo de DETECCIÓN de errores: Fletcher checksum (bloques de 8 bits).
Réplica exacta de la lógica implementada en el Emisor para que el Receptor en Python sea
100% compatible con las tramas que ese programa genera.

sum1, sum2 acumulados mod 255, cada uno codificado en 8 bits -> 16 bits
de redundancia total.
"""

N_CHECKSUM = 16  # bits de redundancia (8 + 8)


def calcular_fletcher(mensaje_bin: str) -> str:
    """Calcula únicamente los 16 bits de checksum de Fletcher."""
    sum1 = 0
    sum2 = 0
    for i in range(0, len(mensaje_bin), 8):
        bloque = mensaje_bin[i : i + 8]
        valor = int(bloque, 2)
        sum1 = (sum1 + valor) % 255
        sum2 = (sum2 + sum1) % 255
    return f"{sum1:08b}{sum2:08b}"


def calcular_integridad(mensaje_bin: str) -> str:
    """EMISOR (referencia): mensaje + checksum de Fletcher."""
    return mensaje_bin + calcular_fletcher(mensaje_bin)


def verificar_integridad(trama_bin: str) -> bool:
    """
    RECEPTOR: separa mensaje/checksum, recalcula el checksum sobre el
    mensaje recibido y compara. True = sin error, False = error detectado.
    """
    if len(trama_bin) <= N_CHECKSUM:
        return False
    mensaje = trama_bin[: len(trama_bin) - N_CHECKSUM]
    checksum_recibido = trama_bin[len(trama_bin) - N_CHECKSUM :]
    return calcular_fletcher(mensaje) == checksum_recibido


if __name__ == "__main__":
    # Validado contra la salida real del Emisor en Go (mensaje "Hola", sin ruido)
    trama_referencia = "010010000110111101101100011000011000010110101001"
    print("verificar_integridad (trama real de Go):", verificar_integridad(trama_referencia))
    assert verificar_integridad(trama_referencia) is True
    print("OK: coincide con el Emisor en Go")