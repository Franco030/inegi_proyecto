from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QLineEdit, QLabel, QFormLayout, QGroupBox, QMessageBox,
    QAbstractItemView, QComboBox, QHeaderView, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from modelo import Municipio, Localidad, TipoVivienda, ActividadEconomica

class CatalogoWidget(QWidget):
    """
    Pestaña para el CRUD de todos los catálogos (Requisito 2).
    Rediseñada con un QTabWidget para manejar Múltiples CRUDs.
    Implementa filtros de búsqueda en vivo para todas las tablas.
    """
    
    # --- SEÑAL ---
    # Esta señal se emite cuando un catálogo cambia (guardar, eliminar)
    # CensoWidget la escuchará para recargar sus ComboBoxes.
    catalogos_actualizados = pyqtSignal()
    
    def __init__(self, catalogo_controller):
        super().__init__()
        self.catalogo_controller = catalogo_controller
        
        # IDs de selección para cada pestaña
        self.current_municipio_id = None
        self.current_localidad_id = None
        self.current_tipo_vivienda_id = None
        self.current_actividad_id = None
        
        self.setup_ui()
        
        # Carga inicial de datos
        self.poblar_combo_municipios()
        self.cargar_municipios()
        self.cargar_localidades()
        self.cargar_tipos_vivienda()
        self.cargar_actividades_economicas()

    def setup_ui(self):
        # Layout principal que contendrá las pestañas
        main_layout = QVBoxLayout(self)
        tab_widget = QTabWidget()
        # Asignar un objectName para el QSS (estilo de pestañas internas)
        tab_widget.setObjectName("catalogo_tabs")
        
        # Crear cada pestaña y añadirla
        tab_widget.addTab(self.crear_tab_municipios(), "Municipios")
        tab_widget.addTab(self.crear_tab_localidades(), "Localidades")
        tab_widget.addTab(self.crear_tab_tipos_vivienda(), "Tipos de Vivienda")
        tab_widget.addTab(self.crear_tab_actividades(), "Actividades Económicas")
        
        main_layout.addWidget(tab_widget)

    # --- PESTAÑA 1: MUNICIPIOS ---
    def crear_tab_municipios(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Formulario
        form_widget_muni = QWidget()
        form_layout_muni = QFormLayout(form_widget_muni)
        self.txt_municipio_nombre = QLineEdit()
        self.btn_guardar_municipio = QPushButton("Guardar (Nuevo/Actualizar)")
        self.btn_limpiar_form_muni = QPushButton("Limpiar Formulario")
        self.btn_eliminar_municipio = QPushButton("Eliminar Seleccionado")
        self.btn_eliminar_municipio.setObjectName("btn_eliminar") # Para QSS
        
        form_layout_muni.addRow(QLabel("Nombre:"), self.txt_municipio_nombre)
        form_layout_muni.addRow(self.btn_guardar_municipio)
        form_layout_muni.addRow(self.btn_limpiar_form_muni)
        form_layout_muni.addRow(self.btn_eliminar_municipio)

        # Lado Derecho (Filtro + Tabla)
        right_layout = QVBoxLayout()
        self.filtro_municipio = QLineEdit()
        self.filtro_municipio.setPlaceholderText("Filtrar por nombre...")
        
        self.tabla_municipios = QTableWidget()
        self.tabla_municipios.setColumnCount(2)
        self.tabla_municipios.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla_municipios.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_municipios.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_municipios.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        right_layout.addWidget(QLabel("Filtrar Tabla:"))
        right_layout.addWidget(self.filtro_municipio)
        right_layout.addWidget(self.tabla_municipios)
        
        layout.addWidget(form_widget_muni, 1)
        layout.addLayout(right_layout, 2)
        
        # Conexiones
        self.btn_guardar_municipio.clicked.connect(self.guardar_municipio)
        self.btn_limpiar_form_muni.clicked.connect(self.limpiar_form_municipio)
        self.btn_eliminar_municipio.clicked.connect(self.eliminar_municipio)
        self.tabla_municipios.itemClicked.connect(self.seleccionar_municipio)
        self.filtro_municipio.textChanged.connect(self.filtrar_tabla_municipios)
        
        return widget

    # --- PESTAÑA 2: LOCALIDADES ---
    def crear_tab_localidades(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Formulario
        form_widget_loc = QWidget()
        form_layout_loc = QFormLayout(form_widget_loc)
        self.txt_localidad_nombre = QLineEdit()
        self.combo_localidad_municipio = QComboBox() 
        self.btn_guardar_localidad = QPushButton("Guardar (Nuevo/Actualizar)")
        self.btn_limpiar_form_loc = QPushButton("Limpiar Formulario")
        self.btn_eliminar_localidad = QPushButton("Eliminar Seleccionado")
        self.btn_eliminar_localidad.setObjectName("btn_eliminar") # Para QSS
        
        form_layout_loc.addRow(QLabel("Nombre:"), self.txt_localidad_nombre)
        form_layout_loc.addRow(QLabel("Municipio:"), self.combo_localidad_municipio)
        form_layout_loc.addRow(self.btn_guardar_localidad)
        form_layout_loc.addRow(self.btn_limpiar_form_loc)
        form_layout_loc.addRow(self.btn_eliminar_localidad)

        # Lado Derecho (Filtro + Tabla)
        right_layout = QVBoxLayout()
        self.filtro_localidad = QLineEdit()
        self.filtro_localidad.setPlaceholderText("Filtrar por nombre o municipio...")
        
        self.tabla_localidades = QTableWidget()
        self.tabla_localidades.setColumnCount(3)
        self.tabla_localidades.setHorizontalHeaderLabels(["ID", "Nombre", "Municipio"])
        self.tabla_localidades.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_localidades.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_localidades.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        right_layout.addWidget(QLabel("Filtrar Tabla:"))
        right_layout.addWidget(self.filtro_localidad)
        right_layout.addWidget(self.tabla_localidades)
        
        layout.addWidget(form_widget_loc, 1)
        layout.addLayout(right_layout, 2)
        
        # Conexiones
        self.btn_guardar_localidad.clicked.connect(self.guardar_localidad)
        self.btn_limpiar_form_loc.clicked.connect(self.limpiar_form_localidad)
        self.btn_eliminar_localidad.clicked.connect(self.eliminar_localidad)
        self.tabla_localidades.itemClicked.connect(self.seleccionar_localidad)
        self.filtro_localidad.textChanged.connect(self.filtrar_tabla_localidades)
        
        return widget

    # --- PESTAÑA 3: TIPOS DE VIVIENDA ---
    def crear_tab_tipos_vivienda(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Formulario
        form_widget_tipo = QWidget()
        form_layout_tipo = QFormLayout(form_widget_tipo)
        self.txt_tipo_vivienda_nombre = QLineEdit()
        self.btn_guardar_tipo = QPushButton("Guardar (Nuevo/Actualizar)")
        self.btn_limpiar_form_tipo = QPushButton("Limpiar Formulario")
        self.btn_eliminar_tipo = QPushButton("Eliminar Seleccionado")
        self.btn_eliminar_tipo.setObjectName("btn_eliminar") # Para QSS
        
        form_layout_tipo.addRow(QLabel("Nombre:"), self.txt_tipo_vivienda_nombre)
        form_layout_tipo.addRow(self.btn_guardar_tipo)
        form_layout_tipo.addRow(self.btn_limpiar_form_tipo)
        form_layout_tipo.addRow(self.btn_eliminar_tipo)

        # Lado Derecho (Filtro + Tabla)
        right_layout = QVBoxLayout()
        self.filtro_tipo_vivienda = QLineEdit()
        self.filtro_tipo_vivienda.setPlaceholderText("Filtrar por nombre...")

        self.tabla_tipos_vivienda = QTableWidget()
        self.tabla_tipos_vivienda.setColumnCount(2)
        self.tabla_tipos_vivienda.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla_tipos_vivienda.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_tipos_vivienda.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_tipos_vivienda.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        right_layout.addWidget(QLabel("Filtrar Tabla:"))
        right_layout.addWidget(self.filtro_tipo_vivienda)
        right_layout.addWidget(self.tabla_tipos_vivienda)
        
        layout.addWidget(form_widget_tipo, 1)
        layout.addLayout(right_layout, 2)
        
        # Conexiones
        self.btn_guardar_tipo.clicked.connect(self.guardar_tipo_vivienda)
        self.btn_limpiar_form_tipo.clicked.connect(self.limpiar_form_tipo_vivienda)
        self.btn_eliminar_tipo.clicked.connect(self.eliminar_tipo_vivienda)
        self.tabla_tipos_vivienda.itemClicked.connect(self.seleccionar_tipo_vivienda)
        self.filtro_tipo_vivienda.textChanged.connect(self.filtrar_tabla_tipos_vivienda)
        
        return widget

    # --- PESTAÑA 4: ACTIVIDADES ECONÓMICAS ---
    def crear_tab_actividades(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Formulario
        form_widget_act = QWidget()
        form_layout_act = QFormLayout(form_widget_act)
        self.txt_actividad_nombre = QLineEdit()
        self.btn_guardar_actividad = QPushButton("Guardar (Nuevo/Actualizar)")
        self.btn_limpiar_form_act = QPushButton("Limpiar Formulario")
        self.btn_eliminar_actividad = QPushButton("Eliminar Seleccionado")
        self.btn_eliminar_actividad.setObjectName("btn_eliminar") # Para QSS
        
        form_layout_act.addRow(QLabel("Nombre:"), self.txt_actividad_nombre)
        form_layout_act.addRow(self.btn_guardar_actividad)
        form_layout_act.addRow(self.btn_limpiar_form_act)
        form_layout_act.addRow(self.btn_eliminar_actividad)

        # Lado Derecho (Filtro + Tabla)
        right_layout = QVBoxLayout()
        self.filtro_actividad = QLineEdit()
        self.filtro_actividad.setPlaceholderText("Filtrar por nombre...")

        self.tabla_actividades = QTableWidget()
        self.tabla_actividades.setColumnCount(2)
        self.tabla_actividades.setHorizontalHeaderLabels(["ID", "Nombre"])
        self.tabla_actividades.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_actividades.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_actividades.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        right_layout.addWidget(QLabel("Filtrar Tabla:"))
        right_layout.addWidget(self.filtro_actividad)
        right_layout.addWidget(self.tabla_actividades)
        
        layout.addWidget(form_widget_act, 1)
        layout.addLayout(right_layout, 2)
        
        # Conexiones
        self.btn_guardar_actividad.clicked.connect(self.guardar_actividad_economica)
        self.btn_limpiar_form_act.clicked.connect(self.limpiar_form_actividad)
        self.btn_eliminar_actividad.clicked.connect(self.eliminar_actividad_economica)
        self.tabla_actividades.itemClicked.connect(self.seleccionar_actividad_economica)
        self.filtro_actividad.textChanged.connect(self.filtrar_tabla_actividades)
        
        return widget

    # --- MÉTODOS DE FILTRO ---
    def filtrar_tabla_municipios(self):
        filtro_texto = self.filtro_municipio.text().lower()
        for i in range(self.tabla_municipios.rowCount()):
            item_nombre = self.tabla_municipios.item(i, 1) # Columna "Nombre"
            if item_nombre:
                if filtro_texto in item_nombre.text().lower():
                    self.tabla_municipios.setRowHidden(i, False)
                else:
                    self.tabla_municipios.setRowHidden(i, True)

    def filtrar_tabla_localidades(self):
        filtro_texto = self.filtro_localidad.text().lower()
        for i in range(self.tabla_localidades.rowCount()):
            item_nombre = self.tabla_localidades.item(i, 1) # Columna "Nombre"
            item_municipio = self.tabla_localidades.item(i, 2) # Columna "Municipio"
            
            match_nombre = (item_nombre and filtro_texto in item_nombre.text().lower())
            match_municipio = (item_municipio and filtro_texto in item_municipio.text().lower())
            
            if match_nombre or match_municipio:
                self.tabla_localidades.setRowHidden(i, False)
            else:
                self.tabla_localidades.setRowHidden(i, True)

    def filtrar_tabla_tipos_vivienda(self):
        filtro_texto = self.filtro_tipo_vivienda.text().lower()
        for i in range(self.tabla_tipos_vivienda.rowCount()):
            item_nombre = self.tabla_tipos_vivienda.item(i, 1) # Columna "Nombre"
            if item_nombre:
                if filtro_texto in item_nombre.text().lower():
                    self.tabla_tipos_vivienda.setRowHidden(i, False)
                else:
                    self.tabla_tipos_vivienda.setRowHidden(i, True)

    def filtrar_tabla_actividades(self):
        filtro_texto = self.filtro_actividad.text().lower()
        for i in range(self.tabla_actividades.rowCount()):
            item_nombre = self.tabla_actividades.item(i, 1) # Columna "Nombre"
            if item_nombre:
                if filtro_texto in item_nombre.text().lower():
                    self.tabla_actividades.setRowHidden(i, False)
                else:
                    self.tabla_actividades.setRowHidden(i, True)

    # --- MÉTODOS CRUD (MUNICIPIO) ---
    def limpiar_form_municipio(self): 
        self.current_municipio_id = None
        self.txt_municipio_nombre.clear()
        self.tabla_municipios.clearSelection()

    def cargar_municipios(self):
        self.tabla_municipios.setRowCount(0)
        lista_municipios: list[Municipio] = self.catalogo_controller.obtener_todos_municipios()
        for i, municipio in enumerate(lista_municipios):
            self.tabla_municipios.insertRow(i)
            self.tabla_municipios.setItem(i, 0, QTableWidgetItem(str(municipio.id)))
            self.tabla_municipios.setItem(i, 1, QTableWidgetItem(municipio.nombre))
        self.limpiar_form_municipio()
        self.poblar_combo_municipios() # Recargar combo en pestaña localidades

    def seleccionar_municipio(self, item): 
        fila = self.tabla_municipios.row(item)
        id_municipio = self.tabla_municipios.item(fila, 0).text()
        nombre_municipio = self.tabla_municipios.item(fila, 1).text()
        self.current_municipio_id = int(id_municipio)
        self.txt_municipio_nombre.setText(nombre_municipio)

    def guardar_municipio(self): 
        nombre = self.txt_municipio_nombre.text()
        if not nombre:
            QMessageBox.warning(self, "Datos Incompletos", "El nombre del municipio no puede estar vacío.")
            return
        if self.current_municipio_id is None:
            resultado = self.catalogo_controller.guardar_municipio(nombre)
            mensaje = f"Municipio '{resultado.nombre}' creado."
        else:
            resultado = self.catalogo_controller.actualizar_municipio(self.current_municipio_id, nombre)
            mensaje = f"Municipio '{resultado.nombre}' actualizado."
        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.cargar_municipios()
            self.catalogos_actualizados.emit()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el municipio.")

    def eliminar_municipio(self): 
        if self.current_municipio_id is None:
            QMessageBox.warning(self, "Sin Selección", "Seleccione un municipio de la tabla para eliminar.")
            return
        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea eliminar el municipio ID {self.current_municipio_id}?\nADVERTENCIA: Esto eliminará sus localidades asociadas.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            exito = self.catalogo_controller.eliminar_municipio(self.current_municipio_id)
            if exito:
                QMessageBox.information(self, "Eliminado", "El municipio ha sido eliminado.")
                self.cargar_municipios()
                self.catalogos_actualizados.emit()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el municipio (puede tener localidades activas).")

    # --- MÉTODOS DE LOCALIDAD ---
    def poblar_combo_municipios(self):
        self.combo_localidad_municipio.clear()
        self.combo_localidad_municipio.addItem("Seleccione un Municipio...", None)
        municipios = self.catalogo_controller.obtener_todos_municipios()
        for m in municipios:
            self.combo_localidad_municipio.addItem(m.nombre, m.id)

    def limpiar_form_localidad(self): 
        self.current_localidad_id = None
        self.txt_localidad_nombre.clear()
        self.combo_localidad_municipio.setCurrentIndex(0)
        self.tabla_localidades.clearSelection()

    def cargar_localidades(self): 
        self.tabla_localidades.setRowCount(0)
        lista_localidades: list[Localidad] = self.catalogo_controller.obtener_todas_localidades()
        for i, loc in enumerate(lista_localidades):
            self.tabla_localidades.insertRow(i)
            self.tabla_localidades.setItem(i, 0, QTableWidgetItem(str(loc.id)))
            self.tabla_localidades.setItem(i, 1, QTableWidgetItem(loc.nombre))
            self.tabla_localidades.setItem(i, 2, QTableWidgetItem(loc.municipio.nombre))
        self.limpiar_form_localidad()

    def seleccionar_localidad(self, item): 
        fila = self.tabla_localidades.row(item)
        id_localidad = self.tabla_localidades.item(fila, 0).text()
        nombre_localidad = self.tabla_localidades.item(fila, 1).text()
        nombre_municipio = self.tabla_localidades.item(fila, 2).text()
        self.current_localidad_id = int(id_localidad)
        self.txt_localidad_nombre.setText(nombre_localidad)
        index = self.combo_localidad_municipio.findText(nombre_municipio, Qt.MatchFixedString)
        if index >= 0:
            self.combo_localidad_municipio.setCurrentIndex(index)

    def guardar_localidad(self): 
        nombre = self.txt_localidad_nombre.text()
        id_municipio = self.combo_localidad_municipio.currentData()
        if not nombre or not id_municipio:
            QMessageBox.warning(self, "Datos Incompletos", "Debe ingresar un nombre y seleccionar un municipio.")
            return
        if self.current_localidad_id is None:
            resultado = self.catalogo_controller.guardar_localidad(nombre, id_municipio)
            mensaje = f"Localidad '{resultado.nombre}' creada."
        else:
            resultado = self.catalogo_controller.actualizar_localidad(self.current_localidad_id, nombre, id_municipio)
            mensaje = f"Localidad '{resultado.nombre}' actualizada."
        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.cargar_localidades()
            self.catalogos_actualizados.emit()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la localidad.")

    def eliminar_localidad(self): 
        if self.current_localidad_id is None:
            QMessageBox.warning(self, "Sin Selección", "Seleccione una localidad de la tabla para eliminar.")
            return
        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea eliminar la localidad ID {self.current_localidad_id}?\nADVERTENCIA: Esto eliminará sus viviendas asociadas.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            exito = self.catalogo_controller.eliminar_localidad(self.current_localidad_id)
            if exito:
                QMessageBox.information(self, "Eliminado", "La localidad ha sido eliminada.")
                self.cargar_localidades()
                self.catalogos_actualizados.emit()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la localidad (puede tener viviendas activas).")

    # --- MÉTODOS PARA TIPO VIVIENDA ---
    
    def limpiar_form_tipo_vivienda(self):
        self.current_tipo_vivienda_id = None
        self.txt_tipo_vivienda_nombre.clear()
        self.tabla_tipos_vivienda.clearSelection()

    def cargar_tipos_vivienda(self):
        self.tabla_tipos_vivienda.setRowCount(0)
        lista_tipos: list[TipoVivienda] = self.catalogo_controller.obtener_todos_tipos_vivienda()
        for i, tipo in enumerate(lista_tipos):
            self.tabla_tipos_vivienda.insertRow(i)
            self.tabla_tipos_vivienda.setItem(i, 0, QTableWidgetItem(str(tipo.id)))
            self.tabla_tipos_vivienda.setItem(i, 1, QTableWidgetItem(tipo.nombre))
        self.limpiar_form_tipo_vivienda()

    def seleccionar_tipo_vivienda(self, item):
        fila = self.tabla_tipos_vivienda.row(item)
        id_tipo = self.tabla_tipos_vivienda.item(fila, 0).text()
        nombre_tipo = self.tabla_tipos_vivienda.item(fila, 1).text()
        self.current_tipo_vivienda_id = int(id_tipo)
        self.txt_tipo_vivienda_nombre.setText(nombre_tipo)

    def guardar_tipo_vivienda(self):
        nombre = self.txt_tipo_vivienda_nombre.text()
        if not nombre:
            QMessageBox.warning(self, "Datos Incompletos", "El nombre del tipo de vivienda no puede estar vacío.")
            return
        if self.current_tipo_vivienda_id is None:
            resultado = self.catalogo_controller.guardar_tipo_vivienda(nombre)
            mensaje = f"Tipo de Vivienda '{resultado.nombre}' creado."
        else:
            resultado = self.catalogo_controller.actualizar_tipo_vivienda(self.current_tipo_vivienda_id, nombre)
            mensaje = f"Tipo de Vivienda '{resultado.nombre}' actualizado."
        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.cargar_tipos_vivienda()
            self.catalogos_actualizados.emit()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar el tipo de vivienda.")

    def eliminar_tipo_vivienda(self):
        if self.current_tipo_vivienda_id is None:
            QMessageBox.warning(self, "Sin Selección", "Seleccione un tipo de la tabla para eliminar.")
            return
        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea eliminar el Tipo de Vivienda ID {self.current_tipo_vivienda_id}?\nADVERTENCIA: Esto eliminará sus viviendas asociadas.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            exito = self.catalogo_controller.eliminar_tipo_vivienda(self.current_tipo_vivienda_id)
            if exito:
                QMessageBox.information(self, "Eliminado", "El tipo de vivienda ha sido eliminado.")
                self.cargar_tipos_vivienda()
                self.catalogos_actualizados.emit()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar (puede tener viviendas activas).")

    # --- MÉTODOS PARA ACTIVIDAD ECONOMICA ---
    
    def limpiar_form_actividad(self):
        self.current_actividad_id = None
        self.txt_actividad_nombre.clear()
        self.tabla_actividades.clearSelection()

    def cargar_actividades_economicas(self):
        self.tabla_actividades.setRowCount(0)
        lista_act: list[ActividadEconomica] = self.catalogo_controller.obtener_todas_actividades_economicas()
        for i, act in enumerate(lista_act):
            self.tabla_actividades.insertRow(i)
            self.tabla_actividades.setItem(i, 0, QTableWidgetItem(str(act.id)))
            self.tabla_actividades.setItem(i, 1, QTableWidgetItem(act.nombre))
        self.limpiar_form_actividad()

    def seleccionar_actividad_economica(self, item):
        fila = self.tabla_actividades.row(item)
        id_act = self.tabla_actividades.item(fila, 0).text()
        nombre_act = self.tabla_actividades.item(fila, 1).text()
        self.current_actividad_id = int(id_act)
        self.txt_actividad_nombre.setText(nombre_act)

    def guardar_actividad_economica(self):
        nombre = self.txt_actividad_nombre.text()
        if not nombre:
            QMessageBox.warning(self, "Datos Incompletos", "El nombre de la actividad no puede estar vacío.")
            return
        if self.current_actividad_id is None:
            resultado = self.catalogo_controller.guardar_actividad_economica(nombre)
            mensaje = f"Actividad '{resultado.nombre}' creada."
        else:
            resultado = self.catalogo_controller.actualizar_actividad_economica(self.current_actividad_id, nombre)
            mensaje = f"Actividad '{resultado.nombre}' actualizada."
        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.cargar_actividades_economicas()
            self.catalogos_actualizados.emit()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la actividad.")

    def eliminar_actividad_economica(self):
        if self.current_actividad_id is None:
            QMessageBox.warning(self, "Sin Selección", "Seleccione una actividad de la tabla para eliminar.")
            return
        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea eliminar la Actividad ID {self.current_actividad_id}?\nADVERTENCIA: Esto eliminará sus asociaciones con viviendas.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirmar == QMessageBox.Yes:
            exito = self.catalogo_controller.eliminar_actividad_economica(self.current_actividad_id)
            if exito:
                QMessageBox.information(self, "Eliminado", "La actividad ha sido eliminada.")
                self.cargar_actividades_economicas()
                self.catalogos_actualizados.emit()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar (puede estar en uso por viviendas).")