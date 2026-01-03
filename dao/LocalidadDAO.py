from .BaseDAO import BaseDAO
from modelo import Localidad, Municipio
from sqlalchemy import select
from typing import List

class LocalidadDAO(BaseDAO):
    """
    DAO específico para la entidad Localidad
    """
    
    def obtener_por_municipio(self, id_municipio: int) -> List[Localidad]:
        """
        Obtiene todas las localidades que pertenecen a un municipio especifico
        """

        try:
            with self._get_session() as session:
                statement = select(Localidad).where(Localidad.municipio_id == id_municipio)
                return session.scalars(statement).all()
        except Exception as e:
            print(f"Error al obtener localidades para municipio {id_municipio}: {e}")
            return []