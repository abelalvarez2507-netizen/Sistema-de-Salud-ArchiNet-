from servicios.persistencia.esquema.tablas import TablasRepositorioMixin
from servicios.persistencia.esquema.migraciones import MigracionesRepositorioMixin

class RepositorioEsquemaMixin(TablasRepositorioMixin, MigracionesRepositorioMixin):
    """Combina creación y migración del esquema SQLite."""

__all__ = ["RepositorioEsquemaMixin"]
