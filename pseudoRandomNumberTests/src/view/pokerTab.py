from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt6.QtGui import QDoubleValidator, QFont

class PokerTab(QWidget):
    """
    Clase para la pestaña de la prueba de Poker.

    Esta clase crea la interfaz de usuario y los elementos relacionados con la prueba de Poker.

    Args:
        main_window (MainWindow): Referencia a la ventana principal de la aplicación.

    Methods:
        initUI(): Inicializa la interfaz de usuario y los elementos relacionados con la prueba de Poker.
        load_data_to_table(data): Carga los datos en la tabla de la interfaz de usuario.
        load_data_to_table2(data): Carga los datos en la segunda tabla de la interfaz de usuario.
    """

    def __init__(self, main_window):
        """
        Inicializa la pestaña de la prueba de Poker.

        Args:
            main_window (MainWindow): Referencia a la ventana principal de la aplicación.
        """
        super().__init__()
        self.main_window = main_window  # Referencia a la ventana MainWindow
        self.initUI()

    def initUI(self):
        """
        Inicializa la interfaz de usuario y los elementos relacionados con la prueba de Poker.
        """
        label_text = "PRUEBA DE POKER\nDescripción de las manos: (D) Todos Diferentes, (O) Un par, (T) Dos pares, (K) Tercia\n (F) Tercia y Par (Full house), (P) Cuatro del mismo valor (poker), (Q) Quintilla"
        label = QLabel(label_text)

        label_text_second ="Datos Seleccionados:"
        second_label = QLabel(label_text_second)

        # Crear una fuente en negrita para el título
        font = QFont()
        font.setBold(True)
        label.setFont(font)

        self.status = QLabel("Estado de la prueba:")
        # Crear una fuente en negrita para el estado
        font_status = QFont()
        font_status.setBold(True)
        self.status.setFont(font_status)

        self.intervals = QLabel("Definir el tamaño de cada Subconjunto(Por defecto 1000):")
        self.intervalsNum = QLineEdit()

        double_validator = QDoubleValidator()
        self.intervalsNum.setValidator(double_validator)

        self.sum_val = QLabel("Valor de la sumatoria: ")
        self.chi_val = QLabel("Valor de la prueba chi inversa: ")
        self.test = QPushButton("Pobar Datos")
        self.g1 = QPushButton("Ver Gráfica Sumatoria vs Chi Inversa")
        self.g2 = QPushButton("Ver Gráfica Frecuencia de manos")
        self.test.clicked.connect(self.main_window.doPokerTest)
        self.g1.clicked.connect(self.main_window.showGraph1Poker)
        self.g2.clicked.connect(self.main_window.showGraph2Poker)

        # Crear tabla con scroll
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Dos columnas: No y Ri
        self.table.verticalHeader().setVisible(False)  # Oculta el número de fila
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)  # La última sección se expande automáticamente
        self.table.setHorizontalHeaderLabels(["No", "Ri"])

        # Crear una segunda tabla con scroll
        self.table2 = QTableWidget()
        self.table2.setColumnCount(2)  # Dos columnas: Subconjunto y Estado
        self.table2.verticalHeader().setVisible(False)  # Oculta el número de fila
        header2 = self.table2.horizontalHeader()
        header2.setStretchLastSection(True)
        self.table2.setHorizontalHeaderLabels(["Subconjunto", "Estado"])

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.table2)
        layout.addWidget(second_label)
        layout.addWidget(self.table)
        layout.addWidget(self.intervals)
        layout.addWidget(self.intervalsNum)
        layout.addWidget(self.sum_val)
        layout.addWidget(self.chi_val)
        layout.addWidget(self.status)
        layout.addWidget(self.test)
        layout.addWidget(self.g1)
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
    
    def load_data_to_table2(self, data):
        """
        Carga los datos en la segunda tabla de la interfaz de usuario.

        Args:
            data (list): Lista de tuplas que contienen los datos a cargar en la segunda tabla.
                Cada tupla contiene el subconjunto y el estado correspondiente.
        """
        # Establecer el tamaño de la tabla a 2 filas
        self.table2.setRowCount(1)

        # Iterar sobre los primeros dos elementos de data
        for row, (subconjunto, estado) in enumerate(data[:1]):
            item_subconjunto = QTableWidgetItem(subconjunto)
            item_estado = QTableWidgetItem(estado)
            self.table2.setItem(row, 0, item_subconjunto)
            self.table2.setItem(row, 1, item_estado)

        # Ajustar el tamaño de la tabla para que se ajuste al contenido
        self.table2.resizeRowsToContents()

        # Obtener la altura total de las filas
        total_height = self.table2.rowHeight(0) * 2  # Sumar la altura de las dos filas

        # Ajustar la altura de la tabla en función de la altura total de las filas
        self.table2.setFixedHeight(total_height)
        
