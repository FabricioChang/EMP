import serial
import firebase_admin
from firebase_admin import credentials, db

# === CONFIGURA ESTO ===
SERIAL_PORT = "COM6"  # Cambia según el puerto de tu Arduino en Linux
BAUD_RATE = 9600
FIREBASE_CRED = "ruta/tu_clave_firebase.json"  # Ruta a tu archivo JSON de clave privada
DB_URL = "https://gestion-inventario-emp-default-rtdb.firebaseio.com/"

# Inicializar Firebase
cred = credentials.Certificate(FIREBASE_CRED)
firebase_admin.initialize_app(cred, {
    'databaseURL': DB_URL
})

# Referencia directa al stock del producto1
ref_stock = db.reference("/presentacion/inventario/producto1/stock")

# Conexión con Arduino
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
print("Escuchando datos del Arduino...")

while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea.startswith("PESO:"):
            valor = float(linea.split(":")[1])
            print(f"Peso leído: {valor} g")

            # Enviar el valor a Firebase
            ref_stock.set(valor)
            print("Dato enviado a Firebase -> presentacion/producto1/inventario/stock")
    except Exception as e:
        print(f"Error: {e}")
