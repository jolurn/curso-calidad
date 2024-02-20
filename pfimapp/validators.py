from django.core.exceptions import ValidationError
from functools import wraps
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

def validate_min_length_and_letters(min_length):
    @wraps(validate_min_length_and_letters)
    def validator(value):
        if len(value) < min_length:
            raise ValidationError(f"Este campo debe tener al menos {min_length} caracteres.")
        if not value.isalpha():
            raise ValidationError('Este campo debe contener solo letras.')
    return validator
    
def validate_numeric_length(length):
    @wraps(validate_numeric_length)
    def validator(value):
        str_value = str(value)  # Convertir el valor a una cadena para obtener su longitud
        if not str_value.isdigit():
            raise ValidationError("Este campo debe contener solo dígitos numéricos.")
        if len(str_value) != length:
            raise ValidationError(f"Este campo debe tener exactamente {length} dígitos.")
    return validator

def validate_min_numeric_length(min_length):
    @wraps(validate_min_numeric_length)
    def validator(value):
        str_value = str(value)  # Convertir el valor a una cadena para facilitar la validación
        numeric_chars = sum(c.isdigit() for c in str_value)  # Contar los caracteres numéricos
        if numeric_chars < min_length:
            raise ValidationError(f"Este campo debe contener al menos {min_length} caracteres numéricos.")
    return validator
        
def validate_password(value):
    if len(value) < 3:
        raise ValidationError("La contraseña debe tener al menos 3 caracteres alfanuméricos.")

def validate_min_length_correo(min_length):
    @wraps(validate_min_length_correo)
    def validator(value):
        if len(value) < min_length:
            raise ValidationError(f"Este campo debe tener al menos {min_length} caracteres.")
        return  # Retorna aquí si la longitud es válida
    return validator

def validate_past_date(value):
    # Calcula la fecha hace 26 años a partir de la fecha actual
    min_birth_date = timezone.now().date() - timedelta(days=(22 * 365))

    if value > timezone.now().date():
        raise ValidationError('La fecha de nacimiento no puede estar en el futuro.')
    elif value > min_birth_date:
        raise ValidationError('La edad mínima permitida es de 22 años.')
    
