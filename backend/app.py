from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
from diffprivlib.mechanisms import Laplace
import random, time, sqlite3, os

app = Flask(__name__)
CORS(app)

# Llave para cifrado
key = Fernet.generate_key()
cipher = Fernet(key)

# Parámetros configurables
EPSILON = float(os.getenv("EPSILON", 1.0))  # ε diferencial configurable por variable de entorno
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))  # Tamaño de batch para mixnet

# Almacenamiento temporal
batch_mensajes = []

# Inicializar SQLite para persistencia simple
conn = sqlite3.connect("mensajes.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mensaje TEXT,
    timestamp REAL
)
""")
conn.commit()

def procesar_mensaje(mensaje):
    """Cifra y añade ruido diferencial al mensaje, luego lo mezcla."""
    # Cifrar mensaje
    mensaje_cifrado = cipher.encrypt(mensaje.encode())

    # Añadir a batch
    batch_mensajes.append(mensaje_cifrado)

    # Si batch está lleno, mezclar y almacenar
    mensajes_a_guardar = []
    if len(batch_mensajes) >= BATCH_SIZE:
        random.shuffle(batch_mensajes)  # Mixnet
        lap = Laplace(epsilon=EPSILON, sensitivity=1.0)
        for m in batch_mensajes:
            tiempo_ruidoso = lap.randomise(time.time())
            mensajes_a_guardar.append((m.decode(), tiempo_ruidoso))
            c.execute("INSERT INTO mensajes (mensaje, timestamp) VALUES (?, ?)", (m.decode(), tiempo_ruidoso))
        conn.commit()
        batch_mensajes.clear()
    
    return mensajes_a_guardar

@app.route("/mensajes", methods=["POST"])
def recibir_mensaje():
    mensaje = request.json.get("mensaje")
    if not mensaje:
        return jsonify({"status": "Mensaje vacío"}), 400

    mensajes_guardados = procesar_mensaje(mensaje)
    status_msg = "Mensaje recibido"
    if mensajes_guardados:
        status_msg += f" y {len(mensajes_guardados)} mensajes procesados en batch"

    return jsonify({"status": status_msg})

@app.route("/mensajes", methods=["GET"])
def obtener_mensajes():
    c.execute("SELECT mensaje, timestamp FROM mensajes ORDER BY id ASC")
    datos = [{"mensaje": row[0], "timestamp": row[1]} for row in c.fetchall()]
    return jsonify(datos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)