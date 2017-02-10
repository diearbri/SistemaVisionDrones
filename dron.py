def moverY(tipo):
    global posDronZ
    global posDronX
    global posDronY
    global ts
    global maxDesplamiento
    cont = 0
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            posDronY=posDronY-0.05
        elif tipo == 0:
            posDronY=posDronY+0.05
        vrep.simxSetObjectPosition(clientID,dron,-1,(posDronX,posDronY,posDronZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def moverX(tipo):
    global posDronZ
    global posDronX
    global posDronY
    global ts
    global maxDesplamiento
    cont = 0
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            posDronX=posDronX+0.05
        elif tipo == 0:
            posDronX=posDronX-0.05
        vrep.simxSetObjectPosition(clientID,dron,-1,(posDronX,posDronY,posDronZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def addCola(cola , element):
    cont = 0
    for i in cola:
        cont=cont+1
    if cont<5:
        cola.append(element)
    else:
        cola.popleft()
        cola.append(element)
    return cola

def sumCola(cola):
    acum = 0
    for i in cola:
        acum=acum+abs(i)
    return acum

def countCola(cola):
    cont = 0
    for i in cola:
        cont=cont+1
    return cont

def printCola(cola,coord):
    print("+++++++++Inicia "+coord)
    for i in cola:
        print(str(i))
    print("---------FIN "+coord)

def create(name):

    try:
        if(os.path.isfile(name)):
            os.remove(name)
            file=open(name,'a')
            file.close()
    except:
            print("error occured")
            sys.exit(0)


def escribir(name, posicion):
    archivo = open(name, "a")
    archivo.write(posicion+'\n')
    archivo.close()

from collections import deque
from Tkinter import *
import vrep
import sys
import math
import time
import cv2
import numpy as np
import sys
import os

ts=0.3
width=256
height=256
maxDesplamiento = 2
nameArchTrack="Tracking.txt"

bordeT = 100

vrep.simxFinish(-1)

clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID != -1:
    print('Conexion Exitosa')
else:
    print('Conexion Fallida')
    sys.exit('No se pudo Conectar')

create(nameArchTrack)
erroCode,dron = vrep.simxGetObjectHandle(clientID,'Quadricopter_target',vrep.simx_opmode_oneshot_wait)
erroCode,camara = vrep.simxGetObjectHandle(clientID,'Vision_sensor_front',vrep.simx_opmode_oneshot_wait)   #'Quadricopter_frontCamera'   Vision_sensor
#erroCode,gps = vrep.simxGetObjectHandle(clientID,'GPS_reference',vrep.simx_opmode_oneshot_wait)
_,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_streaming)

time.sleep(2)
# Inicializamos el primer frame a vac?o.
# Nos servir? para obtener el fondo
fondo = None
coordX0 = 0
coordY0 = 0
coordX = 0
coordY = 0
coordXAnt = 0
coordYAnt = 0
cont = 1
#cola_x = deque()
#cola_y = deque()
# Recorremos todos los frames
while True:
    if cont<10:
        positionDron=vrep.simxGetObjectPosition(clientID,dron,-1,vrep.simx_opmode_oneshot)
        posDronX=positionDron[1][0]
        posDronY=positionDron[1][1]
        posDronZ = positionDron[1][2]
        print(str(posDronX)+"  "+str(posDronY)+"  "+str(posDronZ)+"  ")
    cont=cont+1
    # Obtenemos el frame
    #(grabbed, frame) = camara.read()
    _,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_buffer)
    #coordenadasGps=vrep.simxGetObjectPosition(clientID,gps,-1,vrep.simx_opmode_oneshot)
    #print(resolution)
    img = np.array(image,dtype=np.uint8)
    img.resize(width, height, 3)
    #img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img1 = np.fliplr(img)

    img2 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    frame = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    cv2.imshow('camaraDron', img2)
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
    umbral = cv2.threshold(resta, 125, 225, cv2.THRESH_BINARY)[1]
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
        #print("(x, y, w, h)=="+str(x)+","+str(y)+","+str(w)+","+str(h))
        # Dibujamos el rect?ngulo del bounds
        if w<254 and h<254:
            cv2.rectangle(frame, (x, y), (x + w, y + h) , (0, 255, 0), 2)
            coordX = x+w/2
            coordY = y+h/2
            moverXBool = 1
            moverYBool = 1
            print("coord X, Y "+str(coordX)+" , "+str(coordY))
            if coordX>bordeT and coordX<(width-bordeT):
                print("**No Mover X")
                coordXAnt = coordX
                moverXBool = 0
            if coordY>bordeT and coordY<(width-bordeT):
                print("**No Mover Y")
                coordYAnt = coordY
                moverYBool = 0
            #print("coordAnt X, Y "+str(coordXAnt)+" , "+str(coordYAnt))
            #if coordXAnt!=0:
            #    addCola(cola_x,coordX-coordXAnt)
            #if coordYAnt!=0:
            #    addCola(cola_y,coordY-coordYAnt)

            if ((moverXBool or moverYBool)):
                #print("************************************")
                #printCola(cola_x,"X")
                #printCola(cola_y,"Y")
                #print("SUM X,Y "+str(sumCola(cola_x))+" , "+str(sumCola(cola_y)))
              #  factor=2
                if moverXBool and coordX!=coordXAnt:
                    if coordX<bordeT:
                        print("Mover X atras")
                        moverX(0)#atras

                    else:
                        print("Mover X adelante")
                        moverX(1)#sube

                if moverYBool and coordY!=coordYAnt:
                    if coordY<bordeT:
                        print("Mover Y sube")
                        moverY(0)#sube
                    else:
                        print("Mover Y baja")
                        moverY(1)#baja
              #  escribir(nameArchTrack,str(coordenadasGps[1][0])+", "+str(coordenadasGps[1][1])+", "+str(coordenadasGps[1][2]))
             #   cola_x = deque()
             #   cola_y = deque()
                coordX = 0
                coordY = 0
            coordXAnt = coordX
            coordYAnt = coordY



            ##if (coordX<bordeT) and (coordX>width-bordeT)
    # Mostramos las im?genes de la c?mara, el umbral y la resta
    cv2.imshow("DeteccionBuque", frame)
    #cv2.imshow("Umbral", umbral)
    #cv2.imshow("Resta", resta)
    #cv2.imshow("Contorno", contornosimg)
    # Tiempo de espera para que se vea bien 0.1
    time.sleep(0.1)
    # Si ha pulsado la letra esc, salimos
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break;
# Liberamos la c?mara y cerramos todas las ventanas
#camara.release()
cv2.destroyAllWindows()


