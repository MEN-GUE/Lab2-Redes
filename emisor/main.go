package main

import (
	"bufio"
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

// 1. CAPA DE APLICACION
func solicitarMensaje() (string, int) {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Ingrese el mensaje a enviar: ")
	mensaje, _ := reader.ReadString('\n')

	fmt.Println("Seleccione el algoritmo (1: Detección [Fletcher], 2: Corrección [Hamming]): ")
	var algoritmo int
	fmt.Scanln(&algoritmo)

	return strings.TrimSpace(mensaje), algoritmo
}

// 2. CAPA DE PRESENTACION
func codificarMensaje(mensaje string) string {
	var binario strings.Builder
	for _, c := range mensaje {
		// %08b asegura que cada caracter se represente con 8 bits
		binario.WriteString(fmt.Sprintf("%08b", c))
	}
	return binario.String()
}

// ALGORITMO 1: Fletcher Checksum (Detección de Errores)
func calcularFletcher(binario string) string {
	var sum1, sum2 int
	
	// Divide en bloques de 8 bits[cite: 2]
	for i := 0; i < len(binario); i += 8 {
		end := i + 8
		if end > len(binario) {
			end = len(binario)
		}
		bloque := binario[i:end]

		// Convertir el bloque binario a entero
		valor, _ := strconv.ParseInt(bloque, 2, 64)
		
		sum1 = (sum1 + int(valor)) % 255
		sum2 = (sum2 + sum1) % 255
	}

	// Retorna la trama original concatenada con los dos bytes del checksum (16 bits extras en total)
	checksum := fmt.Sprintf("%08b%08b", sum1, sum2)
	return binario + checksum
}

// ALGORITMO 2: Código de Hamming (Corrección de Errores)
func calcularHamming(binario string) string {
	m := len(binario)
	r := 0

	// Calcular la cantidad de bits de redundancia r cumpliendo (m+r+1) <= 2^r[cite: 2]
	for (m + r + 1) > int(math.Pow(2, float64(r))) {
		r++
	}

	n := m + r
	// Arreglo indexado desde 1 para facilitar las matemáticas de Hamming
	trama := make([]int, n+1)

	// Intercalar bits de datos y dejar en 0 los espacios para los bits de paridad (potencias de 2)
	j := 0
	for i := 1; i <= n; i++ {
		// Verificamos si la posición 'i' es potencia de 2 usando bitwise AND
		if (i & (i - 1)) == 0 {
			trama[i] = 0 // Espacio para bit de paridad
		} else {
			if binario[j] == '1' {
				trama[i] = 1
			} else {
				trama[i] = 0
			}
			j++
		}
	}

	// Calcular el valor (XOR) de los bits de paridad
	for i := 0; i < r; i++ {
		posicionParidad := 1 << i // Equivalente a 2^i (1, 2, 4, 8, 16...)
		paridad := 0
		for k := 1; k <= n; k++ {
			// Si el bit en la posición k aporta a esta paridad
			if (k & posicionParidad) != 0 {
				paridad ^= trama[k]
			}
		}
		trama[posicionParidad] = paridad
	}

	// Construir el string binario final
	var resultado strings.Builder
	for i := 1; i <= n; i++ {
		if trama[i] == 1 {
			resultado.WriteRune('1')
		} else {
			resultado.WriteRune('0')
		}
	}

	return resultado.String()
}

// 3. CAPA DE ENLACE
func calcularIntegridad(mensajeBinario string, algoritmo int) string {
	if algoritmo == 1 {
		fmt.Println("[Enlace] Aplicando Fletcher Checksum...")
		return calcularFletcher(mensajeBinario)
	} else if algoritmo == 2 {
		fmt.Println("[Enlace] Aplicando Código de Hamming...")
		return calcularHamming(mensajeBinario)
	}
	
	fmt.Println("[Alerta] Algoritmo no válido. Devolviendo trama original.")
	return mensajeBinario
}

// 4. RUIDO
func aplicarRuido(trama string, probabilidad float64) string {
	rand.Seed(time.Now().UnixNano())
	var tramaConRuido strings.Builder
	
	for _, bit := range trama {
		if rand.Float64() < probabilidad {
			// Invertir el bit si entra en la probabilidad de error
			if bit == '0' {
				tramaConRuido.WriteRune('1')
			} else {
				tramaConRuido.WriteRune('0')
			}
		} else {
			tramaConRuido.WriteRune(bit)
		}
	}
	return tramaConRuido.String()
}

func main() {
	fmt.Println("--- INICIANDO EMISOR ---")
	
	// Flujo de Aplicación
	mensaje, algoritmo := solicitarMensaje()
	
	// Flujo de Presentación
	binario := codificarMensaje(mensaje)
	fmt.Println("[Presentación] Mensaje binario original:", binario)
	
	// Flujo de Enlace
	trama := calcularIntegridad(binario, algoritmo)
	fmt.Println("[Enlace] Trama con redundancia:", trama)
	
	// Flujo de Ruido
	var tasaError float64
	fmt.Print("\nIngrese la tasa de error (ej. 0.01 para 1/100, 0 para sin error): ")
	fmt.Scanln(&tasaError)
	
	tramaFinal := aplicarRuido(trama, tasaError)
	
	// Salida
	fmt.Println("\n=========================================")
	fmt.Println("--- TRAMA FINAL PARA EL RECEPTOR ---")
	fmt.Println(tramaFinal)
	fmt.Println("=========================================")
}