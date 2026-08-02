"""
No hay conexión real por red: la trama se pega manualmente (input),
tal como indica la guía resumida del laboratorio.
"""

import fletcher_deteccion as fletcher
import hamming_correccion as hamming


# ---------------------------------------------------------------------------
# CAPA TRANSMISIÓN
# ---------------------------------------------------------------------------
def recibir_informacion() -> str:
    """Simula la recepción de la trama (pegada manualmente desde el Emisor)."""
    trama = input("Pega la trama binaria recibida del emisor: ").strip()
    if not trama or not all(c in "01" for c in trama):
        raise ValueError("La trama debe contener únicamente 0s y 1s.")
    return trama


# ---------------------------------------------------------------------------
# CAPA ENLACE
# ---------------------------------------------------------------------------
def verificar_integridad(trama: str, algoritmo: int):
    """
    Devuelve (estado, mensaje_bin_o_None, posicion_error_o_None)
    estado ∈ {"OK", "CORREGIDO", "ERROR"}
    """
    if algoritmo == 1:  # Fletcher (detección)
        sin_error = fletcher.verificar_integridad(trama)
        if sin_error:
            mensaje_bin = trama[: len(trama) - fletcher.N_CHECKSUM]
            return "OK", mensaje_bin, None
        return "ERROR", None, None  # Fletcher solo detecta, no corrige

    elif algoritmo == 2:  # Hamming (corrección)
        hubo_error, corregido, pos, mensaje_limpio = hamming.verificar_y_corregir(trama)
        if not hubo_error:
            return "OK", mensaje_limpio, None
        elif corregido:
            return "CORREGIDO", mensaje_limpio, pos
        else:
            return "ERROR", None, pos

    else:
        raise ValueError("Algoritmo no soportado: usa 1 (Fletcher) o 2 (Hamming)")


# ---------------------------------------------------------------------------
# CAPA PRESENTACIÓN
# ---------------------------------------------------------------------------
def decodificar_mensaje(mensaje_bin: str) -> str:
    """Decodifica ASCII binario (8 bits/carácter) a texto, como el Emisor lo codificó."""
    if not mensaje_bin or len(mensaje_bin) % 8 != 0:
        return mensaje_bin  # no es un múltiplo de 8; se muestra crudo
    try:
        chars = [chr(int(mensaje_bin[i : i + 8], 2)) for i in range(0, len(mensaje_bin), 8)]
        texto = "".join(chars)
        if all(c.isprintable() or c in "\n\t" for c in texto):
            return texto
    except ValueError:
        pass
    return mensaje_bin


# ---------------------------------------------------------------------------
# CAPA APLICACIÓN
# ---------------------------------------------------------------------------
def mostrar_mensaje(estado: str, mensaje_bin, pos_error):
    print("-" * 50)
    if estado == "OK":
        print("Trama recibida SIN ERRORES.")
        print("Mensaje:", decodificar_mensaje(mensaje_bin))
    elif estado == "CORREGIDO":
        print(f"Se detectó un error en la posición {pos_error} y fue CORREGIDO.")
        print("Trama original limpia:", mensaje_bin)
        print("Mensaje:", decodificar_mensaje(mensaje_bin))
    else:  # ERROR
        print("ERROR: se detectó un error en la trama. Trama descartada.")
    print("-" * 50)


def main():
    print("=== RECEPTOR (Python) - Lab 2 Redes ===")
    algoritmo = int(input("Algoritmo usado por el emisor (1: Fletcher, 2: Hamming): ").strip())
    trama = recibir_informacion()
    estado, mensaje_bin, pos = verificar_integridad(trama, algoritmo)
    mostrar_mensaje(estado, mensaje_bin, pos)


if __name__ == "__main__":
    main()