from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
from diffprivlib.mechanisms import Laplace
from dotenv import load_dotenv
import random, time, os
from db import mensajes_col

load_dotenv()

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:5173", "https://buzon-anonimo.vercel.app"]}},
    supports_credentials=True,
    methods=["GET", "POST", "DELETE", "OPTIONS"]
)


# 🔐 Configuración de seguridad
key = os.getenv("FERNET_KEY")
if not key:
    raise ValueError("FERNET_KEY no definido en las variables de entorno")
cipher = Fernet(key.encode())


EPSILON = 1  
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 5))
SENSITIVITY = 3600  # 1 hora en segundos

# Validación de seguridad
if EPSILON > 10:
    print("⚠️  WARNING: Epsilon muy alto, privacidad comprometida")
    EPSILON = 0.1  # Forzar valor seguro

# 📊 Cálculo de escala del ruido (para debugging)
NOISE_SCALE = SENSITIVITY / EPSILON
print(f"🔐 Configuración de Privacidad Diferencial:")
print(f"   ε (epsilon): {EPSILON}")
print(f"   Sensibilidad: {SENSITIVITY}s ({SENSITIVITY/3600:.1f}h)")
print(f"   Escala de ruido: {NOISE_SCALE:.2f}s ({NOISE_SCALE/3600:.2f}h)")
print(f"   Tamaño del batch: {BATCH_SIZE}")

# Almacén temporal del batch con timestamps reales
batch_mensajes = []

def procesar_mensaje(mensaje):
    """Procesa y cifra mensajes con privacidad diferencial"""
    mensaje_cifrado = cipher.encrypt(mensaje.encode())
    timestamp_real = time.time()
    
    # Guarda el mensaje con su timestamp real
    batch_mensajes.append({
        'mensaje': mensaje_cifrado,
        'timestamp': timestamp_real
    })

    mensajes_guardados = []

    if len(batch_mensajes) >= BATCH_SIZE:
        print(f"\n Procesando batch de {len(batch_mensajes)} mensajes...")
        
        # Mezcla aleatoria (mixnet)
        random.shuffle(batch_mensajes)
        
        # Generador de ruido Laplaciano
        lap = Laplace(epsilon=EPSILON, sensitivity=SENSITIVITY)
        
        print("📝 Aplicando ruido diferencial a cada mensaje:")
        
        for i, item in enumerate(batch_mensajes, 1):
          
            tiempo_ruidoso = lap.randomise(item['timestamp'])
            diferencia = tiempo_ruidoso - item['timestamp']
            
            print(f"   Msg {i}: {tiempo_ruidoso:.2f} (Δ = {diferencia:+.1f}s / {diferencia/3600:+.2f}h)")
            
            doc = {
                "mensaje": item['mensaje'].decode(),
                "timestamp": tiempo_ruidoso
            }
            mensajes_col.insert_one(doc)
            mensajes_guardados.append(doc)

        batch_mensajes.clear()
        print(f"✅ Batch completado y almacenado\n")

    return mensajes_guardados

#  Rutas de la API
@app.route("/mensajes", methods=["POST"])
def recibir_mensaje():
    """Recibe y procesa mensajes cifrados"""
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
        print(f" Error al recibir mensaje: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/mensajes/procesados", methods=["GET"])
def obtener_mensajes():
    """Obtiene todos los mensajes procesados"""
    try:
        datos = list(mensajes_col.find({}, {"_id": 0}).sort("timestamp", -1))
        return jsonify(datos)
    except Exception as e:
        print(f" Error al obtener mensajes: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/mensajes/eliminar", methods=["DELETE", "OPTIONS"])
def eliminar_mensajes():
    """Elimina todos los mensajes"""
    if request.method == "OPTIONS":
        return '', 200
    try:
        resultado = mensajes_col.delete_many({})
        batch_mensajes.clear()
        print(f"  {resultado.deleted_count} mensajes eliminados")
        return jsonify({
            "status": "Mensajes eliminados",
            "count": resultado.deleted_count
        })
    except Exception as e:
        print(f" Error al eliminar mensajes: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/stats", methods=["GET"])
def obtener_estadisticas():
    """Obtiene estadísticas del sistema"""
    try:
        total_mensajes = mensajes_col.count_documents({})
        return jsonify({
            "total_mensajes": total_mensajes,
            "batch_pendiente": len(batch_mensajes),
            "epsilon": EPSILON,
            "batch_size": BATCH_SIZE,
            "noise_scale": NOISE_SCALE
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)