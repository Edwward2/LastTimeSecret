import time, secrets, base64
from fastapi import FastAPI, HTTPException
from app.models import CreateSecretIn, SecretOut, RevealOut
from app.security import generate_aes_key, encrypt_secret, decrypt_secret
from app.storage import save_secret, get_secret, delete_secret

# Inicializa la aplicación FastAPI con un título descriptivo
app = FastAPI(title="LastSecret")


# --------------------------
# Crear un secreto (POST /api/secrets)
# --------------------------
@app.post("/api/secrets", response_model=SecretOut)
def create_secret(inp: CreateSecretIn):
   

    # Genera un ID único (seguro para URL)
    sid = secrets.token_urlsafe(16)

    # Genera una clave AES de 256 bits
    aes_key = generate_aes_key()

    # Cifra el secreto con la clave AES y genera un nonce (vector de inicialización)
    ciphertext, nonce = encrypt_secret(aes_key, inp.secret)

    # Prepara el payload para guardar en Redis (todo en Base64 para ser JSON-safe)
    payload = {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "aes_key": base64.b64encode(aes_key).decode(),
        "created_at": str(int(time.time()))
    }

    # Guarda en Redis con el TTL definido por el usuario
    save_secret(sid, payload, inp.ttl_seconds)

    # Retorna solo el ID y la URL para recuperar el secreto
    return SecretOut(id=sid, url=f"/s/{sid}")


# --------------------------
# Revelar un secreto (POST /api/secrets/{sid}/reveal)
# --------------------------
@app.post("/api/secrets/{sid}/reveal", response_model=RevealOut)
def reveal_secret(sid: str):
    """
    Revela un secreto previamente almacenado y lo elimina después de su lectura.
    
    - Busca el secreto en Redis por ID.
    - Si no existe o expiró, devuelve error 404.
    - Descifra el contenido usando AES-GCM.
    - Si ocurre un error de descifrado, elimina el secreto y devuelve error 500.
    - Después de revelar el secreto exitosamente, lo elimina ("burn after read").
    """

    # Obtiene el secreto desde Redis
    data = get_secret(sid)
    if not data:
        raise HTTPException(status_code=404, detail="Not found or expired")

    # Decodifica los datos Base64 (clave, nonce, texto cifrado)
    aes_key = base64.b64decode(data["aes_key"])
    nonce = base64.b64decode(data["nonce"])
    ciphertext = base64.b64decode(data["ciphertext"])

    try:
        # Intenta descifrar el secreto
        secret_plain = decrypt_secret(aes_key, ciphertext, nonce)
    except Exception:
        # Si falla, elimina el secreto (seguridad) y devuelve error
        delete_secret(sid)
        raise HTTPException(status_code=500, detail="Decryption failed")

    # "Burn after read": elimina el secreto inmediatamente después de revelarlo
    delete_secret(sid)

    # Devuelve el secreto en texto plano
    return RevealOut(secret=secret_plain)
