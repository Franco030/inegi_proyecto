from .BaseDAO import BaseDAO
from modelo import Vivienda, Habitante, TipoVivienda, Localidad, Municipio
from sqlalchemy import select, func, join, cast, Integer
from sqlalchemy.orm import selectinload, joinedload
from typing import List, Dict, Any, Optional

class CensoDAO(BaseDAO):
    """
    DAO para todas las entidaded principales (Vivienda, Habitante)
    Contiene metodos de consulta avanzados para reportes y estadisticas
    """

    # --- Metodos generales (Pueden usar los genericos de BaseDAO) ---

    def obtener_vivienda_con_habitantes(self, id_vivienda: int) -> Vivienda | None:
        """
        Obtiene una vivienda y carga eagerly (anticipadamente) sus habitantes
        Cumple:
            "Poder saber quienes y cuantos viven por vivienda
        """

        opciones = [selectinload(Vivienda.habitantes)]
        return self.obtener_por_id(Vivienda, id_vivienda, options=opciones)
    
    # --- Metodos para Reportes y Dashboard ---
    
    def obtener_conteo_poblacion_por_ubicacion(self, 
                                                municipio_id: Optional[int] = None, 
                                                localidad_id: Optional[int] = None
                                                ) -> List[Dict[str, Any]]:
        """
        Calcula el número total de población por Localidad, Municipio.
        Acepta filtros dinámicos.
        """
        try:
            with self._get_session() as session:
                # Base de la consulta
                consulta = select(
                    Municipio.nombre.label('municipio'),
                    Localidad.nombre.label('localidad'),
                    func.count(Habitante.id).label('total_habitantes')
                ).select_from(
                    join(Habitante, Vivienda, Habitante.vivienda_id == Vivienda.id)
                    .join(Localidad, Vivienda.localidad_id == Localidad.id)
                    .join(Municipio, Localidad.municipio_id == Municipio.id)
                )

                # --- AÑADIR FILTROS DINÁMICOS ---
                if localidad_id:
                    consulta = consulta.where(Localidad.id == localidad_id)
                elif municipio_id:
                    consulta = consulta.where(Municipio.id == municipio_id)

                # Agrupación y orden
                consulta = consulta.group_by(
                    Municipio.nombre, Localidad.nombre
                ).order_by(
                    Municipio.nombre, Localidad.nombre
                )
                
                resultados = session.execute(consulta).mappings().all()
                return list(resultados)
        except Exception as e:
            print(f"Error al generar reporte de población: {e}")
            return []
        
    def obtener_conteo_por_tipo_vivienda(self, 
                                         municipio_id: Optional[int] = None, 
                                         localidad_id: Optional[int] = None
                                         ) -> List[Dict[str, Any]]:
        """
        Calcula la cantidad de habitantes que viven en cada tipo de casa.
        Acepta filtros dinámicos.
        """
        try:
            with self._get_session() as session:
                # Base de la consulta
                consulta = select(
                    TipoVivienda.nombre.label('tipo_vivienda'),
                    func.count(Habitante.id).label('habitantes')
                ).select_from(
                    join(Habitante, Vivienda, Habitante.vivienda_id == Vivienda.id)
                    .join(TipoVivienda, Vivienda.tipo_vivienda_id == TipoVivienda.id)
                )

                # --- AÑADIR FILTROS DINÁMICOS ---
                # Necesitamos un JOIN extra si filtramos por ubicación
                if localidad_id or municipio_id:
                    consulta = consulta.join(Localidad, Vivienda.localidad_id == Localidad.id)
                    if localidad_id:
                        consulta = consulta.where(Localidad.id == localidad_id)
                    elif municipio_id:
                        consulta = consulta.where(Localidad.municipio_id == municipio_id)

                # Agrupación y orden
                consulta = consulta.group_by(
                    TipoVivienda.nombre
                ).order_by(
                    TipoVivienda.nombre
                )
                
                return session.execute(consulta).mappings().all()
        except Exception as e:
            print(f"Error al generar reporte por tipo de vivienda: {e}")
            return []
        

    def obtener_actividades_economicas_por_vivienda(self, id_vivienda: int) -> List[str]:
        """
        Obtiene los nombres de las actividades economicas que son el sosten de una vivienda especifica
        Cumple:
            Conocer por vivienda la o las actividades economicas 
        """

        try:
            with self._get_session() as session:
                # Utilizamos la relacion Many-to-Many para obtener las actividades a traves de la tabla de asociacion

                vivienda = session.execute(
                    select(Vivienda)
                    .where(Vivienda.id == id_vivienda)
                    .options(selectinload(Vivienda.actividades))
                ).scalar_one_or_none()

                if vivienda:
                    # Retorna solo los nombres de las actividades
                    return [act.nombre for act in vivienda.actividades]
                return []
        except Exception as e:
            print(f"Error al obtener actividades economicas para vivienda {id_vivienda}: {e}")
            return []
        
    
    def obtener_estimaciones_estadisticas_por_localidad(self) -> List[Dict[str, Any]]:
        """
        Calcula estadisticas clave (poblacion total, promedio de edad y promedio de habitantes por vivienda) por localidad.
        Cumple:
            Reportes, graficos y estimaciones estadisticas por localidades
        """
        try:
            with self._get_session as session:
                consulta = select(
                    Localidad.nombre.label('localidad'),
                    func.count(Habitante.id).label('total_poblacion'),
                    func.avg(Habitante.edad).label('promedio_edad_poblacion'),
                    cast(func.count(Habitante.id), Integer) / func.count(Vivienda.id.distinct()).label('promedio_habitantes_por_vivienda')
                ).select_from(
                    join(Habitante, Vivienda, Habitante.vivienda_id == Vivienda.id)
                    .join(Localidad, Vivienda.localidad_id == Localidad.id)
                ).group_by(
                    Localidad.nombre
                ).order_by(
                    Localidad.nombre
                )

                return session.execute(consulta).mappings().all()
        except Exception as e:
            print(f"Error al generar estimaciones estadisticas por localidad: {e}")
            return []

    def obtener_todas_las_edades(self, 
                                 municipio_id: Optional[int] = None, 
                                 localidad_id: Optional[int] = None
                                 ) -> List[int]:
        """
        Obtiene una lista de las edades de todos los habitantes.
        Acepta filtros dinámicos.
        """
        try:
            with self._get_session() as session:
                # Base de la consulta
                statement = select(Habitante.edad)

                # --- AÑADIR FILTROS DINÁMICOS ---
                if localidad_id or municipio_id:
                    # Necesitamos JOINs para filtrar por ubicación
                    statement = statement.join(Vivienda, Habitante.vivienda_id == Vivienda.id) \
                                         .join(Localidad, Vivienda.localidad_id == Localidad.id)
                    
                    if localidad_id:
                        statement = statement.where(Localidad.id == localidad_id)
                    elif municipio_id:
                        statement = statement.where(Localidad.municipio_id == municipio_id)

                return session.scalars(statement).all()
        except Exception as e:
            print(f"Error al obtener la lista de edades: {e}")
            return []