import os

from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QTextEdit, QWhatsThis, QStatusBar, QFileDialog, QInputDialog, QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFontDialog, QColorDialog, QMessageBox, QSizePolicy
from PySide6.QtGui import QAction, QIcon, QKeySequence, QTextCursor, QTextCharFormat, QColor, QTextDocument, QFont
from PySide6.QtCore import Qt, QSize, Signal
from contadorWidget import WordCounterWidget

import speech_recognition as sr
import unicodedata
import re
import threading

class VentanaPrincipal(QMainWindow):
    recognized_text = Signal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Word")
        # Establecer el icono de la aplicación
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(
            __file__), "imagesMO/iconoApp.ico")))

        # Creamos la barra de menus
        barraMenus = self.menuBar()

        # Crea los munus y los agrega a la barra de menus
        archivo = barraMenus.addMenu("&Archivo")
        editar = barraMenus.addMenu("&Editar")

        self.doc = QTextEdit()        # doc es el area de texto principal
        self.setCentralWidget(self.doc)

        # Reconocimiento de voz
        self.escuchando = False
        self.hilo_voz = None
        self.recognizer = sr.Recognizer()
        # Conectar la señal para procesar texto desde el hilo de reconocimiento
        self.recognized_text.connect(self.procesarTextoVoz)


        # Crear acciones usando el nuevo 
        actionNuevoArchivo = self.crearAccion(
            "&Nuevo Archivo",
            QIcon.fromTheme("document-new"),
            "Ctrl+N",
            "Crear un nuevo archivo",
            self.nuevoArchivo
        )

        self.nombreArchivoActual = "Sin título"

        actionAbrirArchivo = self.crearAccion(
            "&Abrir Archivo",
            QIcon.fromTheme("document-open"),
            "Ctrl+A",
            "Abrir un archivo existente",
            self.AbrirArchivo
        )
        
        actionGuardarArchivo = self.crearAccion(
            "&Guardar Archivo",
            QIcon.fromTheme("document-save"),
            "Ctrl+S",
            "Guardar el archivo actual",
            self.GuardarArchivo
        )

        actionDeshacer = self.crearAccion(
            "&Deshacer",
            QIcon.fromTheme("edit-undo"),
            "Ctrl+Z",
            "Deshacer la última acción",
            self.doc.undo
        )

        actionRehacer = self.crearAccion(
            "&Rehacer",
            QIcon.fromTheme("edit-redo"),
            "Ctrl+Y",
            "Rehacer la última acción deshecha",
            self.doc.redo
        )

        actionCortar = self.crearAccion(
            "&Cortar",
            QIcon.fromTheme("edit-cut"),
            "Ctrl+X",
            "Cortar el texto seleccionado",
            self.doc.cut
        )

        actionCopiar = self.crearAccion(
            "&Copiar",
            QIcon.fromTheme("edit-copy"),
            "Ctrl+C",
            "Copiar el texto seleccionado",
            self.doc.copy
        )

        actionPegar = self.crearAccion(
            "&Pegar",
            QIcon.fromTheme("edit-paste"),
            "Ctrl+V",
            "Pegar desde el portapapeles",
            self.doc.paste
        )

        actionBuscar = self.crearAccion(
            "&Buscar",
            QIcon.fromTheme("edit-find"),
            "Ctrl+F",
            "Buscar texto en el documento",
            self.mostrarDockBuscar
        )

        actionReemplazar = self.crearAccion(
            "&Reemplazar",
            QIcon.fromTheme("edit-find-replace"),
            "Ctrl+H",
            "Reemplazar texto en el documento",
            self.reemplazarTexto
        )

        actionSalir = self.crearAccion(
            "&Salir",
            QIcon.fromTheme("application-exit"),
            "Ctrl+Q",
            "Salir de la aplicación",
            self.salir
        )

        # Agregamos la accion a los menus correspondientes
        archivo.addAction(actionNuevoArchivo)
        archivo.addAction(actionAbrirArchivo)
        archivo.addAction(actionGuardarArchivo)
        archivo.addSeparator()
        archivo.addAction(actionSalir)

        editar.addAction(actionDeshacer)
        editar.addAction(actionRehacer)
        editar.addSeparator()
        editar.addAction(actionCortar)
        editar.addAction(actionCopiar)
        editar.addAction(actionPegar)

        # Barra de herramientas Doc
        toolbar = QToolBar("Barra de herramientas 1")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # Barra de herramientas texto
        # === Barra de formato (debajo de la principal) ===
        toolbarFormato = QToolBar("Formato de Texto", self)
        toolbarFormato.setMovable(False)
        toolbarFormato.setFloatable(False)
        toolbarFormato.setIconSize(QSize(20, 20))
        toolbarFormato.setFixedHeight(40)
        toolbarFormato.setToolButtonStyle(Qt.ToolButtonIconOnly)

        ## agregar acciones a la barra de herramientas
        toolbar.addAction(actionNuevoArchivo)
        toolbar.addAction(actionAbrirArchivo)
        toolbar.addAction(actionGuardarArchivo)
        toolbar.addSeparator()
        toolbar.addAction(actionDeshacer)
        toolbar.addAction(actionRehacer)
        toolbar.addSeparator()
        toolbar.addAction(actionCortar)
        toolbar.addAction(actionCopiar)
        toolbar.addAction(actionPegar)
        toolbar.addSeparator()
        toolbar.addAction(actionBuscar)
        #toolbar.addAction(actionReemplazar)
        toolbar.addSeparator()
        toolbar.addAction(actionSalir)

        self.addToolBar(toolbar)

        # Dock para posicionar el texto
        self.dockWidget = QDockWidget("Editor de Texto", self)
        self.dockWidget.setTitleBarWidget(QWidget())  # Quita la barra de titulo del dock
        # Hacer que el dock se ponga a la derecha cuando le de a buscar texto
        self.dockWidget.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.dockWidget.setWidget(self.doc)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.doc = self.dockWidget.widget()

        # Dock para posicionar el buscar texto
        self.dockBuscar = QDockWidget("Buscar / Reemplazar", self)      # self para que sea hijo de la ventana principal
        self.dockBuscar.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockBuscar.setVisible(False)  # oculto al inicio
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockBuscar)
        self.dockBuscar.visibilityChanged.connect(self.cerrarDockBuscar)
        
        # Contenedor de busqueda
        contenedorBusqueda = QWidget()
        contenedorBusqueda.setFixedSize(300, 150)
        layout = QVBoxLayout()

        # Campo de búsqueda
        layoutBuscar = QHBoxLayout()
        layoutBuscar.addWidget(QLabel("Buscar:"))
        self.txtBuscar = QLineEdit()
        self.txtBuscar.setFixedWidth(150)
        layoutBuscar.addWidget(self.txtBuscar)
        layout.addLayout(layoutBuscar)

        # Campo de reemplazo
        layoutReemplazar = QHBoxLayout()
        layoutReemplazar.addWidget(QLabel("Reemplazar con:"))
        self.txtReemplazar = QLineEdit()
        self.txtReemplazar.setFixedWidth(150)
        layoutReemplazar.addWidget(self.txtReemplazar)
        layout.addLayout(layoutReemplazar)

        # Botones Buscar
        layoutBotones1 = QHBoxLayout()
        layoutBotones2 = QHBoxLayout()

        self.btnBuscarSiguiente = QPushButton("Buscar siguiente")
        self.btnBuscarSiguiente.setFixedSize(120, 30)
        layoutBotones1.addWidget(self.btnBuscarSiguiente)

        self.btnBuscarAnterior = QPushButton("Buscar anterior")
        self.btnBuscarAnterior.setFixedSize(120, 30)
        layoutBotones1.addWidget(self.btnBuscarAnterior)
        
        self.btnReemplazar = QPushButton("Reemplazar")
        self.btnReemplazarTodo = QPushButton("Reemplazar todo")
        self.btnReemplazar.setFixedSize(120, 30)
        self.btnReemplazarTodo.setFixedSize(120, 30)
        layoutBotones2.addWidget(self.btnReemplazar)
        layoutBotones2.addWidget(self.btnReemplazarTodo)

        layout.addLayout(layoutBotones1)
        layout.addLayout(layoutBotones2)

        contenedorBusqueda.setLayout(layout)
        self.dockBuscar.setWidget(contenedorBusqueda)

        self.txtBuscar.textChanged.connect(self.buscarPalabra)
        self.btnBuscarSiguiente.clicked.connect(self.buscarSiguientePalabra)
        self.btnBuscarAnterior.clicked.connect(self.buscarAnteriorPalabra)
        self.btnReemplazar.clicked.connect(self.reemplazarTexto)
        self.btnReemplazarTodo.clicked.connect(self.reemplazarTodoTexto)

        # Botones Formato
        self.btnFuente = self.crearBoton(
            QIcon.fromTheme("insert-text"),
            "Ctrl+T",
            "Cambiar tipografía y tamaño del texto",
            self.aplicarFuente
        )

        self.btnNegrita = self.crearBoton(
            QIcon.fromTheme("format-text-bold"),
            "Ctrl+B",
            "Poner en negrita el texto",
            self.aplicarNegrita
        )

        self.btnCursiva = self.crearBoton(
            QIcon.fromTheme("format-text-italic"),
            "Ctrl+I",
            "Poner en cursiva el texto",
            self.aplicarCursiva
        )
        
        self.btnSubrayado = self.crearBoton(
            QIcon.fromTheme("format-text-underline"),
            "Ctrl+U",
            "Poner subrayado al texto por debajo",
            self.aplicarSubrayadoDebajo
        )

        self.btnBackGround = self.crearBoton(
            QIcon.fromTheme("format-justify-fill"),
            "Ctrl+W",
            "Poner subrayado al texto de fondo",
            self.aplicarBackground
        )

        self.btnMicrofono = self.crearBoton(
            QIcon.fromTheme("media-record"),
            "Ctrl+M",
            "Activar/desactivar dictado por voz",
            self.toggleEscuchaVoz
        )

        # Agregar botones al toolbar de formato
        toolbarFormato.addWidget(self.btnFuente)
        toolbarFormato.addWidget(self.btnNegrita)
        toolbarFormato.addWidget(self.btnCursiva)
        toolbarFormato.addWidget(self.btnSubrayado)
        toolbarFormato.addWidget(self.btnBackGround)
        toolbarFormato.addWidget(self.btnMicrofono)

        # Añadir el toolbar debajo del principal
        self.addToolBarBreak(Qt.TopToolBarArea)  # Esto crea una "nueva fila"
        self.addToolBar(Qt.TopToolBarArea, toolbarFormato)

        # Crear el contador y establecer la barra de estado
        # palabras = 0

        # status = QStatusBar()
        # self.setStatusBar(status)
        # self.statusBar().showMessage(f"Palabras: {palabras}")
        # # Conectar la señal textChanged del QTextEdit a la función actualizarContadorPalabras
        # self.doc.textChanged.connect(self.actualizarContadorPalabras)
        self.contador = WordCounterWidget(wpm=200, mostrarPalabras=True, mostrarCaracteres=True, mostrarTiempoLectura=True)
        self.setStatusBar(QStatusBar())
        self.statusBar().addPermanentWidget(self.contador)
        self.doc.textChanged.connect(lambda: self.contador.update_from_text(self.doc.toPlainText()))
        self.contador.update_from_text(self.doc.toPlainText())

        # Inicializaciones necesarias para la búsqueda/resaltado
        self.last_match_range = None
        self.formatoNormal = QTextCharFormat()
        self.formatoNormal.setBackground(QColor(0, 0, 0, 0))
        self.formatoResaltado = QTextCharFormat()
        self.formatoResaltado.setBackground(QColor("magenta"))
        self.textoAnterior = ""

    # Funcion para crear acciones
    def crearAccion(self, nombre, icono, atajo, ayuda, metodo):
        accion = QAction(nombre, self)
        accion.setIcon(icono)
        accion.setShortcut(QKeySequence(atajo))
        accion.setWhatsThis(ayuda)
        accion.triggered.connect(metodo)
        return accion
    
    # Funcion para crear botones
    def crearBoton(self, icono, atajo, ayuda, metodo):
        boton = QPushButton("")
        boton.setIcon(icono)
        boton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 4px;
            }
            QPushButton:checked {
                background-color: grey;
            }
            QPushButton:hover {
                background-color: grey;
            }
        """)
        boton.setFixedSize(25, 25)
        boton.setShortcut(QKeySequence(atajo))
        boton.setCheckable(True)  # Permite activar/desactivar el formato
        boton.setWhatsThis(ayuda)
        boton.clicked.connect(metodo)
        return boton
    
    # PopUps
    def popUpNew(self):
        # Si hay texto en el documento actual
        if self.doc.toPlainText().strip():
            # Mostrar diálogo de confirmación
            respuesta = QMessageBox.question(
                self,
                "Guardar cambios",
                "¿Deseas guardar los cambios antes de crear un nuevo archivo?",
                QMessageBox.Yes | QMessageBox.No
            )

            if respuesta == QMessageBox.Yes:
                # Guardar el archivo
                self.GuardarArchivo()
                # Luego limpiar el documento
                self.doc.clear()
                self.nombreArchivoActual = "Sin título"
                self.statusBar().showMessage("Nuevo archivo creado.")
                return
            
             # Cancelar la acción
            self.statusBar().showMessage("Acción cancelada.")
            self.doc.clear()
            return
        
    def popUpExit(self):
        # Si hay texto en el documento actual
        if self.doc.toPlainText().strip():
            # Mostrar diálogo de confirmación
            respuesta = QMessageBox.question(
                self,
                "Guardar cambios",
                "¿Deseas guardar los cambios antes de salir?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if respuesta == QMessageBox.Yes:
                # Salir y guardar
                self.GuardarArchivo()
                return "exit1"
            elif respuesta == QMessageBox.No:
                 # Cancelar la acción
                return "exit2"

            return "can"

    # Creacion de metodos para las acciones
    def nuevoArchivo(self):
        respuesta = self.popUpNew()
        
    def AbrirArchivo(self):
        ruta = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Archivos de texto (*.txt);;Todos los archivos (*)")  # Literalmente lo pone en la documentacion :/
        
        if ruta[0]: # El 0 contiene la ruta completa del archivo que ha elegido el usuario, el 1 es el filtro seleccionado, si no se selecciona nada, ruta[0] es una cadena vacia
            self.nombreArchivoActual = ruta[0]
            with open(ruta[0], 'r', encoding="utf-8") as archivo:
                contenido = archivo.read()
                self.doc.setText(contenido)

    def GuardarArchivo(self):
        ruta = QFileDialog.getSaveFileName(self, "Guardar Archivo", self.nombreArchivoActual, "Archivos de texto (*.txt);;Todos los archivos (*)")
        if ruta[0]:
            with open(ruta[0], 'w') as archivo:
                contenido = self.doc.toPlainText()
                archivo.write(contenido)


    def mostrarDockBuscar(self):
        self.dockBuscar.setVisible(True)
        self.txtBuscar.setFocus()
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockBuscar)

    def marcarBackGround(self, cursor, color):
        formatoResaltado = QTextCharFormat()
        formatoResaltado.setBackground(QColor(color))
        cursor.mergeCharFormat(formatoResaltado)

    def limpiarResaltados(self):
        doc = self.doc.document()
        # Si tenemos una coincidencia conocida, limpiarla específicamente
        if self.last_match_range:
            cursor = QTextCursor(doc)
            start, end = self.last_match_range
            cursor.setPosition(start)
            cursor.setPosition(end, QTextCursor.KeepAnchor)
            if not self.formatoNormal:
                self.formatoNormal = QTextCharFormat()
                self.formatoNormal.setBackground(QColor(0, 0, 0, 0))
            cursor.mergeCharFormat(self.formatoNormal)
            self.last_match_range = None
            return

        # Si no hay coincidencia guardada, limpiar todo el documento
        cursor = QTextCursor(doc)
        cursor.beginEditBlock()

        formatoLimpio = QTextCharFormat()
        formatoLimpio.setBackground(QColor(0, 0, 0, 0))

        cursor.select(QTextCursor.Document)
        cursor.mergeCharFormat(formatoLimpio)

        cursor.endEditBlock()
        self.doc.moveCursor(QTextCursor.Start)

    def resaltarTodasCoincidencias(self, texto_buscar):
        self.limpiarResaltados()
        if not texto_buscar:
            return

        cursor = self.doc.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.doc.setTextCursor(cursor)

        while True:
            nuevo_cursor = self.doc.document().find(texto_buscar, cursor)
            if nuevo_cursor.isNull():
                break
            self.marcarBackGround(nuevo_cursor, "magenta")
            cursor = nuevo_cursor

    # Busca la primera aparicion de la palabra en el documento
    def buscarPalabra(self, cursor=None):
        # Limpiamos y resaltamos todas las coincidencias primero
        self.limpiarResaltados()
        texto_buscar = self.txtBuscar.text().strip()
        self.resaltarTodasCoincidencias(texto_buscar)

        if not texto_buscar:
            return

        # Si nos llaman pasando un QTextCursor (desde Buscar siguiente/anterior),
        # lo usaremos como punto de partida. Si no (por ejemplo textChanged),
        # creamos uno temporal desde el inicio del documento.
        if isinstance(cursor, QTextCursor):
            start_cursor = cursor
            called_from_buttons = True
        else:
            start_cursor = self.doc.textCursor()
            start_cursor.movePosition(QTextCursor.Start)
            called_from_buttons = False

        # Buscar a partir del cursor de inicio
        nuevo_cursor = self.doc.document().find(texto_buscar, start_cursor)

        if not nuevo_cursor.isNull():
            # Mover el cursor visible al resultado
            self.doc.setTextCursor(nuevo_cursor)
            self.doc.ensureCursorVisible()      # Scrolea solo hasta la primera aparición
            self.marcarBackGround(nuevo_cursor, "magenta")
            self.last_match_range = (nuevo_cursor.selectionStart(), nuevo_cursor.selectionEnd())

            # Si la búsqueda vino desde los botones, damos foco al QTextEdit
            # Si vino por textChanged, dejamos el foco en el QLineEdit (para poder seguir escribiendo)
            if called_from_buttons:
                self.doc.setFocus()
            else:
                # mantenemos el foco en el QLineEdit
                self.txtBuscar.setFocus()
        else:
            self.statusBar().showMessage("No se encontró el texto.")

    # usar buscarPalabra para buscar la siguiente palabra
    def buscarSiguientePalabra(self):
        texto_buscar = self.txtBuscar.text().strip()
        if not texto_buscar:
            self.statusBar().showMessage("Ingrese texto para buscar.")
            return

        cursor_actual = self.doc.textCursor()

        # Determinar desde dónde empezar la búsqueda
        if cursor_actual.hasSelection():
            # Si hay selección, empezamos justo después de la coincidencia actual
            nueva_pos = cursor_actual.selectionEnd()
            cursor_inicio = QTextCursor(self.doc.document())
            cursor_inicio.setPosition(nueva_pos)
        else:
            # Si no hay selección, empezar desde la posición actual del cursor
            cursor_inicio = cursor_actual

        # Llamar a buscarPalabra pasando el cursor de inicio
        self.buscarPalabra(cursor_inicio)

        # Si no se encontró nada, hacer wrap al  (cuando llegamos al final del doc, volver al inicio)
        if self.last_match_range is None:
            cursor_inicio = QTextCursor(self.doc.document())
            cursor_inicio.movePosition(QTextCursor.Start)
            self.buscarPalabra(cursor_inicio)

    def buscarAnteriorPalabra(self):
        texto_buscar = self.txtBuscar.text().strip()
        if not texto_buscar:
            self.statusBar().showMessage("Ingrese texto para buscar.")
            return

        cursor_actual = self.doc.textCursor()

        # Determinar desde dónde empezar la búsqueda
        if cursor_actual.hasSelection():
            # Si hay selección, empezamos justo antes de la coincidencia actual
            nueva_pos = cursor_actual.selectionStart()
            cursor_inicio = QTextCursor(self.doc.document())
            cursor_inicio.setPosition(nueva_pos)
        else:
            cursor_inicio = cursor_actual

        # Buscar hacia atrás
        nuevo_cursor = self.doc.document().find(texto_buscar, cursor_inicio, QTextDocument.FindBackward)

        if not nuevo_cursor.isNull():
            self.doc.setTextCursor(nuevo_cursor)
            self.marcarBackGround(nuevo_cursor, "magenta")
            self.last_match_range = (nuevo_cursor.selectionStart(), nuevo_cursor.selectionEnd())
        else:
            # Si no se encuentra nada, hacer wrap al final del documento
            cursor_final = QTextCursor(self.doc.document())
            cursor_final.movePosition(QTextCursor.End)
            nuevo_cursor = self.doc.document().find(texto_buscar, cursor_final, QTextDocument.FindBackward)
            if not nuevo_cursor.isNull():
                self.doc.setTextCursor(nuevo_cursor)
                self.marcarBackGround(nuevo_cursor, "magenta")
                self.last_match_range = (nuevo_cursor.selectionStart(), nuevo_cursor.selectionEnd())
            else:
                self.statusBar().showMessage("No se encontró el texto.")
        
    def reemplazarTexto(self):
        texto_reemplazar = self.txtReemplazar.text()
        cursor = self.doc.textCursor()

        if cursor.hasSelection():
            cursor.insertText(texto_reemplazar)
            self.doc.setTextCursor(cursor)  # Actualizar el cursor en el doc
            cursor.mergeCharFormat(self.formatoNormal)
            self.limpiarResaltados()
        else:
            self.statusBar().showMessage("No hay texto seleccionado para reemplazar.")

    def reemplazarTodoTexto(self):
        # Obtener los textos de búsqueda y reemplazo
        texto_buscar = self.txtBuscar.text().strip()
        texto_reemplazar = self.txtReemplazar.text()

        if not texto_buscar:
            self.statusBar().showMessage("Ingrese texto para buscar.")
            return

        # Texto original y sus versiones en minúsculas para búsqueda insensible a mayúsculas
        contenido = self.doc.toPlainText()
        contenido_lower = contenido.lower()
        texto_buscar_lower = texto_buscar.lower()

        # Inicializamos el nuevo contenido y la posición de inicio del bucle
        nuevo_contenido = ""
        posicion_actual = 0

        while True:
            # Buscar la siguiente coincidencia desde la posición actual
            indice = contenido_lower.find(texto_buscar_lower, posicion_actual)

            if indice == -1:
                # No hay más coincidencias, agregamos el resto del contenido
                for i in range(posicion_actual, len(contenido)):
                    nuevo_contenido += contenido[i]
                break

            # Agregar caracteres desde la posición actual hasta el inicio de la coincidencia
            for i in range(posicion_actual, indice):
                nuevo_contenido += contenido[i]

            # Agregar el texto de reemplazo
            nuevo_contenido += texto_reemplazar

            # Avanzar la posición actual después de la coincidencia
            posicion_actual = indice + len(texto_buscar)

        # Actualizar el contenido del documento y limpiar resaltados
        self.doc.setText(nuevo_contenido)
        self.limpiarResaltados()

    def cerrarDockBuscar(self, visible: bool):
        if not visible:
            self.limpiarResaltados()

    def salir(self):
        respuesta = self.popUpExit()

        if respuesta == "exit":
            self.close()
        elif respuesta == "cancel":
            self.statusBar().showMessage("Salida cancelada.")
        else:
            self.close()
    
    """
    # Evento para el cierre de la app
    def closeEvent(self, event):
        respuesta = self.popUpExit()

        if respuesta == "exit1" or respuesta == "exit2":
            event.accept()         # se cierra
        else:
            event.ignore()         # no se cierra
    """

    # Funcion para contar palabras
    def contarPalabras(self):
        texto = self.doc.toPlainText()
        listaPalabras = texto.split()
        return len(listaPalabras)
    
    def actualizarContadorPalabras(self):
        self.palabras = self.contarPalabras()
        self.statusBar().showMessage(f"Palabras: {self.palabras}")

    def aplicarFuente(self):
        # Abrir el diálogo de selección de fuente
        ok, fuente = QFontDialog.getFont(self)

        if not ok:  # Si el usuario cancela
            return

        cursor = self.doc.textCursor()

        # Crear el formato con la fuente seleccionada
        formato = QTextCharFormat()
        formato.setFont(fuente)

        if cursor.hasSelection():
            # Aplicar solo a la selección
            cursor.mergeCharFormat(formato)
        else:
            # Aplicar al formato actual (para texto nuevo)
            self.doc.mergeCurrentCharFormat(formato)

    def aplicarNegrita(self):
        cursor = self.doc.textCursor()
        formato = QTextCharFormat()
        formato.setFontWeight(QFont.Bold if self.btnNegrita.isChecked() else QFont.Normal)
        cursor.mergeCharFormat(formato)

        if cursor.hasSelection():
            cursor.mergeCharFormat(formato)
        else:
            self.doc.mergeCurrentCharFormat(formato)

    def aplicarCursiva(self):
        cursor = self.doc.textCursor()
        formato = QTextCharFormat()
        formato.setFontItalic(self.btnCursiva.isChecked())

        if cursor.hasSelection():
            cursor.mergeCharFormat(formato)
        else:
            self.doc.mergeCurrentCharFormat(formato)

    def aplicarSubrayadoDebajo(self):
        cursor = self.doc.textCursor()
        formato = QTextCharFormat()
        formato.setFontUnderline(self.btnSubrayado.isChecked())
        cursor.mergeCharFormat(formato)

        if cursor.hasSelection():
            cursor.mergeCharFormat(formato)
        else:
            self.doc.mergeCurrentCharFormat(formato)

    def aplicarBackground(self):
        # Abrir diálogo de color
        color = QColorDialog.getColor(QColor("yellow"), self, "Seleccionar color de fondo")

        if not color.isValid():
            formatoLimpio = QTextCharFormat()
            formatoLimpio.setBackground(QColor(0, 0, 0, 0))
            self.doc.mergeCurrentCharFormat(formatoLimpio)
            return  # Si el usuario cancela el diálogo

        cursor = self.doc.textCursor()

        if cursor.hasSelection():
            # Aplicar color solo al texto seleccionado
            self.marcarBackGround(cursor, color)
        else:
            # Si no hay selección, aplicarlo como formato actual
            formato = QTextCharFormat()
            formato.setBackground(color)
            self.doc.mergeCurrentCharFormat(formato)
    
    def toggleEscuchaVoz(self):
        if not self.escuchando:
            self.escuchando = True
            self.statusBar().showMessage("🎤 Escuchando... Pulsa el micrófono otra vez para detener.")
            self.btnMicrofono.setChecked(True)

            # Lanzamos el hilo de escucha
            self.hilo_voz = threading.Thread(target=self.esucharPorVoz, daemon=True)
            self.hilo_voz.start()

        else:
            self.escuchando = False
            self.statusBar().showMessage("Micrófono desactivado.")
            self.btnMicrofono.setChecked(False)

    def esucharPorVoz(self):
        with sr.Microphone() as source:
            # Ajustar ruido ambiente
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            while self.escuchando:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    texto = self.recognizer.recognize_google(audio, language="es-ES")

                    # Emitir la señal para procesar el texto en el hilo principal (seguro para GUI)
                    self.recognized_text.emit(texto)

                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    self.statusBar().showMessage("Error al conectar con el servicio de voz.")
                    break

    def procesarTextoVoz(self, texto):
        # Normalizar texto: pasar a minúsculas, quitar acentos y signos de puntuación
        texto_norm = texto.lower().strip()
        texto_norm = unicodedata.normalize('NFD', texto_norm)
        texto_norm = ''.join(ch for ch in texto_norm if unicodedata.category(ch) != 'Mn')
        texto_norm = re.sub(r"[^\w\s]", "", texto_norm)
        texto_norm = re.sub(r"\s+", " ", texto_norm).strip()

        # Mapear comandos a botones y métodos
        comandos = {
            "negrita": (self.btnNegrita, self.aplicarNegrita),
            "cursiva": (self.btnCursiva, self.aplicarCursiva),
            "subrayado": (self.btnSubrayado, self.aplicarSubrayadoDebajo)
        }

        #palabras_on = ["activar", "encender", "poner", "iniciar", "abrir"]
        #palabras_off = ["desactivar", "apagar", "quitar", "cerrar"]

        # Procesar comandos de formato con soporte ON/OFF explícito
        for palabra, (boton, metodo) in comandos.items():
            if palabra in texto_norm:
                '''if any(p in texto_norm for p in palabras_off):
                    boton.setChecked(False)
                    metodo()
                    self.statusBar().showMessage(f"Comando detectado: quitar {palabra}")
                    return
                elif any(p in texto_norm for p in palabras_on):
                    boton.setChecked(True)
                    metodo()
                    self.statusBar().showMessage(f"Comando detectado: activar {palabra}")
                    return
                else:'''
                # Sin indicación ON/OFF, alternar
                boton.toggle()
                metodo()
                self.statusBar().showMessage(f"Comando detectado: {palabra}")
                return

        # Guardar archivo
        if "guardar" in texto_norm:
            # Ejecutar guardado (seguro en hilo principal porque estamos en la señal)
            self.GuardarArchivo()
            self.statusBar().showMessage("Archivo guardado por comando de voz.")
            return

        # Nuevo documento
        if "nuevo documento" in texto_norm or texto_norm == "nuevo":
            self.nuevoArchivo()
            return

        # Si no es comando, escribir texto en el documento
        cursor = self.doc.textCursor()
        cursor.insertText(texto + " ")
        self.doc.setTextCursor(cursor)



if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()


""" Siempre que quieras ejecutar la función ahora mismo: ()

    En las variables 2 formas:
        def saludar():
            return "Hola!"

        x = saludar        # x apunta a la función
        y = saludar()      # y guarda el resultado ("Hola!")

        print(x)  # ➜ <function saludar at 0x...>
        print(x())  # ➜ Hola!
        print(y)  # ➜ Hola!
"""
