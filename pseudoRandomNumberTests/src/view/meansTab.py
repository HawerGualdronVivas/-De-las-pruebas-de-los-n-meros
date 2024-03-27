from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont

class MeansTab(QWidget):
    """
    Clase para la pestaña de la prueba de medias.

    Esta clase crea la interfaz de usuario y los elementos relacionados con la prueba de medias.

    Args:
        main_window (MainWindow): Referencia a la ventana principal de la aplicación.

    Methods:
        initUI(): Inicializa la interfaz de usuario y los elementos relacionados con la prueba de medias.
        load_data_to_table(data): Carga los datos en la tabla de la interfaz de usuario.
    """

    def __init__(self, main_window):
        """
        Inicializa la pestaña de la prueba de medias.

        Args:
            main_window (MainWindow): Referencia a la ventana principal de la aplicación.
        """
        super().__init__()
        self.main_window = main_window  # Referencia a la ventana MainWindow
        self.initUI()

    def initUI(self):
        """
        Inicializa la interfaz de usuario y los elementos relacionados con la prueba de medias.
        """
        label_text = "PRUEBA DE MEDIAS"
        label = QLabel(label_text)

        # Crear una fuente en negrita para el título
        font = QFont()
        font.setBold(True)
        label.setFont(font)

        self.status = QLabel("Estado de la prueba:")
        # Crear una fuente en negrita para el estado
        font_status = QFont()
        font_status.setBold(True)
        self.status.setFont(font_status)

        self.ls = QLabel("Valor Limite Superior:")
        self.mean = QLabel("Valor Media:")
        self.li = QLabel("Valor Limite Inferior: ")
        self.test = QPushButton("Pobar Datos")
        self.g = QPushButton("Ver Limites y Media")

        self.test.clicked.connect(self.main_window.doAverageTest)
        self.g.clicked.connect(self.main_window.showAverageTestG)
        
        # Crear tabla con scroll
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Dos columnas: No y Ri
        self.table.verticalHeader().setVisible(False)  # Oculta el número de fila
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)  # La última sección se expande automáticamente
        self.table.setHorizontalHeaderLabels(["No", "Ri"])

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.table)
        layout.addWidget(self.status)
        layout.addWidget(self.ls)
        layout.addWidget(self.mean)
        layout.addWidget(self.li)
        layout.addWidget(self.test)
        layout.addWidget(self.g)
        self.setLayout(layout)

    def load_data_to_table(self, data):
        """
        Carga los datos en la tabla de la interfaz de usuario.

        Args:
            data (list): Lista de tuplas que contienen los datos a cargar en la tabla.
                Cada tupla contiene el número de fila y el valor de Ri correspondiente.
        """
        self.table.setRowCount(len(data))
        for row, (no, ri) in enumerate(data):
            item_no = QTableWidgetItem(str(no))
            item_ri = QTableWidgetItem(str(ri))
            self.table.setItem(row, 0, item_no)
            self.table.setItem(row, 1, item_ri)
