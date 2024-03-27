import sys
from model.poker_test import PokerTest
from .file_Manager import FileManager
from model.average_test import AverageTest
from model.variance_test import VarianceTest
from model.ks_test import KsTest
from model.chi2_test import ChiTest

class Presenter:
    """
    Clase Presenter que maneja la lógica de la aplicación y se comunica con la interfaz de usuario.
    """

    def __init__(self):
        """
        Inicializa una instancia de Presenter.
        """
        self.file_manager = FileManager()
        self.ri_numbers = []
        self.poker_test = PokerTest(self.ri_numbers)
        self.average_test = AverageTest(self.ri_numbers)
        self.variance_test = VarianceTest(self.ri_numbers)
        self.chi2_test = ChiTest(self.ri_numbers)
        self.ks_test = KsTest(self.ri_numbers)
        self.view = None  # Esta será la referencia a la ventana principal

    def do_poker_test(self):
        """
        Realiza la prueba de Poker con los números generados.
        """
        self.poker_test.ri_nums = self.ri_numbers
        self.poker_test.check_poker()
        
    def do_average_test(self):
        """
        Realiza la prueba de Promedio con los números generados.
        """
        self.average_test.ri_numbers = self.ri_numbers
        self.average_test.checkTest()
    
    def do_variance_test(self):
        """
        Realiza la prueba de Varianza con los números generados.
        """
        self.variance_test.ri_numbers = self.ri_numbers
        self.variance_test.checkTest()
    
    def do_chi2_test(self):
        """
        Realiza la prueba de Chi-Cuadrado con los números generados.
        """
        self.chi2_test.ri_numbers = self.ri_numbers
        self.chi2_test.checkTest()
    
    def do_ks_test(self):
        """
        Realiza la prueba de Kolmogorov-Smirnov con los números generados.
        """
        self.ks_test.ri_numbers = self.ri_numbers
        self.ks_test.checkTest()
    
    def set_main_window(self, main_window):
        """
        Establece la ventana principal de la aplicación.

        :param main_window: Referencia a la ventana principal.
        """
        self.view = main_window
        
    def add_numbers(self):
        """
        Agrega los números desde el archivo al conjunto de números generados.
        """
        self.ri_numbers = self.file_manager.numbers

    def run(self):
        """
        Muestra la ventana principal y ejecuta la aplicación.
        """
        self.view.show()
        sys.exit(self.app.exec())