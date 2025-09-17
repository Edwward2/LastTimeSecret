import os, json
import redis

# URL de conexión a Redis (puede configurarse con variable de entorno)
# Formato: redis://[usuario:password]@host:puerto/db
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Conexión a Redis. 
# decode_responses=False → los valores se manejan como bytes, no como strings.
r = redis.Redis.from_url(REDIS_URL, decode_responses=False)


def save_secret(sid: str, payload: dict, ttl_seconds: int):
    """
    Guarda un secreto en Redis con expiración automática (TTL).

    Parámetros:
        sid (str): ID único del secreto.
        payload (dict): Datos asociados al secreto (JSON serializado).
        ttl_seconds (int): Tiempo de vida en segundos antes de que expire.
    """
    key = f"secret:{sid}"
    r.setex(key, ttl_seconds, json.dumps(payload).encode())


def get_secret(sid: str) -> dict | None:
    """
    Recupera un secreto desde Redis.

    Parámetros:
        sid (str): ID único del secreto.

    Retorna:
        dict: Si existe y no expiró.
        None: Si no existe o ya expiró.
    """
    key = f"secret:{sid}"
    raw = r.get(key)
    if not raw:
        return None
    return json.loads(raw.decode())


def delete_secret(sid: str):
    """
    Elimina un secreto de Redis de forma manual (antes de que expire).

    Parámetros:
        sid (str): ID único del secreto.
    """
    key = f"secret:{sid}"
    r.delete(key)
