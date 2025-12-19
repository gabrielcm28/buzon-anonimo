from pymongo import MongoClient
import certifi

# La misma URI que usaste en Compass
MONGO_URI = "mongodb+srv://gabrielcalderon:pxElEsBqWEqhSEdD@cluster1.r2eyaul.mongodb.net/secure_chat"

try:
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    
    # Probar conexión
    client.admin.command('ping')
    print("✓ Conexión exitosa a MongoDB")
    
    # Listar bases de datos
    print("\nBases de datos disponibles:")
    for db_name in client.list_database_names():
        print(f"  - {db_name}")
    
    # Insertar en una nueva base de datos
    db = client.buzon_anonimo  # o el nombre que quieras
    collection = db.mensajes
    result = collection.insert_one({
        "mensaje": "Hola mundo desde Python",
        "fecha": "2024-12-19"
    })
    print(f"\n✓ Documento insertado con ID: {result.inserted_id}")
    
except Exception as e:
    print(f"✗ Error: {e}")
finally:
    client.close()

