from typing import Protocol
from servicios.persistencia.contratos.personas import PersonasProtocol
from servicios.persistencia.contratos.personal import PersonalProtocol
from servicios.persistencia.contratos.citas import CitasProtocol
from servicios.persistencia.contratos.atenciones import AtencionesProtocol
from servicios.persistencia.contratos.medicamentos import MedicamentosProtocol
from servicios.persistencia.contratos.ciclo import CicloVidaProtocol

class RepositorioSaludProtocol(PersonasProtocol, PersonalProtocol, CitasProtocol, AtencionesProtocol, MedicamentosProtocol, CicloVidaProtocol, Protocol):
    """Contrato compuesto por operaciones específicas de cada dominio."""

__all__ = ["RepositorioSaludProtocol"]
