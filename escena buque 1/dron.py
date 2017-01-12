def moverY(tipo):
    global posDronZ
    global posDronX
    global posDronY
    global ts
    global maxDesplamiento
    cont = 0
    #while ( (y>=-4.70 and y<=2.25) and cont<=maxDesplamiento):
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            posDronY=posDronY+0.05
        elif tipo == 0:
            posDronY=posDronY-0.05
        vrep.simxSetObjectPosition(clientID,dron,-1,(posDronX,posDronY,posDronZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def moverX(tipo):
    global posDronZ
    global posDronX
    global posDronY
    global ts
    global maxDesplamiento
    cont = 0
    #while ( x>=-3.80 and x<=3.77 and cont<=maxDesplamiento):
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            posDronX=posDronX-0.05
        elif tipo == 0:
            posDronX=posDronX+0.05
        #print(str(x)+" : "+str(y)+" :"+str(posZ))
        vrep.simxSetObjectPosition(clientID,dron,-1,(posDronX,posDronY,posDronZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)




from Tkinter import *
import vrep
import sys
import math
import time
import cv2
import numpy as np

posDronZ = 4.000
posDronX=2.3750
posDronY=4.6500
ts=0.5
width=256
height=256
maxDesplamiento = 1;

bordeT = 100 #equivale un 40% del width y height con la finalidad de que el dron se mueva para mantener al barco en entre {47,211}por w,h

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
coordX = 0
coordY = 0
coordXAnt = 0
coordYAnt = 0
# Recorremos todos los frames
while True:
    # Obtenemos el frame
    #(grabbed, frame) = camara.read()
    _,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_buffer)
    img = np.array(image,dtype=np.uint8)
    img.resize(width, height, 3)

    img = np.rot90(img,2)
    img1 = np.fliplr(img)

    img2 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    frame = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    cv2.imshow('Imge2', img2)
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
        # Dibujamos el rect?ngulo del bounds
        if w<254 and h<254:
            cv2.rectangle(frame, (x, y), (x + w, y + h) , (0, 255, 0), 2)
            coordX = x+w/2
            coordY = y+h/2
            #print("coord  centro barco (X,Y) ("+str(coordX)+","+str(coordY)+") Se debe enviar al algoritmo Hungaryan")

            if(coordX<bordeT) and (coordX>width-bordeT):
                coordXAnt = coordX
                #coordYAnt = coordY
                #print("coord  centro barco (X,Y) ("+str(coordX)+","+str(coordY)+") Se debe enviar al algoritmo Hungaryan esta en el rago central")
            elif(coordY<bordeT) and (coordY>height -bordeT):
                coordYAnt = coordY
            print("coord  centro barco (X,Y) ("+str(coordX)+","+str(coordY)+") Se debe enviar al algoritmo Hungaryan esta en el rago central")
            #print(str(coordX)+" X "+str(coordXAnt))
            if coordXAnt != coordX:
                print("mover X")
                moverX(coordX>coordXAnt)
                if coordY > coordYAnt+10:
                    print("mover y")
                    coordYAnt = coordY
                    moverY(1)
                elif coordY < coordYAnt-10:
                    print("mover y")
                    coordYAnt = coordY
                    moverY(0)
            elif coordYAnt != coordY:
                print("mover y")
                moverY(coordY>coordYAnt)


            ##if (coordX<bordeT) and (coordX>width-bordeT)
    # Mostramos las im?genes de la c?mara, el umbral y la resta
    cv2.imshow("frameHSV", frame)
    #cv2.imshow("Umbral", umbral)
    #cv2.imshow("Resta", resta)
    #cv2.imshow("Contorno", contornosimg)
    # Tiempo de espera para que se vea bien
    time.sleep(0.05)
    # Si ha pulsado la letra esc, salimos
    k=cv2.waitKey(1) & 0xFF
    if k==27:
        break;
# Liberamos la c?mara y cerramos todas las ventanas
#camara.release()
cv2.destroyAllWindows()


