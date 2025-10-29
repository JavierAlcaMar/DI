from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton
)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        self.usuario = "admin"
        self.contraseña = "admin"

        self.setFixedSize(240, 150)

        self.usuario_label = QLabel("Usuario:", self)
        self.usuario_label.move(20, 20)
        
        self.qlineedit_usuario = QLineEdit(self)        # Hace que se pueda escribir en la línea de texto
        self.qlineedit_usuario.setPlaceholderText("Usuario")
        self.qlineedit_usuario.move(100, 20)
        self.qlineedit_usuario.setFixedWidth(120)       # Ancho fijo de la línea de texto

        self.pass_label = QLabel("Contraseña:", self)
        self.pass_label.move(20, 70)
        
        self.qlineedit_pass = QLineEdit(self)
        self.qlineedit_pass.move(100, 70)
        self.qlineedit_pass.setPlaceholderText("Contraseña")
        self.qlineedit_pass.setEchoMode(QLineEdit.EchoMode.Password)   # Hace que los caracteres se muestren como asteriscos
        self.qlineedit_pass.setFixedWidth(120)

        self.boton_login = QPushButton("Login", self)
        self.boton_login.move(20, 110)
        self.boton_login.setFixedSize(200, 30)
        
        self.etiqueta_resultado = QLabel("", self)
        self.etiqueta_resultado.move(20, 140)
        self.etiqueta_resultado.setFixedWidth(200)

        self.boton_login.clicked.connect(self.mostrar_resultado)
        self.qlineedit_usuario.textChanged.connect(self.resetear)
        self.qlineedit_pass.textChanged.connect(self.resetear)



        
    def comprobar_credenciales(self):
        if(self.qlineedit_usuario.text() == self.usuario and self.qlineedit_pass.text() == self.contraseña):
            return True
        else:
            return False
    
    def mostrar_resultado(self, correcto):
        if(self.comprobar_credenciales()):
            self.setFixedSize(240, 170)
            self.etiqueta_resultado.setText("Login correcto")
            self.etiqueta_resultado.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.setFixedSize(240, 170)
            self.etiqueta_resultado.setText("Login incorrecto")
            self.etiqueta_resultado.setStyleSheet("color: red; font-weight: bold;")

    def resetear(self):
        self.etiqueta_resultado.clear()
        self.setFixedSize(240, 150)
        
        

if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()

