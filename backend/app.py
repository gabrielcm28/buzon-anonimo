from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
from diffprivlib.mechanisms import Laplace
from dotenv import load_dotenv
import random, time, os

from db import mensajes_col

load_dotenv()  # CARGA .env

app = Flask(__name__)
CORS(app)

# 🔐 Llave desde ENV
key = os.getenv("FERNET_KEY").encode()
cipher = Fernet(key)

EPSILON = float(os.getenv("EPSILON", 1.0))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))

batch_mensajes = []

def procesar_mensaje(mensaje):
    mensaje_cifrado = cipher.encrypt(mensaje.encode())
    batch_mensajes.append(mensaje_cifrado)

    mensajes_guardados = []

    if len(batch_mensajes) >= BATCH_SIZE:
        random.shuffle(batch_mensajes)
        lap = Laplace(epsilon=EPSILON, sensitivity=1.0)

        for m in batch_mensajes:
            tiempo_ruidoso = lap.randomise(time.time())
            doc = {
                "mensaje": m.decode(),
                "timestamp": tiempo_ruidoso
            }
            mensajes_col.insert_one(doc)
            mensajes_guardados.append(doc)

        batch_mensajes.clear()

    return mensajes_guardados

@app.route("/mensajes", methods=["POST"])
def recibir_mensaje():
    mensaje = request.json.get("mensaje")
    if not mensaje:
        return jsonify({"error": "Mensaje vacío"}), 400

    guardados = procesar_mensaje(mensaje)

    return jsonify({
        "status": "Mensaje recibido",
        "procesados": len(guardados)
    })

@app.route("/mensajes/procesados", methods=["GET"])
def obtener_mensajes():
    datos = []
    for doc in mensajes_col.find({}, {"_id": 0}):
        datos.append(doc)
    return jsonify(datos)

if __name__ == "__main__":
    app.run(debug=True)
