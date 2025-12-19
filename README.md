# SILENTDROP — Plataforma de mensajería segura y anónima

SILENTDROP es una plataforma web que protege el contenido y los metadatos de los mensajes mediante cifrado, mezcla de mensajes y privacidad diferencial. El backend corre en Flask, la base de datos es MongoDB y el frontend es un React simple para pruebas/demo.

## 📌 Características
- Mensajes cifrados con **Fernet**.
- Mezcla de mensajes para anonimato (**Mixnet**).
- Ruido en timestamps usando **Privacidad Diferencial**.
- Backend desacoplado de frontend (API REST).
- Base de datos MongoDB.
- Frontend simple en React para pruebas/demo.

## 🛠️ Tecnologías
- **Backend:** Python + Flask + Flask-CORS
- **Base de datos:** MongoDB
- **Frontend:** React
- **Cifrado:** Cryptography (Fernet)
- **Privacidad diferencial:** diffprivlib

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio
```bash

git clone <url-del-repo>
cd buzon-anonimo/backend

```

## CREAR ENTORNO VIRTUAL (Python)
```bash 

 python -m venv venv
 .\venv\Scripts\Activate.ps1

```
## Instalar dependencias 

```bash 

pip install -r requirements.txt

```

## Copiar el archivo .env de ejemplo y generar la llave 

```bash 

copy .env.example .env

python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" 

```
## Levantar el Back-End 

```bash 


python app.py

```



