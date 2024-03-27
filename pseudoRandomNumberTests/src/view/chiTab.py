from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QSizePolicy, QGridLayout
from PyQt6.QtGui import QDoubleValidator, QFont

class ChiTab(QWidget):
    """
    Clase para la pestaña de la prueba de chi-cuadrado.

    Esta clase crea la interfaz de usuario y los elementos relacionados con la prueba de chi-cuadrado.

    Args:
        main_window (MainWindow): Referencia a la ventana principal de la aplicación.

    Methods:
        initUI(): Inicializa la interfaz de usuario y los elementos relacionados con la prueba de chi-cuadrado.
        load_data_to_table(data): Carga los datos en la tabla de la interfaz de usuario.
    """

    def __init__(self, main_window):
        """
        Inicializa la pestaña de la prueba de chi-cuadrado.

        Args:
            main_window (MainWindow): Referencia a la ventana principal de la aplicación.
        """
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        """
        Inicializa la interfaz de usuario y los elementos relacionados con la prueba de chi-cuadrado.
        """
        label = QLabel("PRUEBA CHI-CUADRADO")

        # Crear una fuente en negrita para el título
        font = QFont()
        font.setBold(True)
        label.setFont(font)

        self.status = QLabel("Estado de la prueba:")
        # Crear una fuente en negrita para el estado
        font_status = QFont()
        font_status.setBold(True)
        self.status.setFont(font_status)

        self.ni_min = QLabel("Valor Ni Maximo:")
        self.ni_max = QLabel("Valor Ni Minimo: ")
        self.test = QPushButton("Pobar Datos")
        self.n = QLabel("Numero de intervalos:")
        self.g = QPushButton("Ver Grafica Suma Chi2 y Chi2Inversa calculada")
        self.g2 = QPushButton("Ver Grafica frecuencia de los intervalos")
        self.test.clicked.connect(self.main_window.doChi2Test)
        self.g.clicked.connect(self.main_window.showChi2TestG)
        self.g2.clicked.connect(self.main_window.showChi2TestG2)

        # Crear tabla con scroll
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Dos columnas: No y Ri
        self.table.verticalHeader().setVisible(False)  # Oculta el número de fila
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)  # La última sección se expande automáticamente
        self.table.setHorizontalHeaderLabels(["No", "Ri"])

        self.a_label = QLabel("Valor 'a' (Valor mas bajo Ni) por defecto 8:")
        self.b_label = QLabel("Valor 'b' (Valor mas alto Ni) por defecto 10:")
        self.a_input = QLineEdit()
        self.b_input = QLineEdit()
        double_validator = QDoubleValidator()
        self.a_input.setValidator(double_validator)
        self.b_input.setValidator(double_validator)

        self.intervals = QLabel("Insertar Intervalos por defecto 8:")
        self.intervalsNum = QLineEdit()
        
        self.intervalsNum.setValidator(double_validator)
        self.sum_chi2 = QLabel("Valor de la sumatoria de Chi2: ")
        self.chi_test = QLabel("Valor de la prueba Chi2 inversa: ")

        # Ajuste del tamaño de la tabla
        self.table.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.table.setMinimumHeight(20)  # Establecer una altura mínima para la tabla

        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(self.intervals, 2, 0)
        layout.addWidget(self.intervalsNum, 2, 1)
        layout.addWidget(self.a_label, 3, 0)
        layout.addWidget(self.a_input, 3, 1)
        layout.addWidget(self.b_label, 4, 0)
        layout.addWidget(self.b_input, 4, 1)
        layout.addWidget(self.n, 7, 0)
        layout.addWidget(self.ni_max, 8, 0)
        layout.addWidget(self.ni_min, 9, 0)
        layout.addWidget(self.sum_chi2, 10, 0)
        layout.addWidget(self.chi_test, 11, 0)
        layout.addWidget(self.status, 12, 0)
        layout.addWidget(self.g, 13, 0)
        layout.addWidget(self.g2, 14, 0)
        layout.addWidget(self.test, 15, 0)
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
