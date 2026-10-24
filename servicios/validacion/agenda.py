def normalizar_fecha(valor):
    """Acepta DD/MM/AAAA o AAAA-MM-DD y devuelve DD/MM/AAAA."""
    fecha = texto_requerido(valor, "La fecha de la cita", 10)

    formatos = ("%d/%m/%Y", "%Y-%m-%d")
    for formato in formatos:
        try:
            fecha_objeto = datetime.strptime(fecha, formato)
            return fecha_objeto.strftime("%d/%m/%Y")
        except ValueError:
            continue

    raise ValueError(
        "La fecha debe tener el formato DD/MM/AAAA. Ejemplo: 15/09/2026."
    )


def normalizar_hora(valor):
    """Valida y normaliza una hora en formato de 24 horas HH:MM."""
    hora = texto_requerido(valor, "La hora de la cita", 5)
    try:
        hora_objeto = datetime.strptime(hora, "%H:%M")
    except ValueError as error:
        raise ValueError(
            "La hora debe tener el formato HH:MM, por ejemplo 09:30."
        ) from error
    return hora_objeto.strftime("%H:%M")

