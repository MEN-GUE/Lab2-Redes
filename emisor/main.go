package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"
)

// 1. CAPA DE APLICACION
func solicitarMensaje() (string, int) {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Ingrese el mensaje a enviar: ")
	mensaje, _ := reader.ReadString('\n')
	
	fmt.Println("Seleccione el algoritmo (1: Detección, 2: Corrección): ")
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

// 3. CAPA DE ENLACE (Esqueleto)
func calcularIntegridad(mensajeBinario string, algoritmo int) string {
	// TODO: Aquí implementar lógica de CRC-32, Fletcher, Hamming o Viterbi
	redundancia := "0000" // Placeholder temporal
	return mensajeBinario + redundancia
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
	fmt.Print("\nIngrese la tasa de error (ej. 0.01 para 1/100): ")
	fmt.Scanln(&tasaError)
	
	tramaFinal := aplicarRuido(trama, tasaError)
	
	// Salida final para copiar y pegar en el Receptor durante las pruebas manuales[cite: 1]
	fmt.Println("\n=========================================")
	fmt.Println("--- TRAMA FINAL PARA EL RECEPTOR ---")
	fmt.Println(tramaFinal)
	fmt.Println("=========================================")
}