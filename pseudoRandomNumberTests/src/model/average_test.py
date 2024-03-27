from statistics import mean
from math import sqrt
from scipy.stats import norm
import matplotlib.pyplot as plt

class AverageTest:
    """
    Clase que implementa la Prueba de Promedio para una secuencia de números generados.
    """

    def __init__(self, ri_nums):
        """
        Inicializa una instancia de AverageTest.

        :param ri_nums: Lista de números generados.
        """
        self.ri_nums = ri_nums
        self.average = 0
        self.alpha = 0.05
        self.acceptation = 0.95
        self.passed = False
        self.n = len(ri_nums)
        self.z = 0.0
        self.superior_limit = 0.0
        self.inferior_limit = 0.0

    def calcAverage(self):
        """
        Calcula el promedio de la secuencia de números generados.
        """
        if self.n != 0:
            self.average = mean(self.ri_nums)

    def calculateZ(self):
        """
        Calcula el valor Z necesario para la prueba.
        """
        self.z = norm.ppf(1 - (self.alpha / 2))

    def calculateSuperiorLimit(self):
        """
        Calcula el límite superior para la prueba.
        """
        if self.n > 0:
            self.superior_limit = (1/2) + (self.z * (1 / sqrt(12 * self.n)))

    def calculateInferiorLimit(self):
        """
        Calcula el límite inferior para la prueba.
        """
        if self.n > 0:
            self.inferior_limit = (1/2) - (self.z * (1 / sqrt(12 * self.n)))
    
    def checkTest(self):
        """
        Realiza la prueba de Promedio y establece si ha sido superada.
        """
        self.calcAverage()
        self.calculateZ()
        self.calculateSuperiorLimit()
        self.calculateInferiorLimit()
        if self.inferior_limit <= self.average <= self.superior_limit:
            self.passed = True
        else:
            self.passed = False
    
    def checkIfPassed(self):
        """
        Comprueba si la prueba ha sido superada.

        :return: True si la prueba ha sido superada, False en caso contrario.
        """
        if self.inferior_limit <= self.average <= self.superior_limit:
            self.passed = True
        else:
            self.passed = False
        return self.passed
    
    def clear(self):
        """
        Restablece los valores de la prueba a sus valores iniciales.
        """
        self.average = 0
        self.alpha = 0.05
        self.acceptation = 0.95
        self.passed = False
        self.z = 0.0
        self.superior_limit = 0.0
        self.inferior_limit = 0.0

    def plotLimitsAndAverage(self):
        """
        Genera un gráfico que muestra los límites y el valor promedio.
        """
        x = ["Límite Inferior", "Promedio", "Límite Superior"]
        y = [self.inferior_limit, self.average, self.superior_limit]

        fig, ax = plt.subplots()
        bars = plt.bar(x, y, color=['red', 'blue', 'green'])
        plt.title('Comparación de Límite Inferior, Promedio (Media) y Límite Superior')
        plt.xlabel('Categoría')
        plt.ylabel('Valor')

        # Agregar etiquetas de valor en las barras
        for bar, value in zip(bars, y):
            ax.annotate(str(value), xy=(bar.get_x() + bar.get_width() / 2, value), xytext=(0, 1),
                        textcoords='offset points', ha='center', va='bottom')
        plt.show()
