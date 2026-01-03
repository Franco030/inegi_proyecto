from .BaseDAO import BaseDAO
from modelo import Municipio

class MunicipioDAO(BaseDAO):
    """
    DAO especifico para la entidad municipio
    """
    # Hereda guardar(), obtener_por_id(), y listar_todos() del BaseDAO
    # No necesita metodo adicionales si solo se usa el CRUD basico
    pass