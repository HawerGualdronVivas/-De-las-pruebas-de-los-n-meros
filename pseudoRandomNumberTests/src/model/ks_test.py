from statistics import mean
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

class KsTest:
    """
    Clase que implementa la Prueba de Kolmogorov-Smirnov (KS) para una secuencia de números generados.
    """

    def __init__(self, ri_nums=[], n_intervals=10):
        """
        Inicializa una instancia de KsTest.

        :param ri_nums: Lista de números generados.
        :param n_intervals: Cantidad de intervalos para la prueba KS.
        """
        self.ri = ri_nums
        self.n = len(ri_nums)
        self.average = 0
        self.d_max = 0
        self.d_max_p = 0
        self.min = 0
        self.max = 0
        self.oi = []
        self.oia = []
        self.prob_oi = []
        self.oia_a = []
        self.prob_esp = []
        self.diff = []
        self.passed = False
        self.alpha = 0.05
        self.intervals = []
        self.n_intervals = n_intervals

    def calculate_oia(self):
        """
        Calcula la sumatoria acumulada de las frecuencias observadas (oia).
        """
        cum_freq = 0

        for freq in self.oi:
            cum_freq += freq
            self.oia.append(cum_freq)

    def calculate_min(self):
        """
        Calcula el valor mínimo en la secuencia de números generados.
        """
        if self.n != 0:
            self.min = min(self.ri)

    def calculate_max(self):
        """
        Calcula el valor máximo en la secuencia de números generados.
        """
        if self.n != 0:
            self.max = max(self.ri)

    def calculateAverage(self):
        """
        Calcula el promedio de la secuencia de números generados.
        """
        if self.n != 0:
            self.average = mean(self.ri)

    def checkTest(self):
        """
        Realiza la prueba de Kolmogorov-Smirnov (KS) y establece si ha sido superada.
        """
        self.calculate_min()
        self.calculate_max()
        self.calculateAverage()
        self.calculate_intervals()
        self.calculate_oi()
        self.calculate_oia()
        self.calculate_prob_oi()
        self.calculate_oia_a()
        self.calculate_prob_esp()
        self.calculate_diff()
        self.d_max = max(self.diff)
        self.calculate_KS()
        if self.d_max <= self.d_max_p:
            self.passed = True
        else:
            self.passed = False

    def calculate_KS(self):
        """
        Calcula el valor crítico de Kolmogorov-Smirnov (KS) para la prueba.
        """
        alpha = self.alpha
        n = self.n
        if self.n <= 50 and self.n > 0:
            # Calcular el valor crítico usando la función scipy.stats.ksone.ppf()
            critical_value = stats.ksone.ppf(1 - alpha / 2, n) 
            # OJO: Usamos 1 - alpha / 2 para una prueba bilateral
        if self.n > 50:
            # Calcular el valor crítico usando la función scipy.stats.kstwobign.isf()
            critical_value = stats.kstwobign.isf(alpha) / np.sqrt(n)
        self.d_max_p = critical_value

    def calculate_prob_esp(self):
        """
        Calcula las probabilidades esperadas para cada intervalo.
        """
        for i in range(len(self.oia_a)):
            self.prob_esp.append(self.oia_a[i] / self.n)

    def calculate_diff(self):
        """
        Calcula las diferencias absolutas entre las probabilidades observadas y esperadas.
        """
        for i in range(len(self.prob_esp)):
            self.diff.append(abs(self.prob_esp[i] - self.prob_oi[i]))

    def calculate_oia_a(self):
        """
        Calcula la sumatoria acumulada de las probabilidades esperadas (oia_a).
        """
        n1 = self.n / self.n_intervals
        for i in range(self.n_intervals):
            self.oia_a.append(n1 * (i + 1))

    def calculate_prob_oi(self):
        """
        Calcula las probabilidades observadas para cada intervalo.
        """
        for i in range(len(self.oia)):
            self.prob_oi.append(self.oia[i] / self.n)

    def calculate_oi(self):
        """
        Calcula las frecuencias observadas para cada intervalo.
        """
        self.ri.sort()
        self.oi = [0] * self.n_intervals
        # Iterar a través de los valores de ri y contar en qué intervalo caen
        for valor in self.ri:
            for i, intervalo in enumerate(self.intervals):
                if intervalo[0] <= valor < intervalo[1]:
                    self.oi[i] += 1
                    break  # No es necesario seguir buscando en otros intervalos

        return self.oi

    def calculate_intervals(self):
        """
        Calcula los intervalos utilizados para la prueba KS.
        """
        if self.n != 0:
            n_intervals = self.n_intervals
            interval_size = (self.max - self.min) / n_intervals
            initial = self.min
            for _ in range(n_intervals):
                new_interval = (initial, initial + interval_size)
                self.intervals.append(new_interval)
                initial = new_interval[1]

    def plotDs(self):
        """
        Genera un gráfico que muestra los valores Dmax (error calculado) y Dmax_p (valor KS máximo de la tabla).
        """
        x = ["Dmax (error calculado)", "Dmax_p (valor KS máximo -> Tabla)"]
        y = [self.d_max, self.d_max_p]

        fig, ax = plt.subplots()
        bars = plt.bar(x, y, color=['red', 'blue'])
        plt.title('Comparación de Dmax (error calculado) y Dmax_p (valor KS máximo -> Tabla)')
        plt.ylabel('Valores')
        plt.xlabel('Errores')

        # Agregar etiquetas de valor en las barras
        for bar, value in zip(bars, y):
            ax.annotate(str(value), xy=(bar.get_x() + bar.get_width() / 2, value), xytext=(0, 1),
                        textcoords='offset points', ha='center', va='bottom')
        plt.show()

    def plotIntervals(self):
        """
        Genera un gráfico que muestra las probabilidades observadas y esperadas en cada intervalo.
        """
        # Create a list to store interval labels
        interval_labels = []

        # Create lists to store observed and expected probabilities
        observed_probabilities = []
        expected_probabilities = []

        for i, interval in enumerate(self.intervals):
            # Define the label for the interval
            label = f"Intervalo {i + 1}: [{interval[0]:.3f}, {interval[1]:.3f})"
            interval_labels.append(label)

            # Append observed and expected probabilities to their respective lists
            observed_probabilities.append(self.prob_esp[i])
            expected_probabilities.append(self.prob_oi[i])

        # Create an array of x positions for the bars
        x = np.arange(len(interval_labels))

        # Create a bar chart
        width = 0.35  # Width of the bars
        fig, ax = plt.subplots()
        observed_bars = ax.bar(x - width / 2, observed_probabilities, width, label='Probabilidad Observada')
        expected_bars = ax.bar(x + width / 2, expected_probabilities, width, label='Probabilidad Esperada')

        # Add labels, title, and legend
        ax.set_xlabel('Intervalos')
        ax.set_ylabel('Probabilidades')
        ax.set_title('Probabilidades Observadas y Esperadas en Cada Intervalo')
        ax.set_xticks(x)
        ax.set_xticklabels(interval_labels, rotation=45, ha='right')
        ax.legend()
        plt.tight_layout()
        plt.show()

    def plotIntervalsFreq(self):
        """
        Genera un gráfico que muestra las frecuencias observadas en cada intervalo.
        """
        # Create a list to store interval labels
        interval_labels = []

        # Create a list to store observed frequencies
        observed_frequencies = []

        for i, interval in enumerate(self.intervals):
            # Define the label for the interval
            label = f"Intervalo {i + 1}: [{interval[0]:.3f}, {interval[1]:.3f})"
            interval_labels.append(label)

            # Append observed frequencies to the list
            observed_frequencies.append(self.oi[i])

        # Create an array of x positions for the bars
        x = np.arange(len(interval_labels))

        # Create a bar chart
        width = 0.35  # Width of the bars
        fig, ax = plt.subplots()
        # Add labels, title, and legend
        ax.set_xlabel('Intervalos')
        ax.set_ylabel('Frecuencia de Números en Cada Intervalo')
        ax.set_title('Frecuencias de Números Observadas para Cada Intervalo')
        ax.set_xticks(x)
        ax.set_xticklabels(interval_labels, rotation=45, ha='right')

        # Plot the observed frequencies as bars
        bars = ax.bar(x, observed_frequencies, width, label='Frecuencia Observada')

        # Add values on top of the bars
        for bar, oi in zip(bars, observed_frequencies):
            height = bar.get_height()
            ax.annotate(f'{oi}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        ax.legend()
        plt.tight_layout()
        plt.show()
