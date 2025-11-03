# 📝 Mini Word

**Mini Word** es un editor de texto ligero desarrollado con **PySide6 (Qt for Python)**.  
Incluye funcionalidades básicas de edición, búsqueda, reemplazo y formato de texto, con una interfaz gráfica moderna y fácil de usar.

![image alt](https://github.com/JavierAlcaMar/DI/blob/53e54f77e2bd13619bd92f455f0ede5d1d6c7ec2/cap.png)

---

## 🚀 Características principales

✅ **Gestión de archivos**
- Crear nuevos documentos  
- Abrir archivos `.txt`  
- Guardar con nombre personalizado  
- Confirmación para guardar cambios antes de salir  

✅ **Edición básica**
- Deshacer / Rehacer  
- Cortar, Copiar, Pegar  

✅ **Búsqueda y reemplazo**
- Panel lateral tipo *dock* para buscar y reemplazar texto  
- Resaltado automático de coincidencias  
- Función de “Buscar siguiente” y “Reemplazar todo”  

✅ **Formato de texto**
- Cambiar fuente y tamaño  
- Aplicar **negrita**, *cursiva*, y _subrayado_  
- Seleccionar color de fondo del texto  
- Botones con iconos en una barra de formato  

✅ **Interfaz**
- Barras de herramientas personalizadas  
- Contador de palabras en la barra de estado  
- Diálogos de confirmación al crear o cerrar archivos  
- Diseño adaptable con *dock widgets*  

---

## ⚙️ Requisitos

- **Python 3.8+**  
- **PySide6**

Puedes instalar PySide6 con:
```bash
pip install PySide6
```

---

## ▶️ Ejecución

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tuusuario/mini-word.git
   ```
2. Entra al directorio del proyecto:
   ```bash
   cd mini-word
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

---

## 📂 Estructura del proyecto

```
mini-word/
│── (otros ejercicios)
├── main.py                  # Código principal de la aplicación
├── imagesMO/
│   └── iconoApp.png         # Icono de la ventana principal
└── README.md                # Documentación del proyecto
```

---

## 💡 Funciones destacadas del código

- **crearAccion()** → Simplifica la creación de acciones con atajos e iconos.  
- **crearBoton()** → Genera botones de formato personalizados con efectos hover.  
- **buscarPalabra() / reemplazarTexto()** → Implementan la lógica de búsqueda avanzada con resaltado.  
- **aplicarFuente(), aplicarNegrita(), aplicarCursiva(), aplicarBackground()** → Controlan el formato del texto.  
- **popUpNew() y popUpExit()** → Muestran ventanas emergentes para guardar antes de crear o cerrar archivos.  

---

## 🧑‍💻 Autor

**Desarrollado por:** *[Javier Alcaraz Martín]*  
💼 Proyecto educativo desarrollado con **PySide6** en **Python**.  

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.
