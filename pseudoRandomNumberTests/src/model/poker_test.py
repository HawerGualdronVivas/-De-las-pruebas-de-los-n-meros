from numpy import mean, var
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

class PokerTest:
    """
    Clase para realizar la Prueba de Poker en una secuencia de números pseudoaleatorios.

    Args:
        ri_nums (list): Una lista de números pseudoaleatorios en el rango [0, 1).

    Attributes:
        ri_nums (list): La lista de números pseudoaleatorios proporcionada.
        prob (list): Probabilidades de cada mano de poker según la tabla de poker.
        oi (list): Frecuencias observadas de cada mano.
        ei (list): Frecuencias esperadas de cada mano.
        eid (list): Resultado del cálculo (oi - ei)^2 / ei para cada mano.
        passed (bool): Indica si la prueba de poker ha pasado.
        n (int): Número de elementos en la secuencia de números pseudoaleatorios.
        total_sum (float): Suma total de los valores calculados (oi - ei)^2 / ei.
        chi_reverse (float): Valor crítico de chi-cuadrado para un nivel de significancia de 0.05.

    """

    def __init__(self, ri_nums):
        self.ri_nums = ri_nums
        self.prob = [0.3024, 0.504, 0.108, 0.072, 0.009, 0.0045, 0.0001]
        self.oi = [0, 0, 0, 0, 0, 0, 0]
        self.ei = []
        self.eid = []
        self.passed = False
        self.n = len(ri_nums)
        self.total_sum = 0.0
        self.chi_reverse = st.chi2.ppf(1 - 0.05, 6)

    def check_poker(self):
        """
        Realiza la prueba de poker y determina si ha pasado.

        Returns:
            bool: True si la prueba ha pasado, False en caso contrario.
        """
        self.calculate_oi()
        self.calculate_ei()
        self.calculate_eid()
        self.calculate_total_sum()
        if (self.total_sum < self.chi_reverse):
            self.passed = True
        else:
            self.passed = False
        return self.passed
    
    def calculate_total_sum(self):
        """Calcula la suma total de los valores calculados (oi - ei)^2 / ei."""
        for num in self.eid:
            self.total_sum += num
    
    def calculate_oi(self):
        """Calcula las frecuencias observadas de cada mano de poker."""
        for n in self.ri_nums:
            arr = str(n).split(".")
            num = arr[1]
            if self.all_diff(str(num)):  # todas diferentes
                self.oi[0] += 1
            elif self.all_same(str(num)):  # todas iguales
                self.oi[6] += 1
            elif self.four_of_a_kind(str(num)):  # cuatro del mismo valor (poker)
                self.oi[5] += 1
            elif self.one_three_of_a_kind_and_one_pair(str(num)):  # una tercia y un par (Full house)
                self.oi[4] += 1
            elif self.only_three_of_a_kind(str(num)):  # solo una tercia
                self.oi[3] += 1
            elif self.two_pairs(str(num)):  # dos pares
                self.oi[2] += 1
            elif self.only_one_pair(str(num)):  # solo un par
                self.oi[1] += 1
    
    def all_diff(self, numstr):
        """Comprueba si todos los caracteres son diferentes en el número dado."""
        return len(numstr) == len(set(numstr))
    
    def all_same(self, numstr):
        """Comprueba si todos los caracteres son iguales en el número dado."""
        return len(set(numstr)) == 1
    
    def four_of_a_kind(self, numstr):
        """Comprueba si hay cuatro del mismo valor en el número dado."""
        count = {}
        for char in numstr:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1

        num_quads = sum(1 for freq in count.values() if freq == 4)

        return num_quads == 1
    
    def two_pairs(self, numstr):
        """Comprueba si hay dos pares en el número dado."""
        count = {}
        for char in numstr:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1

        num_pairs = sum(1 for freq in count.values() if freq == 2)

        return num_pairs == 2
    
    def one_three_of_a_kind_and_one_pair(self, numstr):
        """Comprueba si hay una tercia y un par en el número dado (Full house)."""
        count = {}
        for char in numstr:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1

        num_pairs = sum(1 for freq in count.values() if freq == 2)
        num_triples = sum(1 for freq in count.values() if freq == 3)

        return num_pairs == 1 and num_triples == 1

    def only_one_pair(self, numstr):
        """Comprueba si hay solo un par en el número dado."""
        count = {}
        for char in numstr:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1

        num_pairs = sum(1 for freq in count.values() if freq == 2)

        return num_pairs == 1

    def only_three_of_a_kind(self, numstr):
        """Comprueba si hay solo una tercia en el número dado."""
        count = {}
        for char in numstr:
            if char in count:
                count[char] += 1
            else:
                count[char] = 1

        num_triples = sum(1 for freq in count.values() if freq == 3)

        return num_triples == 1
    
    def calculate_ei(self):
        """Calcula las frecuencias esperadas de cada mano de poker."""
        for i in range(0, 7):
            self.ei.append(self.prob[i] * self.n)

    def calculate_eid(self):
        """Calcula el resultado del cálculo (oi - ei)^2 / ei para cada mano de poker."""
        for i in range(0, len(self.oi)):
            if (self.prob[i] * self.n) != 0:
                self.eid.append(((self.oi[i] - self.prob[i] * self.n) ** 2) / (self.prob[i] * self.n))
            
    def plot_totalSum_vs_chiReverse(self):
        """
        Genera y muestra un gráfico de barras que compara la suma total (oi - ei)^2 / ei con el valor crítico de chi-cuadrado.

        Este gráfico ayuda a visualizar si la prueba de poker ha pasado o no.
        """
        if self.n != 0:
            x = ['SUM (Ei - Oi)^2 / Ei', 'Chi2_reverse']  
            y = [self.total_sum, self.chi_reverse]    
            colors = ['purple', 'yellow']
            fig, ax = plt.subplots()
            bars = plt.bar(x, y, color=['purple', 'yellow'])
            plt.bar(x, y, edgecolor='black', color=colors)
            plt.xlabel('Índices')
            plt.ylabel('Valores')
            plt.title('Gráfico de Barras: chi_reverse vs. total_sum')
            for bar, value in zip(bars, y):
                ax.annotate(str(value), xy=(bar.get_x() + bar.get_width() / 2, value), xytext=(0, 1),
                            textcoords='offset points', ha='center', va='bottom')
            # Mostrar el gráfico
            plt.show()
    
    def plot_oi_vs_ei(self):
        """
        Genera y muestra un gráfico de barras que compara las frecuencias observadas (oi) y las frecuencias esperadas (ei).

        Este gráfico ayuda a visualizar cómo se comparan las frecuencias en la prueba de poker.
        """
        if self.n != 0:
            hands = ['D', 'O', 'T', 'K', 'F', 'P', 'Q']  # Manos de poker
            oi = self.oi  # Frecuencias observadas
            ei = self.ei  # Frecuencias esperadas

            ancho_barra = 0.35
            indice = np.arange(len(hands))
            ancho_total = 0.4

            fig, ax = plt.subplots()
            oi = ax.bar(indice - ancho_barra / 2, oi, ancho_barra, label='Obtenidas')
            ei = ax.bar(indice + ancho_barra / 2, ei, ancho_barra, label='Esperadas', alpha=0.7)

            ax.set_xlabel('Manos')
            ax.set_ylabel('Frecuencia')
            ax.set_title('Manos vs. Frecuencia (Obtenidas vs. Esperadas)')
            ax.set_xticks(indice)
            ax.set_xticklabels(hands)
            ax.legend()

            plt.show()
        
    def __str__(self):
        return f"PokerTest(ri_nums={self.ri_nums}, prob={self.prob}, oi={self.oi}, ei={self.ei}, eid={self.eid}, passed={self.passed}, n={self.n}, total_sum={self.total_sum}, chi_reverse={self.chi_reverse})"