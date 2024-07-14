# yoloBlind

# Detección de Objetos y Descripción por Voz

Este proyecto utiliza OpenCV, YOLO (You Only Look Once) y `pyttsx3` para detectar objetos en imágenes capturadas por una cámara y describirlos por voz. El sistema es ideal para ayudar a personas con discapacidad visual a identificar objetos en su entorno.

## Requisitos

- Python 3.x
- OpenCV
- pyttsx3
- NumPy
- pytesseract
- YOLOv3 (pesos y configuraciones)

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/maxbot86/yoloBlind.git
    cd yoloBlind
    ```

2. Instala las dependencias:
    ```bash
    pip install opencv-python pyttsx3 numpy
    ```

3. Descarga los archivos de configuración y pesos de YOLOv3 y colócalos en el directorio del proyecto:
    - `yolov3.weights` (se debera descargar de internet)
    - `yolov3.cfg`
    - `cocoES.names` (archivo con los nombres de las clases en español)

## Uso

1. Ejecuta el script principal:
    ```bash
    python main.py
    ```

2. Selecciona la cámara que deseas utilizar de la lista de cámaras disponibles.

3. El sistema capturará frames de la cámara y realizará la detección de objetos. Cada vez que detecte un objeto, dirá su nombre en voz alta.

4. Para salir del programa, presiona la tecla `q`.

## Explicación del Código

El script `main.py` realiza los siguientes pasos:

1. **Inicialización**:
    - Se importan las bibliotecas necesarias.
    - Se define una función `list_cameras` para listar las cámaras disponibles.
    - Se define una función `select_camera` para permitir al usuario seleccionar una cámara.

2. **Configuración de `pyttsx3`**:
    - Se inicializa el motor de texto a voz `pyttsx3` y se configura la voz en español.

3. **Carga de YOLO**:
    - Se cargan los pesos y configuraciones de YOLOv3.
    - Se cargan los nombres de las clases desde el archivo `cocoES.names`.( se puede usar `cocoEN.names` si lo desea en ingles)

4. **Selección de la Cámara**:
    - El usuario selecciona la cámara a utilizar.

5. **Captura de Video**:
    - Se inicia la captura de video desde la cámara seleccionada.
    - En cada frame capturado, se realiza la detección de objetos utilizando YOLO.

6. **Detección y Descripción**:
    - Si se presiona la tecla `d`, se realiza la detección de objetos en el frame actual.
    - Se dibujan rectángulos alrededor de los objetos detectados y se muestra su nombre.
    - Se utiliza `pyttsx3` para decir el nombre del objeto en voz alta.
    - Se guarda la imagen con las detecciones en un archivo con timestamp.

7. **Salida**:
    - Se muestra la imagen con las detecciones en una ventana.
    - El usuario puede salir del programa presionando la tecla `q`.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Para más detalles, consulta el archivo `LICENSE`.
