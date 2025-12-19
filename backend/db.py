import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    MONGO_URI,
    tls=True,  # asegura TLS 1.2+
    serverSelectionTimeoutMS=5000  # tiempo máximo de espera para conectar
)

db = client["secure_chat"]
mensajes_col = db["mensajes"]

# Probar conexión al iniciar
try:
    client.admin.command("ping")
    print("Conexión a MongoDB Atlas OK")
except Exception as e:
    print("Error conectando a MongoDB Atlas:", e)
