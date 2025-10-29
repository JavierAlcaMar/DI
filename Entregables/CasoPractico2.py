from PySide6.QtWidgets import QApplication, QLineEdit, QLabel, QMainWindow

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Ventana")
        self.linea = QLineEdit(self)
        self.linea.setMaxLength(5)
        self.linea.setFixedSize(50, 30)  
        self.etiqueta = QLabel("", self)
        self.etiqueta.move(60, 0)           # En vez de 50 le pongo 60 para que se vea mejor
        self.etiqueta.setFixedSize(50, 30)
        self.linea.textChanged.connect(self.actualizar_etiqueta)

    def actualizar_etiqueta(self, texto):
        self.etiqueta.setText(texto)




if __name__ == "__main__":
    app = QApplication([])      
    ventana1 = Ventana()
    ventana1.show()
    app.exec()                