from django.core.exceptions import ValidationError

TAMANO_MAXIMO_IMAGEN_MB = 5


def validar_tamano_imagen(archivo):
    """Rechaza imágenes que superan el tamaño máximo permitido."""
    if archivo.size > TAMANO_MAXIMO_IMAGEN_MB * 1024 * 1024:
        raise ValidationError(f"La imagen no puede superar los {TAMANO_MAXIMO_IMAGEN_MB} MB.")
