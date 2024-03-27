from typing import Any
from scipy.stats import chi2
import numpy as np
import matplotlib.pyplot as plt

class ChiTest:
    """
    Clase que implementa la Prueba de Chi-Cuadrado para una secuencia de números generados.
    """

    def __init__(self, ri_values=[], intervals_amount=8, a=8, b=10):
        """
        Inicializa una instancia de ChiTest.

        :param ri_values: Lista de números generados.
        :param intervals_amount: Cantidad de intervalos para la prueba.
        :param a: Parámetro 'a' utilizado en el cálculo de 'ni'.
        :param b: Parámetro 'b' utilizado en el cálculo de 'ni'.
        """
        self.ri_values = ri_values
        self.ni_values = []
        self.a = a
        self.b = b
        self.niMin = 0
        self.niMax = 0
        self.num_amount = len(ri_values)
        self.intervals_amount = intervals_amount
        self.intervals_values = []
        self.frequency_obtained = []
        self.expected_frequency = []
        self.chi_squared_values = []
        self.chiReverse = 0
        self.sumChi2 = 0
        self.passed = False

    def fillNiValues(self):
        """
        Calcula y llena la lista 'ni_values' con los valores 'ni'.
        """
        for i in range(self.num_amount):
            value = self.a + (self.b - self.a) * self.ri_values[i]
            self.ni_values.append(value)

    def sortNiArray(self):
        """
        Ordena la lista 'ni_values'.
        """
        self.ni_values.sort()

    def obtainMinNiValue(self):
        """
        Obtiene el valor mínimo de 'ni_values'.

        :return: El valor mínimo de 'ni_values'.
        """
        self.niMin = min(self.ni_values)
        return min(self.ni_values)

    def obtainMaxNiValue(self):
        """
        Obtiene el valor máximo de 'ni_values'.

        :return: El valor máximo de 'ni_values'.
        """
        self.niMax = max(self.ni_values)
        return max(self.ni_values)

    def fillIntervalsValuesArray(self):
        """
        Llena la lista 'intervals_values' con los valores de los intervalos.
        """
        min_value = self.obtainMinNiValue()
        max_value = self.obtainMaxNiValue()
        self.intervals_values.append(min_value)

        for i in range(self.intervals_amount):
            value = round(self.intervals_values[i] + (max_value - min_value) / self.intervals_amount, 5)
            self.intervals_values.append(value)

    def fillFrequenciesArrays(self):
        """
        Llena las listas 'frequency_obtained' y 'expected_frequency' con las frecuencias observadas y esperadas respectivamente.
        """
        expected_freq = round(float(len(self.ni_values)) / self.intervals_amount, 2)
        counter = 0

        for i in range(len(self.intervals_values) - 1):
            for j in range(len(self.ni_values)):
                if (self.ni_values[j] >= self.intervals_values[i]) and (self.ni_values[j] < self.intervals_values[i + 1]):
                    counter += 1
            self.frequency_obtained.append(counter)
            self.expected_frequency.append(expected_freq)
            counter = 0

    def fillChiSquaredValuesArray(self):
        """
        Llena la lista 'chi_squared_values' con los valores calculados de Chi-Cuadrado.
        """
        for i in range(len(self.frequency_obtained)):
            value = round(((self.frequency_obtained[i] - self.expected_frequency[i]) ** 2) / self.expected_frequency[i], 2)
            self.chi_squared_values.append(value)

    def cumulativeObtainedFrequency(self):
        """
        Calcula la frecuencia acumulada de los valores observados.

        :return: La frecuencia acumulada de los valores observados.
        """
        result = sum(self.frequency_obtained)
        return result

    def cumulativeExpectedFrequency(self):
        """
        Calcula la frecuencia acumulada de los valores esperados.

        :return: La frecuencia acumulada de los valores esperados.
        """
        result = sum(self.expected_frequency)
        return result

    def cumulativeChiSquaredValues(self):
        """
        Calcula la sumatoria de los valores de Chi-Cuadrado.

        :return: La sumatoria de los valores de Chi-Cuadrado.
        """
        result = sum(self.chi_squared_values)
        return result

    def chi_squared_test_value(self):
        """
        Calcula el valor crítico de Chi-Cuadrado para la prueba.

        :return: El valor crítico de Chi-Cuadrado.
        """
        margin_of_error = 0.05
        degrees_of_freedom = self.intervals_amount - 1

        chiSquared = chi2(degrees_of_freedom)
        return chiSquared.ppf(1.0 - margin_of_error)

    def checkTest(self):
        """
        Realiza la prueba de Chi-Cuadrado y establece si ha sido superada.
        """
        self.fillNiValues()
        self.sortNiArray()
        self.fillIntervalsValuesArray()
        self.fillFrequenciesArrays()
        self.fillChiSquaredValuesArray()
        self.chiReverse = self.chi_squared_test_value()
        self.sumChi2 = self.cumulativeChiSquaredValues()
        if self.cumulativeChiSquaredValues() <= self.chi_squared_test_value():
            self.passed = True
        else:
            self.passed = False
            
    def plotChi2(self):
        """
        Genera un gráfico que muestra los valores de Chi-Cuadrado calculados y el valor crítico de Chi-Cuadrado.
        """
        x = ["Sumatoria de Valores Chi2", "Valor de la prueba Chi2 Inversa"]
        y = [self.cumulativeChiSquaredValues(), self.chi_squared_test_value()]

        fig, ax = plt.subplots()
        bars = plt.bar(x, y, color=['yellow', 'red'])
        plt.title('Comparación de Sumatoria de Valores Chi2 y Valor de la prueba Chi2 Inversa')
        plt.ylabel('Valores')
        plt.xlabel('Valores de Chi2')

        # Agregar etiquetas de valor en las barras
        for bar, value in zip(bars, y):
            ax.annotate(str(value), xy=(bar.get_x() + bar.get_width() / 2, value), xytext=(0, 1),
                        textcoords='offset points', ha='center', va='bottom')
        plt.show()
        
    def plotFrequencies(self):
        """
        Genera un gráfico que muestra las frecuencias observadas y esperadas en cada intervalo.
        """
        # Crear un rango de valores para el eje x (los intervalos)
        x = np.arange(len(self.intervals_values) - 1)

        # Ancho de las barras
        width = 0.35

        # Crear la figura y el eje
        fig, ax = plt.subplots()

        # Crear barras para las frecuencias observadas y esperadas
        bars_observed = ax.bar(x - width/2, self.frequency_obtained, width, label='Frecuencia Observada')
        bars_expected = ax.bar(x + width/2, self.expected_frequency, width, label='Frecuencia Esperada')

        # Etiquetas y leyenda
        ax.set_xlabel('Intervalos')
        ax.set_ylabel('Frecuencia')
        ax.set_title('Frecuencias Observadas y Esperadas en Cada Intervalo')

        # Construir las etiquetas de intervalos con el rango
        interval_labels = [f'Intervalo {i + 1}: [{self.intervals_values[i]:.3f}, {self.intervals_values[i+1]:.3f})' for i in range(len(x))]

        # Rotar las etiquetas de intervalos diagonalmente
        ax.set_xticks(x)
        ax.set_xticklabels(interval_labels, rotation=45, ha='right')

        ax.legend()

        plt.tight_layout()
        plt.show()