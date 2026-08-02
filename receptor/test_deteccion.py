"""
Pruebas automatizadas de los algoritmos de detección (Fletcher) y
corrección (Hamming), aisladas del Emisor real, para sacar evidencia
rápida para el reporte (3 mensajes x 3 escenarios de error).

Para la evidencia "oficial" del laboratorio se recomienda además correr
el flujo real: emisor/main.go (Go) -> pegar la trama -> receptor.py
"""

import fletcher_deteccion as fletcher
import hamming_correccion as hamming


def texto_a_bin(texto: str) -> str:
    return "".join(f"{ord(c):08b}" for c in texto)


def flip(bits: str, *posiciones) -> str:
    b = list(bits)
    for p in posiciones:
        b[p] = "1" if b[p] == "0" else "0"
    return "".join(b)


mensajes = ["Hi", "Hola", "UVG Redes 2026"]

print("=" * 60)
print("ALGORITMO DE DETECCIÓN: Fletcher checksum")
print("=" * 60)
for msg in mensajes:
    m_bin = texto_a_bin(msg)
    trama = fletcher.calcular_integridad(m_bin)
    print(f"\nMensaje: {msg!r} | mensaje: {len(m_bin)} bits | trama: {len(trama)} bits")
    print("  Prueba 1 (0 errores):        ", "SIN ERRORES" if fletcher.verificar_integridad(trama) else "ERROR DETECTADO")
    print("  Prueba 2 (1 error, bit 3):   ", "SIN ERRORES" if fletcher.verificar_integridad(flip(trama, 3)) else "ERROR DETECTADO")
    print("  Prueba 3 (2 errores, 3 y 7): ", "SIN ERRORES" if fletcher.verificar_integridad(flip(trama, 3, 7)) else "ERROR DETECTADO")

print("\n" + "=" * 60)
print("ALGORITMO DE CORRECCIÓN: Código de Hamming")
print("=" * 60)
for msg in mensajes:
    m_bin = texto_a_bin(msg)
    trama = hamming.calcular_integridad(m_bin)
    print(f"\nMensaje: {msg!r} | mensaje: {len(m_bin)} bits | trama: {len(trama)} bits")

    r1 = hamming.verificar_y_corregir(trama)
    print("  Prueba 1 (0 errores):        hubo_error=%s" % r1[0])

    r2 = hamming.verificar_y_corregir(flip(trama, 3))
    print(f"  Prueba 2 (1 error, bit 3):   hubo_error={r2[0]} corregido={r2[1]} pos={r2[2]} OK={r2[3] == m_bin}")

    r3 = hamming.verificar_y_corregir(flip(trama, 3, 7))
    print(f"  Prueba 3 (2 errores, 3 y 7): hubo_error={r3[0]} corregido={r3[1]} pos={r3[2]} OK={r3[3] == m_bin}")

print("\n--- Debilidades estructurales (para la discusión del reporte) ---")
print("Fletcher: existen combinaciones de bits alterados que producen el")
print("mismo checksum (colisión) -> no se detectan. Ejemplo típico: dos")
print("errores que se cancelan dentro de la suma mod 255 del mismo bloque.")
print("Hamming simple: corrige 1 bit, pero con 2+ errores puede 'corregir'")
print("una posición incorrecta y entregar un mensaje corrupto sin avisar")
print("(ver Prueba 3 arriba: OK=False en varios casos).")