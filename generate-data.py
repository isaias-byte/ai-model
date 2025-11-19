import requests
import random
import time

# --- Configuración del Script ---
API_URL = "http://127.0.0.1:3000/api/create-transaction-test-populate/"
NUMERO_DE_TRANSACCIONES = 5000
USER_ID_MIN = 220
USER_ID_MAX = 419
# ---------------------------------

print(f"--- Iniciando script: Creando {NUMERO_DE_TRANSACCIONES} transacciones ---")
print(f"Endpoint: {API_URL}")
print(f"IDs de usuario se generarán aleatoriamente entre {USER_ID_MIN} y {USER_ID_MAX}.")

exitosos = 0
fallidos = 0

# Inicia el bucle para 5000 llamadas
for i in range(NUMERO_DE_TRANSACCIONES):
    
    # 1. Crear el payload (el JSON) con datos aleatorios
    payload = {
        # Floats
        "distance_from_home": random.uniform(0.5, 60.0) if random.random() > 0.05 else random.uniform(60.0, 800.0),
        "distance_from_last_transaction": random.uniform(0.1, 10.0) if random.random() > 0.05 else random.uniform(10.0, 60.0),
        "ratio_to_median_purchase_price": random.uniform(0.1, 3.0) if random.random() > 0.05 else random.uniform(3.0, 7.0),
        
        # Booleans
        "repeat_retailer": random.choice([True, False]),
        "used_chip": random.choice([True, False]),
        "used_pin_number": random.choice([True, False]),
        "online_order": random.choice([True, False]),
        "fraud": True if random.random() < 0.40 else False, # ~7% de fraude
        
        # Foreign Key (como pediste, entre 220 y 419)
        "user": random.randint(USER_ID_MIN, USER_ID_MAX)
    }

    try:
        # 2. Enviar la petición POST a tu API
        response = requests.post(API_URL, json=payload)

        # 3. Revisar la respuesta
        if response.status_code == 201:  # 201 = Creado
            exitosos += 1
            # Usamos end='\r' para que se actualice en la misma línea y no llene la consola
            print(f"Progreso: {i+1}/{NUMERO_DE_TRANSACCIONES} (Éxitos: {exitosos} | Fallos: {fallidos})", end='\r')
        else:
            fallidos += 1
            print(f"\n--- ! Error en la petición {i+1} ! ---")
            print(f"Status Code: {response.status_code}")
            print(f"Respuesta: {response.text}")
            # Pausamos si hay un error para poder leerlo
            time.sleep(1)

    except requests.exceptions.ConnectionError as e:
        print(f"\n--- !! ERROR DE CONEXIÓN !! ---")
        print("No se pudo conectar a la API. ¿Está el servidor de Django corriendo?")
        print(f"Error: {e}")
        print("--- SCRIPT DETENIDO ---")
        break # Detiene el script si no puede conectar
    except Exception as e:
        print(f"\nOcurrió un error inesperado: {e}")
        fallidos += 1

# 4. Mostrar resumen final
print("\n" + "---" * 10)
print("¡Script finalizado!")
print(f"  Transacciones creadas exitosamente: {exitosos}")
print(f"  Peticiones fallidas: {fallidos}")
print("---" * 10)