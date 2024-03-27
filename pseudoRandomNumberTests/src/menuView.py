import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QMessageBox, QSpacerItem, QSizePolicy, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from view.view import MainWindow
from controller.presenter import Presenter
import os

class PruebasNumerosApp(QMainWindow):
    def __init__(self, file=None):
        super().__init__()
        self.file = file #Archivo seleccionado para las pruebas
        self.setWindowTitle("Pruebas de los números")  # Título de la ventana
        self.setFixedSize(300, 400) # Tamaño fijo de la ventana

        # QLabel para mostrar la imagen de fondo
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 300, 400)

        # Obtener la ruta absoluta del directorio actual
        current_directory = os.path.dirname(__file__)

        # Construir la ruta relativa a la imagen    
        image_path = os.path.join(current_directory, 'background.png')

        # Cargar la imagen de fondo
        try:
            pixmap = QPixmap(image_path)  # Usando una ruta relativa
            if pixmap.isNull():
                raise FileNotFoundError("No se puede cargar la imagen.")
            self.background_label.setPixmap(pixmap)
            self.background_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        except Exception as e:
            print(f"Error: {e}")

        # Configuración del diseño de la ventana
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Botón para salir de la aplicación
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.salir)
        self.layout.addWidget(self.boton_salir, alignment=Qt.AlignmentFlag.AlignLeft)

        # Espaciador superior para organizar la informacion
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer_top)

        # Ancho fijo de los botones de las pruebas
        self.button_width = 150  # Modificamos el ancho de los botones de las pruebas

        # Botones para las pruebas
        self.boton_medias = QPushButton("Prueba de medias", self)
        self.boton_medias.clicked.connect(self.prueba_medias)
        self.boton_medias.setFixedWidth(self.button_width)
        self.layout.addWidget(self.boton_medias, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boton_varianza = QPushButton("Prueba de varianza", self)
        self.boton_varianza.clicked.connect(self.prueba_varianza)
        self.boton_varianza.setFixedWidth(self.button_width)
        self.layout.addWidget(self.boton_varianza, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boton_ks = QPushButton("Prueba KS", self)
        self.boton_ks.clicked.connect(self.prueba_ks)
        self.boton_ks.setFixedWidth(self.button_width)
        self.layout.addWidget(self.boton_ks, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boton_chi2 = QPushButton("Prueba Chi2", self)
        self.boton_chi2.clicked.connect(self.prueba_chi2)
        self.boton_chi2.setFixedWidth(self.button_width)
        self.layout.addWidget(self.boton_chi2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.boton_poker = QPushButton("Prueba de Poker", self)
        self.boton_poker.clicked.connect(self.prueba_poker)
        self.boton_poker.setFixedWidth(self.button_width)
        self.layout.addWidget(self.boton_poker, alignment=Qt.AlignmentFlag.AlignCenter)

        # Espaciador inferior para organizar la informacion
        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer_bottom)

        # Deshabilita el botón de cierre (X)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)  # Deshabilitar el botón de cierre (X)

    def prueba_medias(self):
        """
        Función para realizar la prueba de medias.
        Cierra la ventana actual y abre una nueva ventana para la prueba de medias.
        """
        self.close()
        # Crear una instancia del presentador de la aplicación
        presenter = Presenter()
        # Crear una instancia de la ventana principal de la aplicación
        main_window = MainWindow(presenter, 0, self.file)
        # Establecer la referencia a la ventana principal en el presentador
        presenter.set_main_window(main_window)
        # Mostrar la ventana principal
        main_window.show()

    def prueba_varianza(self):
        """
        Función para realizar la prueba de varianza.
        Cierra la ventana actual y abre una nueva ventana para la prueba de medias.
        """
        self.close()
        # Crear una instancia del presentador de la aplicación
        presenter = Presenter()
        # Crear una instancia de la ventana principal de la aplicación
        main_window = MainWindow(presenter, 1, self.file)
        # Establecer la referencia a la ventana principal en el presentador
        presenter.set_main_window(main_window)
        # Mostrar la ventana principal
        main_window.show()

    def prueba_ks(self):
        """
        Función para realizar la prueba de KS.
        Cierra la ventana actual y abre una nueva ventana para la prueba de medias.
        """
        self.close()
        # Crear una instancia del presentador de la aplicación
        presenter = Presenter()
        # Crear una instancia de la ventana principal de la aplicación
        main_window = MainWindow(presenter, 3, self.file)
        # Establecer la referencia a la ventana principal en el presentador
        presenter.set_main_window(main_window)
        # Mostrar la ventana principal
        main_window.show()

    def prueba_chi2(self):
        """
        Función para realizar la prueba de Chi2.
        Cierra la ventana actual y abre una nueva ventana para la prueba de medias.
        """
        self.close()
        # Crear una instancia del presentador de la aplicación
        presenter = Presenter()
        # Crear una instancia de la ventana principal de la aplicación
        main_window = MainWindow(presenter, 2, self.file)
        # Establecer la referencia a la ventana principal en el presentador
        presenter.set_main_window(main_window)
        # Mostrar la ventana principal
        main_window.show()

    def prueba_poker(self):
        """
        Función para realizar la prueba de poker.
        Cierra la ventana actual y abre una nueva ventana para la prueba de medias.
        """
        self.close()
        # Crear una instancia del presentador de la aplicación
        presenter = Presenter()
        # Crear una instancia de la ventana principal de la aplicación
        main_window = MainWindow(presenter, 4, self.file)
        # Establecer la referencia a la ventana principal en el presentador
        presenter.set_main_window(main_window)
        # Mostrar la ventana principal
        main_window.show()

    def salir(self):
        """
        Función para salir de la aplicación.
        Muestra un cuadro de diálogo de confirmación antes de cerrar la aplicación.
        """
        reply = QMessageBox.question(self, "Pruebas de los números", "¿Estás seguro que quieres salir?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PruebasNumerosApp()
    ventana.show()
    sys.exit(app.exec())
