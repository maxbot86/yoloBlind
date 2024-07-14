import cv2
import numpy as np
import time
import sys
import pyttsx3

def list_cameras(max_cameras=4):
    """List available camera indices."""
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

def select_camera():
    """Prompt user to select a camera from available cameras."""
    available_cameras = list_cameras()
    if not available_cameras:
        print("No cameras found.")
        return None
    print("Available cameras:")
    for cam in available_cameras:
        print(f"Camera {cam}")
    camera_index = int(input("Select camera index: "))
    if camera_index in available_cameras:
        return camera_index
    else:
        print("Invalid selection.")
        return None


# Iniciar Engine de Pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0")

# Cargar YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Cargar los nombres de las clases
with open("cocoES.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


# Seleccionar la cámara
camera_index = select_camera()
if camera_index is None:
    sys.exit(1)
# Inicializar la webcam
try:
    cap = cv2.VideoCapture(camera_index)
except:
    cap = cv2.VideoCapture(0)


frame_count = 0
while True:
    # Capturar frame-by-frame
    ret, img = cap.read()
    if not ret:
        break
    height, width, channels = img.shape
    
    #if frame_count % 20 == 0:  # Realizar la detección cada 5 fotogramas
    if cv2.waitKey(5) & 0xFF == ord('d'):
        # Preparar la imagen para YOLO
        blob = cv2.dnn.blobFromImage(img, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Mostrar información en pantalla
        class_ids = []
        confidences = []
        boxes = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Objeto detectado
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Eliminar cajas duplicadas usando Non-Maximum Suppression
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                print(label)
                engine.say(label)
                engine.runAndWait()
                color = (255, 0, 0)  # Verde para el cuadro
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        
        # Guardar la imagen con las detecciones
        output_filename = "./saved/take-"+str(time.strftime("%Y%m%d_%H%M%S"))+".jpg"
        cv2.imwrite(output_filename, img)
        print(time.strftime("%Y-%m-%d %H:%M:%S"))

    # Mostrar la imagen en pantalla
    cv2.imshow("Image", img)
    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    #frame_count += 1
# Liberar la captura y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
