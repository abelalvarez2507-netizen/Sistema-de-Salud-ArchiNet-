def texto_requerido(valor, campo, maximo=200):
    """Normaliza un texto obligatorio y limita su longitud."""
    if valor is None:
        raise ValueError(f"{campo} es obligatorio.")

    texto = str(valor).strip()

    if not texto:
        raise ValueError(f"{campo} no puede estar vacío.")

    if len(texto) > maximo:
        raise ValueError(
            f"{campo} no puede superar los {maximo} caracteres."
        )

    return texto


def validar_nombre(valor):
    """Valida nombres formados únicamente por letras y espacios."""
    nombre = unicodedata.normalize(
        "NFC",
        texto_requerido(valor, "El nombre", 100),
    )

    if not all(caracter.isalpha() or caracter == " " for caracter in nombre):
        raise ValueError(
            "El nombre solo puede contener letras, tildes, ñ y espacios."
        )

    return nombre


def validar_nombre_en_edicion(valor):
    """Permite escribir nombres con letras, espacios y tildes en curso."""
    if len(valor) > 100:
        return False

    marcas_tilde = {"\u0300", "\u0301", "\u0303", "\u0308"}
    anterior_es_letra = False

    for caracter in valor:
        if caracter.isalpha():
            anterior_es_letra = True
        elif caracter == " ":
            anterior_es_letra = False
        elif caracter in marcas_tilde and anterior_es_letra:
            continue
        else:
            return False

    return True


def validar_dni_en_edicion(valor):
    """Limita la escritura del DNI a ocho dígitos ASCII como máximo."""
    return valor == "" or (
        len(valor) <= 8
        and all("0" <= caracter <= "9" for caracter in valor)
    )


def validar_edad(valor):
    """Valida la edad en el rango razonable del dominio."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError("La edad debe ser un número entero.")

    if valor < 0 or valor > 120:
        raise ValueError("La edad debe estar entre 0 y 120 años.")

    return valor


def validar_dni(valor):
    """Valida un DNI de exactamente ocho dígitos."""
    if valor is None:
        raise ValueError("El DNI es obligatorio.")

    dni = str(valor).strip()

    if not dni.isascii() or not dni.isdigit():
        raise ValueError("El DNI debe contener únicamente números.")

    if len(dni) != 8:
        raise ValueError("El DNI debe contener exactamente 8 dígitos.")

    return dni

