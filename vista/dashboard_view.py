from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QApplication, QMessageBox, QStyle
from PyQt5.QtGui import QIcon

# Importamos los QWidget que actuarán como pestañas
from .reports_widget import ReportsWidget
from .catalogo_widget import CatalogoWidget
from .censo_widget import CensoWidget
from .asistente_widget import AsistenteWidget

class DashboardView(QMainWindow):
    """
    Ventana principal de la aplicación (Dashboard).
    Contiene QTabWidget para la navegación (Requisito 3) y el menú de cierre.
    """
    def __init__(self, catalogo_controller, censo_controller, asistente_controller):
        super().__init__()
        
        self.catalogo_controller = catalogo_controller
        self.censo_controller = censo_controller
        self.asistente_controller = asistente_controller
        
        self.setWindowTitle("Dashboard - Censo de Población INEGI")
        self.setGeometry(100, 100, 950, 700) # Ventana principal más grande
        
        self.setup_ui()
        self.crear_menu() # Requisito 3: Menú para navegar/cerrar

    def setup_ui(self):
        """Configura la interfaz principal con pestañas (Navegación)."""
        
        # 1. Crear el contenedor de pestañas (Navegación)
        self.tab_widget = QTabWidget()
        
        # 2. Crear las pestañas individuales (cada una es un QWidget)
        
        # Pestaña 1: Reportes
        self.reports_tab = ReportsWidget(self.censo_controller, self.catalogo_controller)
        
        # Pestaña 2: Operaciones del Censo
        self.censo_tab = CensoWidget(self.censo_controller, self.catalogo_controller)
        
        # Pestaña 3: CRUD de Catálogos
        self.catalogo_tab = CatalogoWidget(self.catalogo_controller)

        # Pestaña 4: Asistente IA
        self.asistente_tab = AsistenteWidget(self.asistente_controller)

        # --- 3. CONEXIÓN DE SEÑAL ENTRE PESTAÑAS ---
        # Conecta la señal 'catalogos_actualizados' de la pestaña de catálogos
        # al slot (método) 'poblar_comboboxes' de la pestaña del censo.
        # Esto asegura que CensoWidget vea los nuevos catálogos sin reiniciar.
        self.catalogo_tab.catalogos_actualizados.connect(self.censo_tab.poblar_comboboxes)
        
        # 4. Añadir las pestañas al contenedor (con Iconos)
        style = self.style() # Obtener el estilo actual de la UI

        # Icono de Gráfico/Reporte
        icon_reports = QIcon(style.standardPixmap(QStyle.SP_FileDialogDetailedView))
        self.tab_widget.addTab(self.reports_tab, icon_reports, "Dashboard y Reportes")
        
        # Icono de Censo/Formulario
        icon_censo = QIcon(style.standardPixmap(QStyle.SP_FileIcon))
        self.tab_widget.addTab(self.censo_tab, icon_censo, "Operaciones del Censo")
        
        # Icono de Catálogo/Configuración
        icon_catalogo = QIcon(style.standardPixmap(QStyle.SP_ToolBarHorizontalExtensionButton))
        self.tab_widget.addTab(self.catalogo_tab, icon_catalogo, "Administración de Catálogos")
        
        # Icono de Asistente/IA
        icon_asistente = QIcon(style.standardPixmap(QStyle.SP_MessageBoxInformation))
        self.tab_widget.addTab(self.asistente_tab, icon_asistente, "Asistente IA")
        
        # 5. Establecer el QTabWidget como el widget central
        self.setCentralWidget(self.tab_widget)

    def crear_menu(self):
        """Crea la barra de menú principal (Requisito 3)."""
        menubar = self.menuBar()
        
        # Menú "Archivo"
        archivo_menu = menubar.addMenu("&Archivo")
        
        # Acción "Cerrar Sistema"
        exit_action = QAction(QIcon(), "&Cerrar Sistema", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Cierra la aplicación")
        # Conecta la acción a 'self.close' que cierra la QMainWindow
        exit_action.triggered.connect(self.close) 
        
        archivo_menu.addAction(exit_action)

    def closeEvent(self, event):
        """Sobreescribe el evento de cierre para confirmación."""
        reply = QMessageBox.question(self, 'Confirmar Salida',
                                     "¿Está seguro de que desea cerrar el sistema?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # (Aquí iría la lógica de destruir variables de sesión si existieran)
            event.accept() # Cierra la aplicación
        else:
            event.ignore() # Cancela el cierre