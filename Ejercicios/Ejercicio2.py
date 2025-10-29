from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Principal")
        self.boton1 = QPushButton("Presioname", self)
        self.setCentralWidget(self.boton1)
        self.boton1.clicked.connect(self.click_boton)
        self.boton1.pressed.connect(self.presion_boton)
        self.boton1.released.connect(self.soltar_boton)

    def click_boton(self):
        print("Boton clickeado")

    def presion_boton(self):
        print("Boton presionado")

    def soltar_boton(self):
        print("Boton soltado")

if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()
    app.exec()