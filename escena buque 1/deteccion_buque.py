from Tkinter import *

import vrep
import sys
import math
import time
import cv2
import numpy as np

posZ = 1.500
x=-1.125
y=3.975
ts=0.5
maxDesplamiento = 5;
vrep.simxFinish(-1)

clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID != -1:
    print('Conexion Exitosa')
else:
    print('Conexion Fallida')
    sys.exit('No se pudo Conectar')

erroCode,dron = vrep.simxGetObjectHandle(clientID,'Quadricopter_target',vrep.simx_opmode_oneshot_wait)
erroCode,camara = vrep.simxGetObjectHandle(clientID,'Vision_sensor_front',vrep.simx_opmode_oneshot_wait)   #'Quadricopter_frontCamera'   Vision_sensor
_,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_streaming)
# Inicializamos el primer frame a vac?o.
# Nos servir? para obtener el fondo
fondo = None
# Recorremos todos los frames
while True:
    # Obtenemos el frame
    #(grabbed, frame) = camara.read()
    _,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_buffer)
    img = np.array(image,dtype=np.uint8)
    img.resize(256, 256, 3)
    img1 = np.fliplr(img)
    img2 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    frame = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    cv2.imshow('Imge3', img2)
    # Si hemos llegado al final del v?deo salimos

    # Convertimos a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Aplicamos suavizado para eliminar ruido
    gris = cv2.GaussianBlur(gris, (21, 21), 0)
    # Si todav?a no hemos obtenido el fondo, lo obtenemos
    # Ser? el primer frame que obtengamos
    if fondo is None:
        fondo = gris
        continue
    # Calculo de la diferencia entre el fondo y el frame actual
    resta = cv2.absdiff(fondo, gris)
    # Aplicamos un umbral
    umbral = cv2.threshold(resta, 25, 255, cv2.THRESH_BINARY)[1]
    # Dilatamos el umbral para tapar agujeros
    umbral = cv2.dilate(umbral, None, iterations=2)
    # Copiamos el umbral para detectar los contornos
    contornosimg = umbral.copy()
    # Buscamos contorno en la imagen
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # Recorremos todos los contornos encontrados
    for c in contornos:
    # Eliminamos los contornos m?s peque?os
        if cv2.contourArea(c) < 500:
            continue
        # Obtenemos el bounds del contorno, el rect?ngulo mayor que engloba al contorno
        (x, y, w, h) = cv2.boundingRect(c)
        # Dibujamos el rect?ngulo del bounds
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Mostramos las im?genes de la c?mara, el umbral y la resta
    cv2.imshow("Camara", frame)
    cv2.imshow("Umbral", umbral)
    cv2.imshow("Resta", resta)
    cv2.imshow("Contorno", contornosimg)
    # Capturamos una tecla para salir
    key = cv2.waitKey(1) & 0xFF
    # Tiempo de espera para que se vea bien
    time.sleep(0.015)
    # Si ha pulsado la letra esc, salimos
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break;
# Liberamos la c?mara y cerramos todas las ventanas
#camara.release()
cv2.destroyAllWindows()