import os
import time

DIR_COMPARTIDO = os.path.join(os.path.dirname(__file__), "..", "compartido")
ARCHIVO_ENTRADA = os.path.join(DIR_COMPARTIDO, "entrada_servidor.txt")
ARCHIVO_SALIDA = os.path.join(DIR_COMPARTIDO, "salida_servidor.txt")

os.makedirs(DIR_COMPARTIDO, exist_ok=True)

def obtener_contenido_salida() -> str:
    """Lee el archivo de salida si existe y no está vacío."""
    if os.path.exists(ARCHIVO_SALIDA):
        try:
            with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
                return f.read().strip()
        except PermissionError:
            return ""
    return ""

def enviar_mensaje(mensaje: str, tiempo_espera_max: int = 10):
    print(f"\n[CLIENTE] Escribiendo mensaje: '{mensaje}'...")
    
    # Capturar respuesta previa para verificar cuando cambie
    respuesta_previa = obtener_contenido_salida()

    # Escribir el nuevo mensaje en la entrada
    with open(ARCHIVO_ENTRADA, "w", encoding="utf-8") as f:
        f.write(mensaje + "\n")

    print("[CLIENTE] Esperando respuesta del servidor...")
    
    inicio = time.time()
    while time.time() - inicio < tiempo_espera_max:
        respuesta_actual = obtener_contenido_salida()

        # Si hay un nuevo contenido en la salida diferente al anterior
        if respuesta_actual and respuesta_actual != respuesta_previa:
            print(f"[CLIENTE] <<< Respuesta recibida: {respuesta_actual}")
            return
        
        time.sleep(0.5)  # Simulación de latencia / espera activa

    print("[CLIENTE] Timeout: El servidor no respondió dentro del tiempo esperado.")

def main():
    print("==========================================")
    print("           [CLIENTE INTERACTIVO]          ")
    print("==========================================")
    
    while True:
        try:
            msg = input("\nIngrese un mensaje para enviar (o 'salir' para terminar): ").strip()
            if msg.lower() == 'salir':
                print("[CLIENTE] Finalizando sesión.")
                break
            if not msg:
                print("[CLIENTE] Por favor, ingrese un mensaje válido (no vacío).")
                continue

            enviar_mensaje(msg)

        except KeyboardInterrupt:
            print("\n[CLIENTE] Salida forzada.")
            break

if __name__ == "__main__":
    main()