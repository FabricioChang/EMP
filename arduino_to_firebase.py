import serial
import firebase_admin
from firebase_admin import credentials, db

# === CONFIGURA ESTOS DATOS ===
SERIAL_PORT = "/dev/ttyACM0"   # Ajusta a tu puerto real
BAUD_RATE = 9600
FIREBASE_CRED = "/home/fabricio/Documents/Emprendimiento/EMP/clave_firebase.json"
DB_URL = "https://gestion-inventario-emp-default-rtdb.firebaseio.com/"

# Inicializar Firebase
cred = credentials.Certificate(FIREBASE_CRED)
firebase_admin.initialize_app(cred, {
    'databaseURL': DB_URL
})

# Referencias a producto1 y producto2
ref_producto1 = db.reference("/presentacion/inventario/producto1/stock")
ref_producto2 = db.reference("/presentacion/inventario/producto2/stock")

# Conectar Arduino
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
print("Escuchando datos del Arduino...")

while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea.startswith("PESO1:"):
            valor = float(linea.split(":")[1])
            print(f"Celda 1 -> {valor} g")
            ref_producto1.set(valor)
        elif linea.startswith("PESO2:"):
            valor = float(linea.split(":")[1])
            print(f"Celda 2 -> {valor} g")
            ref_producto2.set(valor)
    except Exception as e:
        print(f"Error: {e}")
