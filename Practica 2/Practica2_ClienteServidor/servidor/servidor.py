import os
import time
import hashlib

# Ruta al directorio compartido (ajustar si la estructura cambia)
DIR_COMPARTIDO = os.path.join(os.path.dirname(__file__), "..", "compartido")
ARCHIVO_ENTRADA = os.path.join(DIR_COMPARTIDO, "entrada_servidor.txt")
ARCHIVO_SALIDA = os.path.join(DIR_COMPARTIDO, "salida_servidor.txt")

# Garantizar que el directorio y los archivos existan al iniciar
os.makedirs(DIR_COMPARTIDO, exist_ok=True)
for ruta in (ARCHIVO_ENTRADA, ARCHIVO_SALIDA):
    if not os.path.exists(ruta):
        with open(ruta, "w", encoding="utf-8") as f:
            pass

def calcular_hash(texto: str) -> str:
    """Genera un hash SHA-256 para identificar el contenido de forma única."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

def procesar_mensaje(mensaje: str) -> str:
    """Lógica de negocio del servidor."""
    mensaje_limpio = mensaje.strip()
    texto_mayus = mensaje_limpio.upper()
    longitud = len(mensaje_limpio)
    return f"PROCESADO: [{texto_mayus}] | Longitud: {longitud} caracteres"

def main():
    print("==========================================")
    print(" [SERVIDOR] Servicio activo y escuchando... ")
    print("==========================================")
    
    ultimo_hash_procesado = None

    try:
        while True:
            if os.path.exists(ARCHIVO_ENTRADA):
                try:
                    with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
                        contenido = f.read().strip()

                    # Verificar que el archivo no esté vacío
                    if contenido:
                        hash_actual = calcular_hash(contenido)

                        # Evitar reprocesar el mismo mensaje
                        if hash_actual != ultimo_hash_procesado:
                            print(f"\n[SERVIDOR] Nuevo mensaje detectado: '{contenido}'")
                            
                            resultado = procesar_mensaje(contenido)
                            
                            # Escribir la respuesta en la salida
                            with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
                                f.write(resultado + "\n")
                            
                            ultimo_hash_procesado = hash_actual
                            print(f"[SERVIDOR] Respuesta generada: '{resultado}'")
                
                except PermissionError:
                    # Ocurre si el cliente está escribiendo en el mismo instante
                    pass
                except Exception as e:
                    print(f"[SERVIDOR] Error al procesar: {e}")

            time.sleep(1)  # Sondeo periódico (polling)

    except KeyboardInterrupt:
        print("\n[SERVIDOR] Deteniendo servicio de forma segura...")

if __name__ == "__main__":
    main()