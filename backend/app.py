from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
from diffprivlib.mechanisms import Laplace
from dotenv import load_dotenv
import random, time, os
from db import mensajes_col

load_dotenv()  # CARGA .env

app = Flask(__name__)

# ⚡ Configuración CORS para tu frontend en Vercel
CORS(app, resources={r"/*": {"origins": "https://silent-drop-b6m6pt7qm-arielangulos-projects.vercel.app"}}, supports_credentials=True, methods=["GET","POST","DELETE","OPTIONS"])

# 🔐 Llave desde ENV
key = os.getenv("FERNET_KEY")
if not key:
    raise ValueError("FERNET_KEY no definido en las variables de entorno")
cipher = Fernet(key.encode())

EPSILON = float(os.getenv("EPSILON", 1.0))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))

batch_mensajes = []

def procesar_mensaje(mensaje):
    mensaje_cifrado = cipher.encrypt(mensaje.encode())
    batch_mensajes.append(mensaje_cifrado)

    mensajes_guardados = []

    if len(batch_mensajes) >= BATCH_SIZE:
        random.shuffle(batch_mensajes)
        lap = Laplace(epsilon=EPSILON, sensitivity=3600)

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

#  Rutas
@app.route("/mensajes", methods=["POST"])
def recibir_mensaje():
    try:
        data = request.get_json(silent=True) or {}
        mensaje = data.get("mensaje")
        if not mensaje:
            return jsonify({"error": "Mensaje vacío"}), 400

        guardados = procesar_mensaje(mensaje)

        return jsonify({
            "status": "Mensaje recibido",
            "procesados": len(guardados),
            "pendientes": len(batch_mensajes)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mensajes/procesados", methods=["GET"])
def obtener_mensajes():
    try:
        datos = []
        for doc in mensajes_col.find({}, {"_id": 0}):
            datos.append(doc)
        return jsonify(datos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/mensajes/eliminar", methods=["DELETE", "OPTIONS"])
def eliminar_mensajes():
    if request.method == "OPTIONS":
       
        return '', 200
    try:
        mensajes_col.delete_many({})
        batch_mensajes.clear()
        return jsonify({"status": "Mensajes eliminados"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Manejo de rutas no encontradas
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

if __name__ == "__main__":
    # ⚡ Para Render usa host='0.0.0.0' y puerto por defecto de Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
