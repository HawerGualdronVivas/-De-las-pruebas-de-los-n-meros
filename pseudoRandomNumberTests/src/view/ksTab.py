from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QDoubleValidator, QFont

class KsTab(QWidget):
    """
    Clase para la pestaña de la prueba de Kolmogorov-Smirnov.

    Esta clase crea la interfaz de usuario y los elementos relacionados con la prueba de Kolmogorov-Smirnov.

    Args:
        main_window (MainWindow): Referencia a la ventana principal de la aplicación.

    Methods:
        initUI(): Inicializa la interfaz de usuario y los elementos relacionados con la prueba de Kolmogorov-Smirnov.
        load_data_to_table(data): Carga los datos en la tabla de la interfaz de usuario.
    """

    def __init__(self, main_window):
        """
        Inicializa la pestaña de la prueba de Kolmogorov-Smirnov.

        Args:
            main_window (MainWindow): Referencia a la ventana principal de la aplicación.
        """
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        """
        Inicializa la interfaz de usuario y los elementos relacionados con la prueba de Kolmogorov-Smirnov.
        """
        label_text = "PRUEBA Kolmogorov-Smirnov"
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

        self.mean = QLabel("Promedio de los datos:")
        self.d_max = QLabel("Valor del D_max:")
        self.d_max_p = QLabel("Valor del d_max_p: ")
        self.test = QPushButton("Pobar Datos")
        self.n = QLabel("Numero de intervalos Por defecto 8:")
        self.g = QPushButton("Ver Grafica d_max y d_max_p")
        self.g2 = QPushButton("Ver Grafica de probabilidad de todos los Intervalos")
        self.g3 = QPushButton("Ver Grafica frecuencia de los intervalos")
        self.test.clicked.connect(self.main_window.doKsTest)
        self.g.clicked.connect(self.main_window.showKsTestG)
        self.g2.clicked.connect(self.main_window.showKsTestG2)
        self.g3.clicked.connect(self.main_window.showKsTestG3)

        # Crear tabla con scroll
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Dos columnas: No y Ri
        self.table.verticalHeader().setVisible(False)  # Oculta el número de fila
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)  # La última sección se expande automáticamente
        self.table.setHorizontalHeaderLabels(["No", "Ri"])

        self.intervals = QLabel("Insertar Intervalos por defecto 10:")
        self.intervalsNum = QLineEdit()
        double_validator = QDoubleValidator()
        self.intervalsNum.setValidator(double_validator)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.table)
        layout.addWidget(self.intervals)
        layout.addWidget(self.intervalsNum)
        layout.addWidget(self.status)
        layout.addWidget(self.mean)
        layout.addWidget(self.d_max)
        layout.addWidget(self.d_max_p)
        layout.addWidget(self.test)
        layout.addWidget(self.g3)
        layout.addWidget(self.g)
        layout.addWidget(self.g2)
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
