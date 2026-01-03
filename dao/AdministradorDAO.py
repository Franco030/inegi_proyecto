from .BaseDAO import BaseDAO
from modelo import Administrador
from sqlalchemy import select
from typing import Optional

class AdministradorDAO(BaseDAO):
    """
    DAO especifico para la entidad Administrador
    """

    def verificar_credenciales(self, usuario: str, contrasena_hash: str) -> Optional[Administrador]:
        """
        Busca un administrador por usuario y verifica el hash de la contraseña
        """
        try:
            with self._get_session() as session:
                statement = select(Administrador).where(Administrador.usuario == usuario)
                administrador = session.scalar(statement)

                if administrador and administrador.contrasena_hash == contrasena_hash:
                    return administrador
                return None
        except Exception as e:
            print(f"Error en la verificacion de credenciales: {e}")
            return None