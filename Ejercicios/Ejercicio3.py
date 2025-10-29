from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow

class Ventana(QMainWindow):
    def _init_(self, nombre):
        super()._init_()
        self.setWindowTitle(f"Ventana {nombre}")
        self.boton = QPushButton(f"Haz clic en {nombre}",self)
        self.setCentralWidget(self.boton)
        self.boton.clicked.connect(self.on_click)

    def on_click(self):
        # Cada instancia usa su propio ⁠ self ⁠
        self.boton.setText(f"Clic en {self.windowTitle()}")
        print(f"[{self.windowTitle()}] Señal recibida -> self={hex(id(self))}")

if _name_ == "_main_":
    app = QApplication([])
    a = Ventana("A")
    b = Ventana("B")
    a.move(200, 200)
    b.move(450, 200)
    a.show()
    b.show()
    app.exec()