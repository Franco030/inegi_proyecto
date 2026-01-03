from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QLineEdit, QLabel, QFormLayout, QGroupBox, QMessageBox,
    QComboBox, QAbstractItemView, QHeaderView
)
from PyQt5.QtCore import Qt

class CensoWidget(QWidget):
    """
    Pestaña para las operaciones principales del censo (CRUD Completo).
    Implementa filtros de búsqueda en vivo para todas las tablas.
    """
    def __init__(self, censo_controller, catalogo_controller):
        super().__init__()
        self.censo_controller = censo_controller
        self.catalogo_controller = catalogo_controller
        
        self.current_vivienda_id = None 
        self.current_habitante_id = None
        self.current_actividad_id = None
        
        self.setup_ui()
        self.poblar_comboboxes()
        self.cargar_tabla_viviendas()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # --- COLUMNA IZQUIERDA (Sin cambios) ---
        col_izquierda = QVBoxLayout()
        vivienda_group = QGroupBox("Formulario de Vivienda")
        vivienda_layout = QFormLayout()
        self.txt_vivienda_direccion = QLineEdit()
        self.combo_localidad = QComboBox()
        self.combo_tipo_vivienda = QComboBox()
        self.btn_guardar_vivienda = QPushButton("Guardar / Actualizar Vivienda")
        self.btn_limpiar_vivienda = QPushButton("Limpiar / Cancelar Edición")
        self.btn_eliminar_vivienda = QPushButton("Eliminar Vivienda Seleccionada")
        vivienda_layout.addRow("Dirección:", self.txt_vivienda_direccion)
        vivienda_layout.addRow("Localidad:", self.combo_localidad)
        vivienda_layout.addRow("Tipo de Vivienda:", self.combo_tipo_vivienda)
        vivienda_layout.addRow(self.btn_guardar_vivienda)
        vivienda_layout.addRow(self.btn_limpiar_vivienda)
        vivienda_layout.addRow(self.btn_eliminar_vivienda)
        vivienda_group.setLayout(vivienda_layout)
        
        self.habitante_group = QGroupBox("Formulario de Habitante")
        habitante_layout = QFormLayout()
        self.lbl_habitante_vivienda = QLabel("Seleccione una vivienda de la tabla ->")
        self.txt_habitante_nombre = QLineEdit()
        self.txt_habitante_edad = QLineEdit()
        self.txt_habitante_sexo = QLineEdit()
        self.txt_habitante_parentesco = QLineEdit()
        self.btn_guardar_habitante = QPushButton("Guardar / Actualizar Habitante")
        self.btn_limpiar_habitante = QPushButton("Limpiar / Cancelar Edición")
        self.btn_eliminar_habitante = QPushButton("Eliminar Habitante Seleccionado")
        habitante_layout.addRow(self.lbl_habitante_vivienda)
        habitante_layout.addRow("Nombre Completo:", self.txt_habitante_nombre)
        habitante_layout.addRow("Edad:", self.txt_habitante_edad)
        habitante_layout.addRow("Sexo (M/F):", self.txt_habitante_sexo)
        habitante_layout.addRow("Parentesco:", self.txt_habitante_parentesco)
        habitante_layout.addRow(self.btn_guardar_habitante)
        habitante_layout.addRow(self.btn_limpiar_habitante)
        habitante_layout.addRow(self.btn_eliminar_habitante)
        self.habitante_group.setLayout(habitante_layout)
        self.habitante_group.setEnabled(False) 
        
        col_izquierda.addWidget(vivienda_group)
        col_izquierda.addWidget(self.habitante_group)
        col_izquierda.addStretch()

        # --- COLUMNA DERECHA (Con Filtros) ---
        col_derecha = QVBoxLayout()
        
        # Tabla de Viviendas (Con Filtro)
        group_lista_viviendas = QGroupBox("Viviendas Registradas")
        layout_lista_viviendas = QVBoxLayout()
        
        self.filtro_viviendas = QLineEdit()
        self.filtro_viviendas.setPlaceholderText("Filtrar por dirección, localidad o tipo...")
        
        self.tabla_viviendas = QTableWidget()
        self.tabla_viviendas.setColumnCount(4)
        self.tabla_viviendas.setHorizontalHeaderLabels(["ID", "Dirección", "Localidad", "Tipo de Vivienda"])
        self.tabla_viviendas.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_viviendas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_viviendas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout_lista_viviendas.addWidget(QLabel("Filtrar Tabla:"))
        layout_lista_viviendas.addWidget(self.filtro_viviendas)
        layout_lista_viviendas.addWidget(self.tabla_viviendas)
        group_lista_viviendas.setLayout(layout_lista_viviendas)
        
        # Tabla de Habitantes (Con Filtro)
        group_habitantes = QGroupBox("Habitantes de la Vivienda Seleccionada (Req 8)")
        layout_habitantes = QVBoxLayout()

        self.filtro_habitantes = QLineEdit()
        self.filtro_habitantes.setPlaceholderText("Filtrar por nombre, edad o parentesco...")

        self.tabla_habitantes = QTableWidget()
        self.tabla_habitantes.setColumnCount(4) 
        self.tabla_habitantes.setHorizontalHeaderLabels(["ID", "Nombre", "Edad", "Parentesco"])
        self.tabla_habitantes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_habitantes.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_habitantes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout_habitantes.addWidget(QLabel("Filtrar Tabla:"))
        layout_habitantes.addWidget(self.filtro_habitantes)
        layout_habitantes.addWidget(self.tabla_habitantes)
        group_habitantes.setLayout(layout_habitantes)
        
        # Tabla de Actividades Económicas (Con Filtro)
        group_actividades = QGroupBox("Sostén Económico de la Vivienda (Req 11)")
        layout_actividades = QVBoxLayout()
        
        add_actividad_layout = QHBoxLayout()
        self.combo_add_actividad = QComboBox()
        self.btn_add_actividad = QPushButton("Añadir")
        add_actividad_layout.addWidget(QLabel("Añadir actividad:"))
        add_actividad_layout.addWidget(self.combo_add_actividad, 1)
        add_actividad_layout.addWidget(self.btn_add_actividad)
        
        self.filtro_actividades = QLineEdit()
        self.filtro_actividades.setPlaceholderText("Filtrar actividades asociadas...")

        self.tabla_actividades = QTableWidget()
        self.tabla_actividades.setColumnCount(2) 
        self.tabla_actividades.setHorizontalHeaderLabels(["ID", "Actividad"])
        self.tabla_actividades.setColumnHidden(0, True) 
        self.tabla_actividades.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_actividades.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_actividades.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_remove_actividad = QPushButton("Eliminar Actividad Seleccionada")

        layout_actividades.addLayout(add_actividad_layout)
        layout_actividades.addWidget(QLabel("Filtrar Actividades Asociadas:"))
        layout_actividades.addWidget(self.filtro_actividades)
        layout_actividades.addWidget(self.tabla_actividades)
        layout_actividades.addWidget(self.btn_remove_actividad)
        group_actividades.setLayout(layout_actividades)
        
        self.group_actividades = group_actividades 
        self.group_actividades.setEnabled(False)

        col_derecha.addWidget(group_lista_viviendas, 2)
        col_derecha.addWidget(group_habitantes, 1)
        col_derecha.addWidget(self.group_actividades, 1)

        main_layout.addLayout(col_izquierda, 1)
        main_layout.addLayout(col_derecha, 2)
        
        # --- Conexiones ---
        self.btn_guardar_vivienda.clicked.connect(self.guardar_vivienda)
        self.btn_limpiar_vivienda.clicked.connect(self.limpiar_form_vivienda)
        self.btn_eliminar_vivienda.clicked.connect(self.eliminar_vivienda)
        self.tabla_viviendas.itemClicked.connect(self.seleccionar_vivienda)
        
        self.btn_guardar_habitante.clicked.connect(self.guardar_habitante)
        self.btn_limpiar_habitante.clicked.connect(self.limpiar_form_habitante)
        self.btn_eliminar_habitante.clicked.connect(self.eliminar_habitante)
        self.tabla_habitantes.itemClicked.connect(self.seleccionar_habitante)

        self.btn_add_actividad.clicked.connect(self.asociar_actividad)
        self.btn_remove_actividad.clicked.connect(self.desasociar_actividad)
        self.tabla_actividades.itemClicked.connect(self.seleccionar_actividad)

        # Conexiones de Filtros (NUEVO)
        self.filtro_viviendas.textChanged.connect(self.filtrar_tabla_viviendas)
        self.filtro_habitantes.textChanged.connect(self.filtrar_tabla_habitantes)
        self.filtro_actividades.textChanged.connect(self.filtrar_tabla_actividades)

    # --- MÉTODOS DE FILTRO (NUEVOS) ---
    def filtrar_tabla_viviendas(self):
        filtro_texto = self.filtro_viviendas.text().lower()
        for i in range(self.tabla_viviendas.rowCount()):
            item_dir = self.tabla_viviendas.item(i, 1) # Dirección
            item_loc = self.tabla_viviendas.item(i, 2) # Localidad
            item_tipo = self.tabla_viviendas.item(i, 3) # Tipo

            match_dir = (item_dir and filtro_texto in item_dir.text().lower())
            match_loc = (item_loc and filtro_texto in item_loc.text().lower())
            match_tipo = (item_tipo and filtro_texto in item_tipo.text().lower())

            if match_dir or match_loc or match_tipo:
                self.tabla_viviendas.setRowHidden(i, False)
            else:
                self.tabla_viviendas.setRowHidden(i, True)

    def filtrar_tabla_habitantes(self):
        filtro_texto = self.filtro_habitantes.text().lower()
        for i in range(self.tabla_habitantes.rowCount()):
            item_nombre = self.tabla_habitantes.item(i, 1) # Nombre
            item_edad = self.tabla_habitantes.item(i, 2) # Edad
            item_par = self.tabla_habitantes.item(i, 3) # Parentesco

            match_nombre = (item_nombre and filtro_texto in item_nombre.text().lower())
            match_edad = (item_edad and filtro_texto in item_edad.text().lower())
            match_par = (item_par and filtro_texto in item_par.text().lower())

            if match_nombre or match_edad or match_par:
                self.tabla_habitantes.setRowHidden(i, False)
            else:
                self.tabla_habitantes.setRowHidden(i, True)

    def filtrar_tabla_actividades(self):
        filtro_texto = self.filtro_actividades.text().lower()
        for i in range(self.tabla_actividades.rowCount()):
            item_act = self.tabla_actividades.item(i, 1) # Nombre Actividad
            if item_act:
                if filtro_texto in item_act.text().lower():
                    self.tabla_actividades.setRowHidden(i, False)
                else:
                    self.tabla_actividades.setRowHidden(i, True)

    # --- MÉTODOS DE CARGA Y LIMPIEZA ---
    def poblar_comboboxes(self):
        # Llenar Localidades
        self.combo_localidad.clear()
        self.combo_localidad.addItem("Seleccione...", None)
        localidades = self.catalogo_controller.obtener_todas_localidades() 
        for loc in localidades:
            self.combo_localidad.addItem(f"{loc.nombre} ({loc.municipio.nombre})", loc.id)
            
        # Llenar Tipos de Vivienda
        self.combo_tipo_vivienda.clear()
        self.combo_tipo_vivienda.addItem("Seleccione...", None)
        tipos = self.catalogo_controller.obtener_todos_tipos_vivienda()
        for tipo in tipos:
            self.combo_tipo_vivienda.addItem(tipo.nombre, tipo.id)
            
        # Llenar ComboBox de Actividades Económicas
        self.combo_add_actividad.clear()
        self.combo_add_actividad.addItem("Seleccione para añadir...", None)
        actividades = self.catalogo_controller.obtener_todas_actividades_economicas()
        for act in actividades:
            self.combo_add_actividad.addItem(act.nombre, act.id)
            
    def cargar_tabla_viviendas(self):
        self.tabla_viviendas.setRowCount(0)
        viviendas = self.censo_controller.obtener_todas_viviendas_con_localidad()
        
        for i, vivienda in enumerate(viviendas):
            self.tabla_viviendas.insertRow(i)
            self.tabla_viviendas.setItem(i, 0, QTableWidgetItem(str(vivienda.id)))
            self.tabla_viviendas.setItem(i, 1, QTableWidgetItem(vivienda.direccion))
            self.tabla_viviendas.setItem(i, 2, QTableWidgetItem(vivienda.localidad.nombre))
            self.tabla_viviendas.setItem(i, 3, QTableWidgetItem(vivienda.tipo_vivienda.nombre))
        
        self.limpiar_form_vivienda() 

    def limpiar_form_vivienda(self):
        self.current_vivienda_id = None
        self.txt_vivienda_direccion.clear()
        self.combo_localidad.setCurrentIndex(0)
        self.combo_tipo_vivienda.setCurrentIndex(0)
        self.tabla_viviendas.clearSelection()
        
        self.habitante_group.setEnabled(False)
        self.lbl_habitante_vivienda.setText("Seleccione una vivienda de la tabla ->")
        self.tabla_habitantes.setRowCount(0)
        self.limpiar_form_habitante()

        self.group_actividades.setEnabled(False)
        self.tabla_actividades.setRowCount(0)
        self.combo_add_actividad.setCurrentIndex(0)
        self.current_actividad_id = None
        
        # Limpiar filtros al recargar
        self.filtro_viviendas.clear()
        self.filtro_habitantes.clear()
        self.filtro_actividades.clear()

    def limpiar_form_habitante(self):
        self.current_habitante_id = None
        self.txt_habitante_nombre.clear()
        self.txt_habitante_edad.clear()
        self.txt_habitante_sexo.clear()
        self.txt_habitante_parentesco.clear()
        self.tabla_habitantes.clearSelection()

    # --- MÉTODOS DE SELECCIÓN ---
    def seleccionar_vivienda(self, item):
        fila = self.tabla_viviendas.row(item)
        id_vivienda = int(self.tabla_viviendas.item(fila, 0).text())
        direccion = self.tabla_viviendas.item(fila, 1).text()
        nombre_localidad = self.tabla_viviendas.item(fila, 2).text()
        nombre_tipo_vivienda = self.tabla_viviendas.item(fila, 3).text()
        
        self.current_vivienda_id = id_vivienda
        
        # Cargar datos en el formulario
        self.txt_vivienda_direccion.setText(direccion)
        index_loc = self.combo_localidad.findText(nombre_localidad, Qt.MatchContains)
        if index_loc >= 0: self.combo_localidad.setCurrentIndex(index_loc)
        index_tipo = self.combo_tipo_vivienda.findText(nombre_tipo_vivienda, Qt.MatchFixedString)
        if index_tipo >= 0: self.combo_tipo_vivienda.setCurrentIndex(index_tipo)

        # Habilitar secciones
        self.habitante_group.setEnabled(True)
        self.group_actividades.setEnabled(True)
        self.lbl_habitante_vivienda.setText(f"Operaciones para Vivienda ID {id_vivienda}")

        # Cargar datos
        self.cargar_datos_habitantes(id_vivienda)
        self.cargar_datos_actividades(id_vivienda)
        self.limpiar_form_habitante()

    def seleccionar_habitante(self, item):
        fila = self.tabla_habitantes.row(item)
        self.current_habitante_id = int(self.tabla_habitantes.item(fila, 0).text())
        
        self.txt_habitante_nombre.setText(self.tabla_habitantes.item(fila, 1).text())
        self.txt_habitante_edad.setText(self.tabla_habitantes.item(fila, 2).text())
        self.txt_habitante_parentesco.setText(self.tabla_habitantes.item(fila, 3).text())
        
        # Lógica para cargar el sexo (requiere obtener el objeto completo o añadirlo a la tabla)
        # Por simplicidad, lo omitimos del formulario de edición por ahora.

    def seleccionar_actividad(self, item):
        fila = self.tabla_actividades.row(item)
        self.current_actividad_id = int(self.tabla_actividades.item(fila, 0).text())

    # --- MÉTODOS DE CARGA DE DATOS (TABLAS HIJAS) ---
    def cargar_datos_habitantes(self, id_vivienda):
        self.filtro_habitantes.clear() # Limpiar filtro al cambiar de vivienda
        self.tabla_habitantes.setRowCount(0)
        habitantes = self.censo_controller.obtener_habitantes_por_vivienda(id_vivienda)
        for i, hab in enumerate(habitantes):
            self.tabla_habitantes.insertRow(i)
            self.tabla_habitantes.setItem(i, 0, QTableWidgetItem(str(hab.id)))
            self.tabla_habitantes.setItem(i, 1, QTableWidgetItem(hab.nombre_completo))
            self.tabla_habitantes.setItem(i, 2, QTableWidgetItem(str(hab.edad)))
            self.tabla_habitantes.setItem(i, 3, QTableWidgetItem(hab.parentesco_con_jefe_familia))

    def cargar_datos_actividades(self, id_vivienda):
        self.filtro_actividades.clear() # Limpiar filtro
        self.tabla_actividades.setRowCount(0)
        self.current_actividad_id = None
        self.tabla_actividades.clearSelection()

        actividades = self.censo_controller.obtener_actividades_por_vivienda(id_vivienda) 
        for i, act in enumerate(actividades):
            self.tabla_actividades.insertRow(i)
            self.tabla_actividades.setItem(i, 0, QTableWidgetItem(str(act.id)))
            self.tabla_actividades.setItem(i, 1, QTableWidgetItem(act.nombre))

    # --- MÉTODOS CRUD VIVIENDA ---
    def guardar_vivienda(self):
        datos = { "direccion": self.txt_vivienda_direccion.text() }
        id_localidad = self.combo_localidad.currentData()
        id_tipo_vivienda = self.combo_tipo_vivienda.currentData()
        
        if not datos["direccion"] or not id_localidad or not id_tipo_vivienda:
            QMessageBox.warning(self, "Datos Incompletos", "Debe completar todos los campos de la vivienda.")
            return

        if self.current_vivienda_id is None:
            resultado = self.censo_controller.registrar_nueva_vivienda(datos, id_localidad, id_tipo_vivienda)
            mensaje = f"Vivienda registrada con ID {resultado.id}."
        else:
            resultado = self.censo_controller.actualizar_vivienda(
                self.current_vivienda_id, datos, id_localidad, id_tipo_vivienda
            )
            mensaje = f"Vivienda ID {resultado.id} actualizada."
        
        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.cargar_tabla_viviendas()
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la vivienda.")

    def eliminar_vivienda(self):
        if self.current_vivienda_id is None:
            QMessageBox.warning(self, "Sin Selección", "Seleccione una vivienda de la tabla para eliminar.")
            return
        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea eliminar la vivienda ID {self.current_vivienda_id}?\nADVERTENCIA: Se eliminarán TODOS sus habitantes y asociaciones.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmar == QMessageBox.Yes:
            exito = self.censo_controller.eliminar_vivienda(self.current_vivienda_id)
            if exito:
                QMessageBox.information(self, "Eliminado", "La vivienda y sus habitantes han sido eliminados.")
                self.cargar_tabla_viviendas()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la vivienda.")

    # --- MÉTODOS CRUD HABITANTE ---
    def guardar_habitante(self):
        if self.current_vivienda_id is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar una vivienda de la tabla primero.")
            return
            
        try:
            # Validar edad como entero
            if not self.txt_habitante_edad.text():
                 QMessageBox.warning(self, "Dato Inválido", "La edad no puede estar vacía.")
                 return
            edad = int(self.txt_habitante_edad.text())
        except ValueError:
            QMessageBox.warning(self, "Dato Inválido", "La edad debe ser un número entero.")
            return

        datos = {
            "nombre_completo": self.txt_habitante_nombre.text(),
            "edad": edad,
            "sexo": self.txt_habitante_sexo.text(),
            "parentesco_con_jefe_familia": self.txt_habitante_parentesco.text()
        }

        if not datos["nombre_completo"] or not datos["sexo"] or not datos["parentesco_con_jefe_familia"]:
            QMessageBox.warning(self, "Datos Incompletos", "Nombre, Sexo y Parentesco son obligatorios.")
            return

        if self.current_habitante_id is None:
            resultado = self.censo_controller.registrar_habitante_en_vivienda(self.current_vivienda_id, datos)
            mensaje = f"Habitante '{resultado.nombre_completo}' registrado."
        else:
            resultado = self.censo_controller.actualizar_habitante(self.current_habitante_id, datos)
            mensaje = f"Habitante '{resultado.nombre_completo}' actualizado."

        if resultado:
            QMessageBox.information(self, "Éxito", mensaje)
            self.cargar_datos_habitantes(self.current_vivienda_id)
            self.limpiar_form_habitante()
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar al habitante.")

    def eliminar_habitante(self):
        if self.current_habitante_id is None:
            QMessageBox.warning(self, "Sin Selección", "Seleccione un habitante de la tabla para eliminar.")
            return
        
        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea eliminar al habitante ID {self.current_habitante_id}?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmar == QMessageBox.Yes:
            exito = self.censo_controller.eliminar_habitante(self.current_habitante_id)
            if exito:
                QMessageBox.information(self, "Eliminado", "El habitante ha sido eliminado.")
                self.cargar_datos_habitantes(self.current_vivienda_id)
                self.limpiar_form_habitante()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar al habitante.")

    # --- MÉTODOS M:M ACTIVIDAD ---
    def asociar_actividad(self):
        if self.current_vivienda_id is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar una vivienda.")
            return
            
        id_actividad = self.combo_add_actividad.currentData()
        if not id_actividad:
            QMessageBox.warning(self, "Error", "Debe seleccionar una actividad del combo para añadir.")
            return

        exito = self.censo_controller.asociar_actividad_a_vivienda(
            self.current_vivienda_id, id_actividad
        )
        
        if exito:
            QMessageBox.information(self, "Éxito", "Actividad asociada a la vivienda.")
            self.cargar_datos_actividades(self.current_vivienda_id)
            self.combo_add_actividad.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", "No se pudo asociar la actividad (posiblemente ya existía).")

    def desasociar_actividad(self):
        if self.current_vivienda_id is None or self.current_actividad_id is None:
            QMessageBox.warning(self, "Error", "Debe seleccionar una vivienda Y una actividad de la tabla inferior para eliminar.")
            return

        confirmar = QMessageBox.question(self, "Confirmar Eliminación",
                                         f"¿Seguro desea quitar esta actividad de la vivienda?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if confirmar == QMessageBox.Yes:
            exito = self.censo_controller.desasociar_actividad_de_vivienda(
                self.current_vivienda_id, self.current_actividad_id
            )
            
            if exito:
                QMessageBox.information(self, "Eliminado", "La actividad ha sido desasociada de la vivienda.")
                self.cargar_datos_actividades(self.current_vivienda_id)
            else:
                QMessageBox.critical(self, "Error", "No se pudo desasociar la actividad.")