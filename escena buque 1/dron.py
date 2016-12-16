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
#erroCode,camara = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)   #'Quadricopter_frontCamera'   Vision_sensor

#########

def derecha():
    moverY(1)

def izquierda():
    moverY(0)

def arriba():
    moverX(1)

def abajo():
    moverX(0)

def zoomPositivo():
    moverZ(1)

def zoomNegativo():
    moverZ(0)
def capturarImage():
    erroCode,dron = vrep.simxGetObjectHandle(clientID,'Quadricopter_target',vrep.simx_opmode_oneshot_wait)
    erroCode,camara = vrep.simxGetObjectHandle(clientID,'Vision_sensor_front',vrep.simx_opmode_oneshot_wait)   #'Quadricopter_frontCamera'   Vision_sensor_front
    _,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_streaming)
    time.sleep(1)
    k=0
    while k==0:
        _,resolution, image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_buffer)
        img = np.array(image,dtype=np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        #cv2.imshow('Imge1', img)
        img1 = np.rot90(img,1)
        img2 = np.fliplr(img1)
        img3 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
        img4 = cv2.cvtColor(img3, cv2.COLOR_BGR2HSV)
        print "esc"
        #cv2.imshow('Imge', img)
        #tecla = cv2.waitKey(5) & 0xFF
        #if tecla == 27:
        k=1
        cv2.imwrite('0.png',img)
        cv2.imwrite('1.png',img1)
        cv2.imwrite('2.png',img2)
        cv2.imwrite('3.png',img3)
        cv2.imwrite('4.png',img4)
        print "listo"
## contDesplamiento = numero de interacci?n dentro del while
## tipo = 1 sumar ; 0 restar
def moverY(tipo):
    global posZ
    global x
    global y
    global ts
    global maxDesplamiento
    cont = 0
    #while ( (y>=-4.70 and y<=2.25) and cont<=maxDesplamiento):
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            y=y+0.1
        elif tipo == 0:
            y=y-0.1
        vrep.simxSetObjectPosition(clientID,dron,-1,(x,y,posZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def moverX(tipo):
    global posZ
    global x
    global y
    global ts
    global maxDesplamiento
    cont = 0
    #while ( x>=-3.80 and x<=3.77 and cont<=maxDesplamiento):
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            x=x-0.1
        elif tipo == 0:
            x=x+0.1

        vrep.simxSetObjectPosition(clientID,dron,-1,(x,y,posZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def moverZ(tipo):
    global posZ
    global x
    global y
    global ts
    global maxDesplamiento
    cont = 0
    #while (posZ>0.50 and posZ<1.5 and cont<=maxDesplamiento):
    while (cont<=maxDesplamiento):
        cont=cont+1
        if tipo == 1:
            posZ=posZ+0.05
        elif tipo == 0:
            posZ=posZ-0.05

        vrep.simxSetObjectPosition(clientID,dron,-1,(x,y,posZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def menu():
    op=0
    while op!=1:
        print("1.Salir")
        print("2. Mover Y")
        print("3. Mover X")
        op = int(input('Ingrese Opcion:'))
        if(op==2):
            moverY()
        if(op==3):
            moverX()

##menu()
ventana = Frame(height=250,width=400)
ventana.pack(padx=10,pady=10)
etiqueta = Label(text="SIMULADOR DRON",font=("Verdana",18)).place(x=100,y=0)

botonXARR = Button(ventana,command=arriba,text="Arriba").place(x=165,y=65)
botonYIZQ = Button(ventana,command=izquierda,text="Izquierda").place(x=120,y=100)
botonYDER = Button(ventana,command=derecha,text="Derecha").place(x=200,y=100)
botonXABA = Button(ventana,command=abajo,text="Abajo").place(x=165,y=135)
botonZPOS = Button(ventana,command=zoomPositivo,text="Zoom +").place(x=20,y=82)
botonZNEG = Button(ventana,command=zoomNegativo,text="Zoom -").place(x=20,y=112)
botonZNEG = Button(ventana,command=capturarImage,text="Capturar Imagen").place(x=20,y=152)


ventana.mainloop()