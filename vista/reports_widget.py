from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QHeaderView, QMessageBox, QGroupBox, QHBoxLayout, 
    QSplitter, QComboBox, QLabel, QFormLayout
)
from PyQt5.QtCore import Qt

# --- 1. IMPORTACIONES DE PYQTGRAPH y NUMPY ---
import pyqtgraph as pg
import numpy as np

pg.setConfigOption('background', '#2E2F30')
pg.setConfigOption('foreground', '#E0E0E0')


class ReportsWidget(QWidget):
    """
    Pestaña que muestra los reportes y el dashboard principal.
    AHORA incluye filtros de datos (Municipio/Localidad).
    """
    def __init__(self, censo_controller, catalogo_controller):
        super().__init__()
        self.censo_controller = censo_controller
        self.catalogo_controller = catalogo_controller
        
        self.histograma_widget = pg.PlotWidget(antialiasing=True)
        
        self.setup_ui()
        self.poblar_filtros_municipio()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Grupo de Filtros (Sin cambios) ---
        filtros_group = QGroupBox("Filtros del Dashboard")
        filtros_layout = QFormLayout()
        self.combo_filtro_municipio = QComboBox()
        self.combo_filtro_localidad = QComboBox()
        self.btn_aplicar_filtros = QPushButton("Aplicar Filtros y Recargar")
        self.btn_limpiar_filtros = QPushButton("Limpiar Filtros")
        filtros_layout.addRow(QLabel("Filtrar por Municipio:"), self.combo_filtro_municipio)
        filtros_layout.addRow(QLabel("Filtrar por Localidad:"), self.combo_filtro_localidad)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_aplicar_filtros)
        btn_layout.addWidget(self.btn_limpiar_filtros)
        filtros_layout.addRow(btn_layout)
        filtros_group.setLayout(filtros_layout)
        main_layout.addWidget(filtros_group)

        # --- Grupos de Reportes (Sin cambios) ---
        poblacion_group = QGroupBox("Dashboard: Población por Ubicación")
        poblacion_layout = QVBoxLayout()
        self.tabla_reporte_poblacion = QTableWidget()
        self.tabla_reporte_poblacion.setColumnCount(3)
        self.tabla_reporte_poblacion.setHorizontalHeaderLabels(["Municipio", "Localidad", "Total Habitantes"])
        self.tabla_reporte_poblacion.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        poblacion_layout.addWidget(self.tabla_reporte_poblacion)
        poblacion_group.setLayout(poblacion_layout)
        
        tipo_vivienda_group = QGroupBox("Reporte: Habitantes por Tipo de Vivienda")
        tipo_vivienda_layout = QVBoxLayout()
        self.tabla_reporte_tipo = QTableWidget()
        self.tabla_reporte_tipo.setColumnCount(2)
        self.tabla_reporte_tipo.setHorizontalHeaderLabels(["Tipo de Vivienda", "Total Habitantes"])
        self.tabla_reporte_tipo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tipo_vivienda_layout.addWidget(self.tabla_reporte_tipo)
        tipo_vivienda_group.setLayout(tipo_vivienda_layout)

        edad_group = QGroupBox("Estimación Estadística: Distribución de Edades")
        edad_layout = QVBoxLayout()
        edad_layout.addWidget(self.histograma_widget) # Widget del histograma
        edad_group.setLayout(edad_layout)

        # --- Layout (Sin cambios) ---
        splitter_vertical = QSplitter(Qt.Vertical)
        splitter_horizontal = QSplitter(Qt.Horizontal)
        splitter_horizontal.addWidget(poblacion_group)
        splitter_horizontal.addWidget(tipo_vivienda_group)
        splitter_vertical.addWidget(splitter_horizontal)
        splitter_vertical.addWidget(edad_group)
        main_layout.addWidget(splitter_vertical)
        
        # --- Conexiones (Sin cambios) ---
        self.btn_aplicar_filtros.clicked.connect(self.recargar_todos_los_reportes)
        self.btn_limpiar_filtros.clicked.connect(self.limpiar_filtros_y_recargar)
        self.combo_filtro_municipio.currentIndexChanged.connect(self.actualizar_filtro_localidad)
        
        # Carga inicial de datos
        self.recargar_todos_los_reportes()

    # --- Métodos de Filtros (Sin cambios) ---
    def poblar_filtros_municipio(self):
        self.combo_filtro_municipio.clear()
        self.combo_filtro_municipio.addItem("Todos los Municipios", None) 
        try:
            municipios = self.catalogo_controller.obtener_todos_municipios()
            for m in municipios:
                self.combo_filtro_municipio.addItem(m.nombre, m.id)
        except Exception as e:
            print(f"Error poblando filtro de municipios: {e}")

    def actualizar_filtro_localidad(self):
        self.combo_filtro_localidad.clear()
        self.combo_filtro_localidad.addItem("Todas las Localidades", None) 
        municipio_id = self.combo_filtro_municipio.currentData()
        if municipio_id is not None:
            try:
                localidades = self.catalogo_controller.obtener_localidades_por_municipio(municipio_id)
                for loc in localidades:
                    self.combo_filtro_localidad.addItem(loc.nombre, loc.id)
            except Exception as e:
                print(f"Error poblando filtro de localidades: {e}")

    def limpiar_filtros_y_recargar(self):
        self.combo_filtro_municipio.setCurrentIndex(0)
        self.recargar_todos_los_reportes()

    def recargar_todos_los_reportes(self):
        print("Recargando reportes con filtros...")
        self.cargar_reporte_poblacion()
        self.cargar_reporte_tipo_vivienda()
        self.cargar_histograma_edad()
        print("Reportes recargados.")

    # --- Métodos de Carga de Datos (Tablas sin cambios) ---
    def cargar_reporte_poblacion(self):
        self.tabla_reporte_poblacion.setRowCount(0)
        municipio_id = self.combo_filtro_municipio.currentData()
        localidad_id = self.combo_filtro_localidad.currentData()
        datos_reporte = self.censo_controller.generar_dashboard_poblacion(municipio_id, localidad_id)
        if not datos_reporte:
            QMessageBox.information(self, "Reporte de Población", "No hay datos de población para los filtros seleccionados.")
            return
        for i, fila in enumerate(datos_reporte):
            self.tabla_reporte_poblacion.insertRow(i)
            self.tabla_reporte_poblacion.setItem(i, 0, QTableWidgetItem(fila['municipio']))
            self.tabla_reporte_poblacion.setItem(i, 1, QTableWidgetItem(fila['localidad']))
            self.tabla_reporte_poblacion.setItem(i, 2, QTableWidgetItem(str(fila['total_habitantes'])))

    def cargar_reporte_tipo_vivienda(self):
        self.tabla_reporte_tipo.setRowCount(0)
        municipio_id = self.combo_filtro_municipio.currentData()
        localidad_id = self.combo_filtro_localidad.currentData()
        datos_reporte = self.censo_controller.generar_reporte_tipos_vivienda(municipio_id, localidad_id)
        if not datos_reporte:
            QMessageBox.information(self, "Reporte de Vivienda", "No hay datos de tipos de vivienda para los filtros seleccionados.")
            return
        for i, fila in enumerate(datos_reporte):
            self.tabla_reporte_tipo.insertRow(i)
            self.tabla_reporte_tipo.setItem(i, 0, QTableWidgetItem(fila['tipo_vivienda']))
            self.tabla_reporte_tipo.setItem(i, 1, QTableWidgetItem(str(fila['habitantes'])))

    # --- CAMBIO 3: Método de Carga de Histograma (Tema Oscuro) ---
    def cargar_histograma_edad(self):
        municipio_id = self.combo_filtro_municipio.currentData()
        localidad_id = self.combo_filtro_localidad.currentData()

        lista_edades = self.censo_controller.generar_reporte_distribucion_edad(municipio_id, localidad_id)
        
        self.histograma_widget.clear()

        if not lista_edades:
            QMessageBox.information(self, "Reporte de Edades", "No hay datos de edades para los filtros seleccionados.")
            return

        try:
            hist, bin_edges = np.histogram(lista_edades, bins=20)
            width = bin_edges[1] - bin_edges[0]
            
            # (a) Usar el color azul de acento del QSS para las barras
            bar_item = pg.BarGraphItem(
                x=bin_edges[:-1],  
                height=hist,       
                width=width * 0.9, # Un poco más delgadas
                brush='#007ACC'    # Color de relleno (azul acento QSS)
            )
            
            self.histograma_widget.addItem(bar_item)
            
            # (b) Usar el color de título del QGroupBox
            self.histograma_widget.setTitle(
                'Distribución de Edades de la Población (Filtrada)', 
                color='#00BFFF', # Color de título (azul claro QSS)
                size='11pt'
            )
            
            # (c) Las etiquetas de los ejes ya heredan el color ('foreground')
            self.histograma_widget.setLabel('bottom', 'Rango de Edad')
            self.histograma_widget.setLabel('left', 'Cantidad de Habitantes')
            self.histograma_widget.showGrid(x=True, y=True, alpha=0.2) # Rejilla sutil
            
        except Exception as e:
            print(f"Error al dibujar el histograma de PyQtGraph: {e}")
            QMessageBox.critical(self, "Error de Gráfico", f"No se pudo dibujar el histograma: {e}")