import sys
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt  
from PyQt6.QtWidgets import QApplication

# Importaciones de pestañas y clases relacionadas
from .chiTab import ChiTab  # Importa la clase ChiTab desde chiTab.py
from .ksTab import KsTab  # Importa la clase KsTab desde ksTab.py
from .varTab import VarianceTab  # Importa la clase VarianceTab desde varTab.py
from .meansTab import MeansTab  # Importa la clase MeansTab desde meansTab.py
from .pokerTab import PokerTab  # Importa la clase PokerTab desde pokerTab.py
from controller.presenter import Presenter
from model.poker_test import PokerTest
from model.average_test import AverageTest
from model.variance_test import VarianceTest
from model.ks_test import KsTest
from model.chi2_test import ChiTest

class MainWindow(QMainWindow):
    """
    Clase para la ventana principal de la aplicación.

    Esta clase crea la ventana principal de la aplicación y gestiona las pestañas y eventos relacionados con las pruebas estadísticas.

    Args:
        presenter (Presenter): Una instancia del presentador que gestiona la lógica de la aplicación.

    Attributes:
        poker_tab (PokerTab): La pestaña para la prueba de Poker.
        means_tab (MeansTab): La pestaña para la prueba de medias.
        variance_tab (VarianceTab): La pestaña para la prueba de varianzas.
        ks_tab (KsTab): La pestaña para la prueba de Kolmogorov-Smirnov.
        chi_tab (ChiTab): La pestaña para la prueba de chi-cuadrado.
        passed_data (list): Lista para almacenar los datos que han pasado la prueba.

    Methods:
        initUI(): Inicializa la interfaz de usuario y los elementos relacionados con las pestañas y botones.
        loadFile(): Abre un cuadro de diálogo para cargar un archivo de datos.
        showErrorMessage(title, message): Muestra un cuadro de mensaje de error.
        doPokerTest(): Realiza la prueba de Poker con los datos cargados.
        showGraph1Poker(): Muestra la gráfica de sumatoria vs. chi inversa para la prueba de Poker.
        showGraph2Poker(): Muestra la gráfica de frecuencia observada vs. frecuencia esperada para la prueba de Poker.
        doAverageTest(): Realiza la prueba de medias con los datos cargados.
        showAverageTestG(): Muestra la gráfica de límites y media para la prueba de medias.
        doVarianceTest(): Realiza la prueba de varianzas con los datos cargados.
        showVarianceTestG(): Muestra la gráfica de límites y varianza para la prueba de varianzas.
        doKsTest(): Realiza la prueba de Kolmogorov-Smirnov con los datos cargados.
        showKsTestG(): Muestra la gráfica de D_max para la prueba de Kolmogorov-Smirnov.
        showKsTestG2(): Muestra la gráfica de probabilidad de los intervalos para la prueba de Kolmogorov-Smirnov.
        showKsTestG3(): Muestra la gráfica de frecuencia de los intervalos para la prueba de Kolmogorov-Smirnov.
        doChi2Test(): Realiza la prueba de chi-cuadrado con los datos cargados.
        showChi2TestG(): Muestra la gráfica de valores Chi2 calculados.
        showChi2TestG2(): Muestra la gráfica de frecuencias observadas para la prueba de chi-cuadrado.
    """

    def __init__(self, presenter, test_option, archivo_seleccionado):
        # Guardar archivo_seleccionado como un atributo de la instancia
        self.archivo_seleccionado = archivo_seleccionado  
        # Una instancia del presentador que gestiona la lógica de la aplicación
        self.presenter = presenter
        # Opción de prueba seleccionada por el usuario
        self.test_option = test_option
        # Lista para almacenar los datos que han pasado la prueba
        self.passed_data = []  
        # Inicializar la interfaz de usuario
        self.initUI(test_option)

    def initUI(self, test_option):
        """
        Inicializa la interfaz de usuario y los elementos relacionados con las pestañas y botones.
        """
        self.setWindowTitle("Number tests")
        self.setGeometry(100, 100, 500, 400)
        self.setFixedSize(500, 600)  # Establecer un tamaño fijo para la ventana
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)  # Desactivar el botón de cerrar
        
        # Crear un widget de pestañas
        tab_widget = QTabWidget()

        # Crear las pestañas correspondientes a las pruebas
        self.poker_tab = PokerTab(self) 
        self.means_tab = MeansTab(self)
        self.variance_tab = VarianceTab(self)
        self.ks_tab = KsTab(self)
        self.chi_tab = ChiTab(self)

        # Agregar las pestañas al widget de pestañas según la opción de prueba seleccionada
        tab_widget = QTabWidget()
        tabs = [self.means_tab, self.variance_tab, self.chi_tab, self.ks_tab, self.poker_tab]
        tab_labels = ["Means Test", "Variance Test", "Chi2 Test", "K-S Test", "Poker Test"]
        if 0 <= test_option < len(tabs):
            tab_widget.addTab(tabs[test_option], tab_labels[test_option])

        # Configurar el diseño vertical
        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        
        # Botones de la interfaz de usuario
        self.load_button = QPushButton("Importar datos", self)
        self.load_button.clicked.connect(self.loadFile)
        vbox.addWidget(self.load_button)

        self.export_button = QPushButton("Exportar datos", self)
        self.export_button.clicked.connect(self.exportData)
        vbox.addWidget(self.export_button)

        self.back_button = QPushButton("Atrás", self)
        self.back_button.clicked.connect(self.backToMenu)
        vbox.addWidget(self.back_button)

        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)

        # Valida si hay un archivo previo cargado
        if self.archivo_seleccionado is not None:
            self.loadSelectedFile(self.archivo_seleccionado)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
    
    def backToMenu(self):
         # Cierra la ventana actual
        self.close()
        # Muestra la instancia existente de PruebasNumerosApp
        from menuView import PruebasNumerosApp
        self.menu_view = PruebasNumerosApp(self.archivo_seleccionado)
        self.menu_view.show()
    
        

    def loadFile(self):
        """
        Abre un cuadro de diálogo para cargar un archivo de datos.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Archivos de Texto (*.txt);;Todos los Archivos (*)")
        if file_name:
            self.presenter.file_manager.input_file_path = file_name
            self.presenter.file_manager.storage_numbers()
            self.presenter.add_numbers()
            self.status_label.setText(f"File Selected: {file_name}")
            self.archivo_seleccionado = file_name
    
    def loadSelectedFile(self, file_name):
        if file_name:
            # Actualiza la ruta del archivo seleccionado
            self.presenter.file_manager.input_file_path = file_name
            self.presenter.file_manager.storage_numbers()
            self.presenter.add_numbers()
            self.status_label.setText(f"File Selected: {file_name}")
            self.archivo_seleccionado = file_name

    def showErrorMessage(self, title, message):
        """
        Muestra un cuadro de mensaje de error.

        Args:
            title (str): El título del mensaje de error.
            message (str): El contenido del mensaje de error.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    # Eventos de prueba de medias
    def doAverageTest(self): 
        """
        Realiza la prueba de medias y actualiza la interfaz de usuario con los resultados.

        Se verifica si hay datos disponibles para realizar la prueba de medias. Si hay datos,
        se realiza la prueba y se actualiza la interfaz de usuario con los resultados.
        Si la prueba pasa, se muestra un mensaje indicando que los datos pasaron la prueba.
        Si la prueba no pasa y la cantidad de datos es mayor que 1000, se realiza la prueba en
        subconjuntos de 1000 datos y se actualiza la interfaz de usuario con el número total
        de datos que pasaron la prueba de medias. Si no se pasa ninguna prueba, se muestra un
        mensaje indicando que los datos no pasaron la prueba.

        """
        if len(self.presenter.ri_numbers) != 0:
                #Se crea una copia de los datos
                all_data = self.presenter.ri_numbers.copy()
                test = AverageTest(self.presenter.ri_numbers)
                self.presenter.average_test = test
                self.presenter.do_average_test()
                if self.presenter.average_test.passed:
                    self.means_tab.status.setText(f"Estado de la prueba: El set de datos seleccionado PASÓ la prueba satisfactoriamente")
                elif not self.presenter.average_test.passed and len(self.presenter.ri_numbers) > 1000:
                    num_passedTwo = 0  # Inicializar contador de datos pasados

                    num_iterations = len(self.presenter.ri_numbers) // 1000
                    for i in range(num_iterations):
                        start_index = i * 1000
                        end_index = (i + 1) * 1000

                        subset_data = all_data[start_index:end_index]

                        self.presenter.ri_numbers = subset_data

                        test = AverageTest(subset_data)
                        self.presenter.average_test = test
                        self.presenter.do_average_test()
                        if self.presenter.average_test.passed:
                            for value in subset_data:
                                self.passed_data.append(value)
                        # Actualizar contador de datos pasados
                        num_passedTwo += len(subset_data)
                    if len(self.passed_data) > 0:
                        num_passedOne = len(self.passed_data)
                        self.means_tab.status.setText(f"Estado de la prueba: Pasaron {num_passedOne} de {num_passedTwo} Datos")
                    else:
                        self.means_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")
                else:
                    self.means_tab.status.setText(f"Estado de la prueba: El set de Datos no pasó la prueba") 
                self.means_tab.ls.setText(f"Valor Limite Superior: {self.presenter.average_test.superior_limit}")
                self.means_tab.mean.setText(f"Valor Media: {self.presenter.average_test.average}")
                self.means_tab.li.setText(f"Valor Limite Inferior: {self.presenter.average_test.inferior_limit}")

                # Llenar la tabla con los datos de self.presenter.ri_numbers
                data = [(i + 1, ri) for i, ri in enumerate(all_data)]
                self.means_tab.load_data_to_table(data)

    def showAverageTestG(self):
        """
        Muestra la gráfica de límites y media para la prueba de medias.
        """
        self.presenter.average_test.plotLimitsAndAverage()

    # Eventos de prueba de varianzas
    def doVarianceTest(self):
        """
        Realiza la prueba de varianzas con los datos cargados.
        """
        if len(self.presenter.ri_numbers) != 0:
            #Se crea una copia de los datos
            all_data = self.presenter.ri_numbers.copy()  
            self.presenter.variance_test = VarianceTest(self.presenter.ri_numbers)
            self.presenter.do_variance_test()
            if self.presenter.variance_test.passed:
                self.variance_tab.status.setText(f"Estado de la prueba: El set de datos seleccionado PASÓ la prueba satisfactoriamente")
            elif not self.presenter.variance_test.passed and len(self.presenter.ri_numbers) > 1000:  
                num_passedTwo = 0  # Inicializar contador de datos pasados

                num_iterations = len(self.presenter.ri_numbers) // 1000
                for i in range(num_iterations):
                    start_index = i * 1000
                    end_index = (i + 1) * 1000

                    subset_data = all_data[start_index:end_index]

                    self.presenter.ri_numbers = subset_data

                    self.presenter.variance_test = VarianceTest(subset_data)
                    self.presenter.do_variance_test()
                    if self.presenter.variance_test.passed:
                        for value in subset_data:
                            self.passed_data.append(value)
                    # Actualizar contador de datos pasados
                    num_passedTwo += len(subset_data)
                if len(self.passed_data) > 0:
                    num_passedOne = len(self.passed_data)
                    self.variance_tab.status.setText(f"Estado de la prueba: Pasaron {num_passedOne} de {num_passedTwo} Datos")
                else:
                    self.variance_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba") 
            else:
                self.variance_tab.status.setText(f"Estado de la prueba: El set de Datos no pasó la prueba") 
            self.variance_tab.ls.setText(f"Valor Limite Superior: {self.presenter.variance_test.superior_limit}")
            self.variance_tab.variance.setText(f"Valor Varianza: {self.presenter.variance_test.variance}")
            self.variance_tab.li.setText(f"Valor Limite Inferior: {self.presenter.variance_test.inferior_limit}")

            # Llenar la tabla con los datos de self.presenter.ri_numbers
            data = [(i + 1, ri) for i, ri in enumerate(all_data)]
            self.variance_tab.load_data_to_table(data)
    
    def exportData(self):
        if self.passed_data:  # Verificar si passed_data no está vacía
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar datos", "", "Archivos de Texto (*.txt);;Todos los Archivos (*)")
            if file_name:
                with open(file_name, 'w') as f:
                    for number in self.passed_data:
                        f.write(str(number) + '\n')
                QMessageBox.information(self, "Datos exportados", "Los datos han sido exportados exitosamente.")
        else:
            QMessageBox.warning(self, "No hay datos para exportar", "No hay datos aprobados para exportar.")
        


    def showVarianceTestG(self):
        """
        Muestra la gráfica de límites y varianza para la prueba de varianzas.
        """
        self.presenter.variance_test.plotLimitsAndVariance()

    # Eventos de prueba de Kolmogorov-Smirnov
    def doKsTest(self):
        """
        Realiza la prueba de Kolmogorov-Smirnov con los datos cargados.
        """
        if len(self.presenter.ri_numbers) != 0:
            # Se crea una copia de los datos
            all_data = self.presenter.ri_numbers.copy()
            if self.ks_tab.intervalsNum.text() != "":
                self.presenter.ks_test = KsTest(self.presenter.ri_numbers, int(self.ks_tab.intervalsNum.text()))
            else:
                self.presenter.ks_test = KsTest(self.presenter.ri_numbers)
            self.presenter.do_ks_test()

            if self.presenter.ks_test.passed:
                self.ks_tab.status.setText(f"Estado de la prueba: El set de datos seleccionado PASÓ la prueba satisfactoriamente")

            elif not self.presenter.variance_test.passed and len(self.presenter.ri_numbers) > 1000: 
                num_passedTwo = 0  # Inicializar contador de datos pasados
                num_iterations = len(self.presenter.ri_numbers) // 1000
                for i in range(num_iterations):
                    start_index = i * 1000
                    end_index = (i + 1) * 1000

                    subset_data = all_data[start_index:end_index]

                    self.presenter.ri_numbers = subset_data

                    if self.ks_tab.intervalsNum.text() != "":
                        self.presenter.ks_test = KsTest(subset_data.copy(), int(self.ks_tab.intervalsNum.text()))
                    else:
                        self.presenter.ks_test = KsTest(subset_data.copy())
                        
                    self.presenter.do_ks_test()

                    if self.presenter.ks_test.passed:

                        for value in subset_data:
                            self.passed_data.append(value)
                    # Actualizar contador de datos pasados
                    num_passedTwo += len(subset_data)
                if len(self.passed_data) > 0:
                    num_passedOne = len(self.passed_data)
                    self.ks_tab.status.setText(f"Estado de la prueba: Pasaron {num_passedOne} de {num_passedTwo} Datos")
                else:
                    self.ks_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")
            else:
                self.ks_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")
            self.ks_tab.mean.setText(f"Promedio de los datos: {self.presenter.ks_test.average}")
            self.ks_tab.d_max.setText(f"Valor del D_max: {self.presenter.ks_test.d_max}")
            self.ks_tab.d_max_p.setText(f"Valor del d_max_p: {self.presenter.ks_test.d_max_p}")
            self.ks_tab.n.setText(f"Numero de intervalos: {self.presenter.ks_test.n_intervals}")

            # Llenar la tabla con los datos de self.presenter.ri_numbers
            data = [(i + 1, ri) for i, ri in enumerate(all_data)]
            self.ks_tab.load_data_to_table(data)

    def showKsTestG(self):
        """
        Muestra la gráfica de D_max para la prueba de Kolmogorov-Smirnov.
        """
        self.presenter.ks_test.plotDs()

    def showKsTestG2(self):
        """
        Muestra la gráfica de probabilidad de los intervalos para la prueba de Kolmogorov-Smirnov.
        """
        self.presenter.ks_test.plotIntervals()

    def showKsTestG3(self):
        """
        Muestra la gráfica de frecuencia de los intervalos para la prueba de Kolmogorov-Smirnov.
        """
        self.presenter.ks_test.plotIntervalsFreq()

    # Eventos de prueba de chi-cuadrado
    def doChi2Test(self):
        """
        Realiza la prueba de chi-cuadrado con los datos cargados.
        """
        if len(self.presenter.ri_numbers) != 0:
            # Se crea una copia de los datos
            all_data = self.presenter.ri_numbers.copy()
            numIntervals = self.chi_tab.intervalsNum.text()
            a = self.chi_tab.a_input.text()
            b = self.chi_tab.b_input.text()
            #
            if numIntervals != "" and a != "" and b != "":
                self.presenter.chi2_test = ChiTest(self.presenter.ri_numbers, int(numIntervals), float(a), float(b))
            elif numIntervals != "" and a != "" and b == "":
                self.showErrorMessage("Error", "Falta el valor de b.")
                return
            elif numIntervals != "" and a == "" and b != "":
                self.showErrorMessage("Error", "Falta el valor de a.")
                return
            elif numIntervals != "" and a == "" and b == "":
                self.presenter.chi2_test = ChiTest(self.presenter.ri_numbers, int(numIntervals))
            else:
                self.presenter.chi2_test = ChiTest(self.presenter.ri_numbers)
            self.presenter.do_chi2_test()
            #
            if self.presenter.chi2_test.passed:
                self.chi_tab.status.setText(f"Estado de la prueba: El set de datos seleccionado PASÓ la prueba satisfactoriamente")
            
            elif not self.presenter.variance_test.passed and len(self.presenter.ri_numbers) > 1000: 
                
                num_passedTwo = 0  # Inicializar contador de datos pasados

                num_iterations = len(self.presenter.ri_numbers) // 1000
                for i in range(num_iterations):
                    start_index = i * 1000
                    end_index = (i + 1) * 1000

                    subset_data = all_data[start_index:end_index]

                    self.presenter.ri_numbers = subset_data

                    if numIntervals != "" and a != "" and b != "":
                        self.presenter.chi2_test = ChiTest(subset_data, int(numIntervals), float(a), float(b))
                    elif numIntervals != "" and a != "" and b == "":
                        self.showErrorMessage("Error", "Falta el valor de b.")
                        return
                    elif numIntervals != "" and a == "" and b != "":
                        self.showErrorMessage("Error", "Falta el valor de a.")
                        return
                    elif numIntervals != "" and a == "" and b == "":
                        self.presenter.chi2_test = ChiTest(subset_data, int(numIntervals))
                    else:
                        self.presenter.chi2_test = ChiTest(subset_data)

                    self.presenter.do_chi2_test()

                    if self.presenter.chi2_test.passed:
                        for value in subset_data:
                            self.passed_data.append(value)
                    num_passedTwo += len(subset_data)
                if len(self.passed_data) > 0:
                    num_passedOne = len(self.passed_data)
                    self.chi_tab.status.setText(f"Estado de la prueba: Pasaron {num_passedOne} de {num_passedTwo} Datos")
                else:
                    self.chi_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")
            else:
                self.chi_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")
            self.chi_tab.ni_min.setText(f"Valor Ni Maximo: {str(self.presenter.chi2_test.niMax)}")
            self.chi_tab.ni_max.setText(f"Valor Ni Minimo: {str(self.presenter.chi2_test.niMin)}")
            self.chi_tab.n.setText(f"Numero de intervalos: {self.presenter.chi2_test.intervals_amount}")
            self.chi_tab.sum_chi2.setText(f"Valor de la sumatoria de Chi2: {self.presenter.chi2_test.sumChi2}")
            self.chi_tab.chi_test.setText(f"Valor de la prueba Chi2 inversa: {self.presenter.chi2_test.chiReverse}")

            # Llenar la tabla con los datos de self.presenter.ri_numbers
            data = [(i + 1, ri) for i, ri in enumerate(self.presenter.ri_numbers)]
            self.chi_tab.load_data_to_table(data)

    def showChi2TestG(self):
        """
        Muestra la gráfica de valores Chi2 calculados.
        """
        self.presenter.chi2_test.plotChi2()

    def showChi2TestG2(self):
        """
        Muestra la gráfica de frecuencias observadas para la prueba de chi-cuadrado.
        """
        self.presenter.chi2_test.plotFrequencies()
    
    # Eventos de prueba de Poker
    def doPokerTest(self):
        """
        Realiza la prueba de Poker con los datos cargados.
        """
        if len(self.presenter.ri_numbers) != 0:
            # Se crea una copia de los datos
            all_data = self.presenter.ri_numbers.copy()
            if len(self.presenter.ri_numbers) > 1000:
                if self.poker_tab.intervalsNum.text() != "":

                    num_passedTwo = 0  # Inicializar contador de datos pasados
                    
                    num_iterations = len(self.presenter.ri_numbers) // int(self.poker_tab.intervalsNum.text())
                    for i in range(num_iterations):
                        start_index = i * int(self.poker_tab.intervalsNum.text())
                        end_index = (i + 1) * int(self.poker_tab.intervalsNum.text())
                        subset_data = all_data[start_index:end_index]

                        self.presenter.ri_numbers = subset_data

                        pokertest = PokerTest(subset_data)
                        self.presenter.poker_test = pokertest
                        self.presenter.do_poker_test()
                        if self.presenter.poker_test.passed:
                            for value in subset_data:
                                self.passed_data.append(value)
                            self.poker_tab.load_data_to_table2([(f"[{start_index}, {end_index})", "PASA")])
                        else:
                            self.poker_tab.load_data_to_table2([(f"[{start_index}, {end_index})", "NO PASA")])
                        QApplication.processEvents()  # Permitir que la interfaz de usuario se actualice
                        num_passedTwo += len(subset_data)
                    if len(self.passed_data) > 0:
                        num_passedOne = len(self.passed_data)
                        self.poker_tab.status.setText(f"Estado de la prueba: Pasaron {num_passedOne} de {num_passedTwo} Datos")
                    else:
                        self.poker_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")
                else:
                    num_passedTwo = 0  # Inicializar contador de datos pasados

                    num_iterations = len(self.presenter.ri_numbers) // 1000
                    for i in range(num_iterations):
                        start_index = i * 1000
                        end_index = (i + 1) * 1000
                        subset_data = all_data[start_index:end_index]

                        self.presenter.ri_numbers = subset_data

                        pokertest = PokerTest(subset_data)
                        self.presenter.poker_test = pokertest
                        self.presenter.do_poker_test()
                        if self.presenter.poker_test.passed:
                            for value in subset_data:
                                self.passed_data.append(value)
                            self.poker_tab.load_data_to_table2([(f"[{start_index}, {end_index})", "PASA")])
                        else:
                            self.poker_tab.load_data_to_table2([(f"[{start_index}, {end_index})", "NO PASA")])
                        QApplication.processEvents()  # Permitir que la interfaz de usuario se actualice
                        # Actualizar contador de datos pasados
                        num_passedTwo += len(subset_data)
                    if len(self.passed_data) > 0:
                        num_passedOne = len(self.passed_data)
                        self.poker_tab.status.setText(f"Estado de la prueba: Pasaron {num_passedOne} de {num_passedTwo} Datos")
                    else:
                        self.poker_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba")  
            else:
                pokertest = PokerTest(self.presenter.ri_numbers)
                self.presenter.poker_test = pokertest
                self.presenter.do_poker_test()
                if self.presenter.poker_test.passed:
                    self.poker_tab.status.setText(f"Estado de la prueba: El set de datos seleccionado PASÓ la prueba satisfactoriamente")
                else:
                    self.poker_tab.status.setText(f"Estado de la prueba: El set de datos no pasó la prueba") 
            self.poker_tab.sum_val.setText(f"Valor de la sumatoria: {self.presenter.poker_test.total_sum}")
            self.poker_tab.chi_val.setText(f"Valor de la prueba chi inversa: {self.presenter.poker_test.chi_reverse}")

            # Llenar la tabla con los datos de self.presenter.ri_numbers
            data = [(i + 1, ri) for i, ri in enumerate(all_data)]
            self.poker_tab.load_data_to_table(data)

    def update_table2(self, start_index, end_index, passed):
        if passed:
            self.poker_tab.load_data_to_table2([(f"[{start_index}, {end_index})", "PASA")])
        else:
            self.poker_tab.load_data_to_table2([(f"[{start_index}, {end_index})", "NO PASA")])

    def showGraph1Poker(self):
        """
        Muestra la gráfica de sumatoria vs. chi inversa para la prueba de Poker.
        """
        self.presenter.poker_test.plot_totalSum_vs_chiReverse()

    def showGraph2Poker(self):
        """
        Muestra la gráfica de frecuencia observada vs. frecuencia esperada para la prueba de Poker.
        """
        self.presenter.poker_test.plot_oi_vs_ei()
    

