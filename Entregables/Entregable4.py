import os

from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QTextEdit, QWhatsThis
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana principal con menús")
    
        barraMenus = self.menuBar()
        menu = barraMenus.addMenu("&Menu")


        action1 = QAction("&Imprimir en dock", self)
        action1.setIcon(QIcon(os.path.join(os.path.dirname(
            __file__), "images/console.png")))
        action1.setWhatsThis("Al ejecutar esta acción, se añadirá " \
        "   el texto \"Acción pulsada\" en el dock. Se puede lanzar por Menú")
        action1.setShortcut(QKeySequence("Ctrl+p"))
        action1.triggered.connect(self.imprimir_en_dock)

        action2 = QAction("&Que es esto?", self)
        action2.setIcon(QIcon(os.path.join(os.path.dirname(
            __file__), "images/ask.png")))
        action2.setWhatsThis("Esta acción hace que al clickear cualquier opción " \
        "   del menú, se muestre su ayuda.")
        action2.setShortcut(QKeySequence("Ctrl+q"))
        action2.triggered.connect(self.showWhatsThis)
        

        menu.addAction(action1)
        menu.addAction(action2)

        toolbar = QToolBar("Barra de herramientas 1")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.addAction(action1)
        toolbar.addAction(action2)
        self.addToolBar(toolbar)

        self.qTextEditDock = QTextEdit()
        self.setCentralWidget(self.qTextEditDock)


    def imprimir_en_dock(self):
        self.qTextEditDock.insertPlainText("Acción pulsada")

    def showWhatsThis(self):
        if(QWhatsThis.inWhatsThisMode()):
            QWhatsThis.leaveWhatsThisMode()
            print("Modo 'Qué es esto?' activado")
        else:
            QWhatsThis.enterWhatsThisMode()
            print("Modo 'Qué es esto?' desactivado")
        



if __name__ == "__main__":
    app = QApplication([])

    ventana1 = VentanaPrincipal()
    ventana1.show()

    app.exec()