from PySide6.QtWidgets import QApplication, QLabel, QWidget

class Ventana(QWidget):     # QWidget de parametro porque hereda de QWidget
    def __init__(self):     # Constructor
        super().__init__()  # Llamada al constructor de la clase padre
        self.setWindowTitle("Mi Ventana")
        self.etiqueta1 = QLabel("Hola Mundo!", self)



if __name__ == "__main__":
    app = QApplication([])      # Crear la aplicacion, los [] son los argumentos de la aplicacion
    ventana1 = Ventana()
    ventana1.show()
    app.exec()                  # Iniciar el bucle de eventos