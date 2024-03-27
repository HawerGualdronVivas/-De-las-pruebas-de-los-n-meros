class FileManager:
    """
    Clase para gestionar un archivo que contiene números en formato de texto.
    """

    def __init__(self, input_file_path=''):
        """
        Inicializa una instancia de FileManager.
        
        :param input_file_path: Ruta del archivo de entrada que contiene los números.
        """
        self.input_file_path = input_file_path
        self.numbers = []

    def storage_numbers(self):
        """
        Lee los números desde el archivo de entrada y los almacena como floats en self.numbers.

        :raises FileNotFoundError: Se levanta si el archivo de entrada no existe.
        :raises Exception: Se levanta si ocurre un error no especificado durante la lectura.
        """
        try:
            with open(self.input_file_path, 'r') as input_file:
                lines = input_file.readlines()
                lista_de_strings = []
                for line in lines:
                    lista_de_strings.append(line)
                # Usando Decimal para mayor precisión y evitar errores con notación 'c'
                self.numbers = [float(s) for s in lista_de_strings]
        except FileNotFoundError:
            print("El archivo de entrada no existe.")
        except Exception as e:
            print(f"Se ha producido un error: {str(e)}")

