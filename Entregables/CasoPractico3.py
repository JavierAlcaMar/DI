from PySide6.QtWidgets import QApplication, QComboBox, QMainWindow

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Ventana")
        self.combo = QComboBox(self)

        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        self.combo.addItems(["Meses del Año"])
        self.combo.addItems(meses)

        # ---------------------------------------------------
        # cambiar el tamaño del texto
        font = self.combo.font()
        font.setPointSize(20)
        self.combo.setFont(font)
        self.combo.setStyleSheet("font-size: 20pt;")  # Alternativa para cambiar el tamaño del texto
        # ---------------------------------------------------

        self.combo.setFixedSize(200, 60)
        self.setFixedSize(200, 60)       # Hago que la ventana tenga el mismo tamaño que el combo

        self.combo.currentTextChanged.connect(self.actualiza_etiqueta)      # La señal le pasa directamente el texto, por eso no lo paso como parámetro

    def actualiza_etiqueta(self, texto):
        print(f'{texto} es el mes número {self.combo.currentIndex()}')      # Al emitir la señal, el índice ya está actualizado en el currentIndex()




if __name__ == "__main__":
    app = QApplication([])      
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()