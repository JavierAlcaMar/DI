import os

from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Ventana principal con menú y barra de herramientas")
        

        barra_menus = self.menuBar()
        menu = barra_menus.addMenu("&Menu")

        ruta_a_icono = os.path.join(os.path.dirname(
            __file__), "images/console.png")
        
        accion = QAction(QIcon(ruta_a_icono), "Imprimir por consola", self)     # Las acciones se usan en muchas partes del codigo, a diferencia de los eventos
        accion.setWhatsThis(
            "Al pulsar sobre el botón se imprimirá un texto por consola")
        accion.setShortcut(QKeySequence("Ctrl+p"))
        accion.triggered.connect(self.imprimir_por_consola)                     # Conectar la accion a un metodo se usa a parte de connect, triggered

        menu.addAction(accion)                                                  # La accion se añade a un menu y a una barra de herramientas

        barra_herramientas = QToolBar("Barra de herramientas 1")
        barra_herramientas.addAction(accion)
        self.addToolBar(barra_herramientas)

    def imprimir_por_consola(self):
        print("Acción lanzada a través del menú, del atajo" +
              " o de la barra de herramientas")


if __name__ == "__main__":
    app = QApplication([])

    ventana1 = VentanaPrincipal()
    ventana1.show()

    app.exec()