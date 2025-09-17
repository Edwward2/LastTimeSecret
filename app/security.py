import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ======================================================
# Generación de clave AES
# ======================================================
def generate_aes_key() -> bytes:
    """
    Genera una clave AES de 256 bits (32 bytes).
    Se utiliza para encriptar y desencriptar secretos.

    Returns:
        bytes: Clave AES generada aleatoriamente.
    """
    return os.urandom(32)  # AES-256


# ======================================================
# Encriptar secreto con AES-GCM
# ======================================================
def encrypt_secret(aes_key: bytes, secret: str) -> tuple[bytes, bytes]:
    """
    Encripta un secreto utilizando AES-GCM (AES en modo Galois/Counter).

    Args:
        aes_key (bytes): Clave AES de 256 bits.
        secret (str): Texto plano del secreto a encriptar.

    Returns:
        tuple[bytes, bytes]: ciphertext (secreto encriptado) y nonce.
    """
    nonce = os.urandom(12)  # 12 bytes recomendado para AES-GCM
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, secret.encode("utf-8"), None)
    return ciphertext, nonce


# ======================================================
# Desencriptar secreto con AES-GCM
# ======================================================
def decrypt_secret(aes_key: bytes, ciphertext: bytes, nonce: bytes) -> str:
    """
    Desencripta un secreto encriptado con AES-GCM.

    Args:
        aes_key (bytes): Clave AES de 256 bits usada en la encriptación.
        ciphertext (bytes): Texto cifrado generado por `encrypt_secret`.
        nonce (bytes): Valor aleatorio generado en la encriptación.

    Returns:
        str: Secreto desencriptado en texto plano.
    """
    aesgcm = AESGCM(aes_key)
    return aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")


# ======================================================
# Helpers opcionales para serializar en Base64
# (útiles si guardas en Redis o JSON)
# ======================================================
def encode_base64(data: bytes) -> str:
    """Convierte bytes a string Base64."""
    return base64.b64encode(data).decode("utf-8")

def decode_base64(data: str) -> bytes:
    """Convierte string Base64 a bytes."""
    return base64.b64decode(data)
