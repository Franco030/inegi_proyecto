from sqlalchemy.orm import sessionmaker, Session, joinedload, selectinload
from sqlalchemy.exc import SQLAlchemyError
from typing import TypeVar, Type, List, Optional, Any
from sqlalchemy import select
from contextlib import contextmanager
from constants import ENGINE

T = TypeVar('T') # Tipo genérico

class BaseDAO:
    """
    Clase base que implementa el CRUD generico y soporta estrategias de carga para Eager Loading
    """

    def __init__(self, engine):
        """
        Inicializa el SessionLocal (SessionMaker)
        """
        self.SessionLocal = sessionmaker(bind=ENGINE, expire_on_commit=False)

    @contextmanager
    def _get_session(self) -> Session:
        """
        Manejador de contexto para la sesion.
        Garantiza que la sesion cierre y se haga rollback/commit
        """
        session = self.SessionLocal()

        try:
            yield session
            # Si no hay errores, se hace commit al salir del 'with'
            session.commit()
        except SQLAlchemyError as e:
            # Si har errores se hace rollback
            session.rollback()
            raise e
        finally:
            # Siempre se cierra la sesion
            session.close()

    def guardar(self, entidad: T) -> Optional[T]:
        """
        Guarda (INSERT) o actualiza (UPDATE) una entidad
        """
        try:
            with self._get_session() as session:
                session.add(entidad)
                # session.refresh(entidad)
                return entidad
        except SQLAlchemyError:
            return None
        
    def obtener_por_id(self, modelo: Type[T], id_entidad: int, options: List[Any]=None) -> Optional[T]:
        """
        Obtiene una entidad por su clave primaria

        Args:
            options: Lista de estrategias de carga (ej. [joinedload(Vivienda.habitantes)])
        """

        try:
            with self._get_session() as session:
                statement = select(modelo).where(modelo.id == id_entidad)

                if options:
                    statement = statement.options(*options)

                entidad = session.scalar(statement)
                return entidad
        except SQLAlchemyError as e:
            print(f"Error al buscar {modelo.__name__} por ID: {e}")
            return None
        
    def listar_todos(self, modelo: Type[T], options: List[Any]=None) -> List[T]:
        """
        Obtiene todas las entidades de un tipo con posibles estrategias con Eager Loading

        Args:
            options: Lista de estrategias de carga (ej. [selectinload(Municipio.localidades)])
        """
        try:
            with self._get_session() as session:
                statement = select(modelo)

                if options:
                    statement = statement.options(*options)

                return session.scalars(statement).all()
        except SQLAlchemyError as e:
            print(f"Error al listar todos los {modelo.__name__}: {e}")
            return []
        
    def eliminar(self, modelo: Type[T], id_entidad: int) -> bool:
        """
        Elimina una entidad por su ID.
        Retorna True si fue exitoso, False si no.
        """
        try:
            with self._get_session() as session:
                # Primero, obtenemos la entidad para asegurar que existe
                entidad = session.get(modelo, id_entidad)
                if entidad:
                    session.delete(entidad)
                    return True
                return False # No se encontró la entidad
        except SQLAlchemyError as e:
            print(f"Error al eliminar {modelo.__name__} ID {id_entidad}: {e}")
            return False