def validar_codigo(valor, campo="El código"):
    """Valida códigos internos sin limitar la cantidad de dígitos."""
    if valor is None:
        raise ValueError(f"{campo} es obligatorio.")
    codigo = str(valor).strip()
    if not codigo:
        raise ValueError(f"{campo} no puede estar vacío.")
    if not PATRON_CODIGO.fullmatch(codigo):
        raise ValueError(
            f"{campo} debe contener al menos 2 caracteres alfanuméricos, guion o guion bajo."
        )
    return codigo


def validar_especialidad(valor):
    return texto_requerido(valor, "La especialidad", 100)


def validar_motivo(valor):
    return texto_requerido(valor, "El motivo de la cita", 200)

