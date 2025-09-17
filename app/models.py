# Importamos utilidades de Pydantic
from pydantic import BaseModel, Field, constr

# ======================================================
# Modelo de entrada (cuando el usuario crea un secreto)
# ======================================================
class CreateSecretIn(BaseModel):
    # Texto del secreto que será almacenado.
    # Restricciones:
    #   - mínimo 1 caracter
    #   - máximo 20.000 caracteres
    secret: constr(
        min_length=1,
        max_length=20000
    ) = Field(
        ...,
        description="Texto secreto que se desea almacenar (mínimo 1 caracter, máximo 20.000).",
        example="Mi contraseña súper secreta"
    )

    # Tiempo de vida del secreto (TTL: Time To Live), en segundos.
    # Valor por defecto: 3600 (1 hora).
    # Restricciones:
    #   - ge=60  → mínimo 60 segundos (1 minuto)
    #   - le=60*60*24*7 → máximo 604800 segundos (7 días)
    ttl_seconds: int = Field(
        3600,
        ge=60,
        le=60*60*24*7,
        description="Tiempo de vida del secreto en segundos (mínimo 60, máximo 604800).",
        example=600  # 10 minutos
    )

# ======================================================
# Modelo de salida (cuando se crea un secreto)
# ======================================================
class SecretOut(BaseModel):
    # ID único del secreto (ejemplo: UUID o hash).
    id: str = Field(
        ...,
        description="Identificador único del secreto (UUID o hash generado).",
        example="b1946ac92492d2347c6235b4d2611184"
    )

    # URL completa para acceder al secreto.
    url: str = Field(
        ...,
        description="URL generada para poder acceder y revelar el secreto.",
        example="https://midominio.com/reveal/b1946ac92492d2347c6235b4d2611184"
    )

    # Tiempo de vida del secreto en segundos (opcional, pero útil para el cliente).
    ttl_seconds: int = Field(
        ...,
        description="Tiempo de vida del secreto en segundos.",
        example=600
    )

    # Si se requiere o no passphrase adicional (opcional).
    use_passphrase: bool = Field(
        False,
        description="Indica si el secreto requiere una passphrase para revelarse.",
        example=False
    )

# ======================================================
# Modelo de salida (cuando se revela un secreto)
# ======================================================
class RevealOut(BaseModel):
    # Contenido del secreto en texto plano (ya desencriptado).
    secret: str = Field(
        ...,
        description="El contenido del secreto en texto plano (desencriptado).",
        example="Mi contraseña súper secreta"
    )

# ======================================================
# Modelo opcional para errores
# ======================================================
class ErrorOut(BaseModel):
    detail: str = Field(
        ...,
        description="Mensaje de error explicativo.",
        example="El secreto ya fue revelado o no existe."
    )
