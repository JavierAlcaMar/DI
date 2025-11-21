# 📝 Mini Word

**Mini Word** es un editor de texto ligero desarrollado con **PySide6 (Qt for Python)**.
Incluye funcionalidades básicas de edición, búsqueda, reemplazo y formato de texto, con una interfaz gráfica moderna y fácil de usar.

---

## 🚀 Características principales

✅ **Gestión de archivos**

* Crear nuevos documentos
* Abrir archivos `.txt`
* Guardar con nombre personalizado
* Confirmación para guardar cambios antes de salir

✅ **Edición básica**

* Deshacer / Rehacer
* Cortar, Copiar, Pegar

✅ **Búsqueda y reemplazo**

* Panel lateral tipo *dock* para buscar y reemplazar texto
* Resaltado automático de coincidencias
* Función de “Buscar siguiente” y “Reemplazar todo”

✅ **Formato de texto**

* Cambiar fuente y tamaño
* Aplicar **negrita**, *cursiva*, y *subrayado*
* Seleccionar color de fondo del texto
* Botones con iconos en una barra de formato

✅ **Interfaz**

* Barras de herramientas personalizadas
* Contador de palabras en la barra de estado
* Diálogos de confirmación al crear o cerrar archivos
* Diseño adaptable con *dock widgets*

---

## ⚙️ Requisitos

* **Python 3.8+**
* **PySide6**

---

## 🛠️ Instalación y entorno de desarrollo

Para trabajar con **Mini Word** de forma segura y reproducible, se recomienda usar **pipenv**, que gestiona un entorno virtual y las dependencias del proyecto.

### 1️⃣ Crear el entorno virtual

En la carpeta del proyecto:

```bash
pipenv --python 3
```

Esto creará un entorno virtual específico para este proyecto y generará un `Pipfile` para controlar las dependencias.

---

### 2️⃣ Activar el entorno virtual

Para entrar en el entorno virtual:

```bash
pipenv shell
```

Verás que el prompt de la terminal muestra el nombre del entorno. Para salir del entorno:

```bash
deactivate
```

---

### 3️⃣ Instalar dependencias

Con el entorno activo, instala las librerías necesarias:

```bash
pipenv install PySide6 pyinstaller
```

Opcionalmente, si quieres usar Pillow para iconos o manipulación de imágenes:

```bash
pipenv install Pillow
```

---

### 4️⃣ Ejecutar la aplicación en desarrollo

Mientras estás en el entorno virtual:

```bash
python main.py
```

Esto ejecutará la aplicación sin necesidad de empaquetarla.

---

### 5️⃣ Crear un ejecutable para macOS

Para generar una aplicación nativa `.app` en macOS, usando PyInstaller:

```bash
pyinstaller \
  --windowed \
  --name MiniWord \
  --icon=imagesMO/iconoApp.icns \
  --add-data "imagesMO:imagesMO" \
  main.py
```

* `--windowed` → Evita que se abra la terminal junto con la app.
* `--name MiniWord` → Nombre de la aplicación.
* `--icon` → Icono de la ventana principal (debe ser `.icns` en macOS).
* `--add-data` → Incluye la carpeta de imágenes dentro del ejecutable.

El resultado se encontrará en:

```
dist/MiniWord.app
```

Y podrás abrir la aplicación como cualquier otra app de macOS.

---

### 6️⃣ Reproducir el entorno en otra máquina

Si se comparte el proyecto, basta con clonar el repositorio y ejecutar:

```bash
pipenv install
pipenv shell
python main.py
```

Esto asegura que se instalen las mismas versiones de las dependencias definidas en el `Pipfile.lock`.

---

## 📂 Estructura del proyecto

```
mini-word/
│── (otros ejercicios)
├── main.py                  # Código principal de la aplicación
├── imagesMO/
│   ├── iconoApp.icns        # Icono de la ventana principal
│   └── logo.png             # Imagen de ejemplo para la interfaz
├── Pipfile                  # Gestión de dependencias
└── README.md                # Documentación del proyecto
```

---

## 💡 Funciones destacadas del código

* **crearAccion()** → Simplifica la creación de acciones con atajos e iconos.
* **crearBoton()** → Genera botones de formato personalizados con efectos hover.
* **buscarPalabra() / reemplazarTexto()** → Implementan la lógica de búsqueda avanzada con resaltado.
* **aplicarFuente(), aplicarNegrita(), aplicarCursiva(), aplicarBackground()** → Controlan el formato del texto.
* **popUpNew() y popUpExit()** → Muestran ventanas emergentes para guardar antes de crear o cerrar archivos.

---

## 🧑‍💻 Autor

**Desarrollado por:** *[Javier Alcaraz Martín]*
💼 Proyecto educativo desarrollado con **PySide6** en **Python**.

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.
Consulta el archivo [LICENSE](LICENSE) para más detalles.
