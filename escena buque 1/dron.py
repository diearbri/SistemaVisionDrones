from Tkinter import *
import vrep
import sys
import math
import time

posZ = 0.5
x=0
y=0
ts=0.025
vrep.simxFinish(-1)

clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID != -1:
    print('Conexion Exitosa')
else:
    print('Conexion Fallida')
    sys.exit('No se pudo Conectar')

erroCode,dron = vrep.simxGetObjectHandle(clientID,'Quadricopter_target',vrep.simx_opmode_oneshot_wait)
##erroCode,camara = vrep.simxGetObjectHandle(clientID,'Vision_sensor',vrep.simx_opmode_oneshot_wait)
##_,resolution,image = vrep.simxGetVisionSensorImage(clientID,camara,0,vrep.simx_opmode_streaming)
##time.sleep(1)
#########
def moverY():
    x=0
    y=0
    posZ=0.5
    while (x>-1.5):
        y=-1.33*x
        x=x-0.0075
        vrep.simxSetObjectPosition(clientID,dron,-1,(0,y,posZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def moverX():
    x=0
    y=0
    posZ=0.5
    while (x>-1.5):
        y=-1.33*x
        x=x-0.0075
        vrep.simxSetObjectPosition(clientID,dron,-1,(x,0,posZ),vrep.simx_opmode_oneshot)
        time.sleep(ts)

def moverZ():
    x=0
    z=0.5
    while (z<2):
        z=z+0.005
        vrep.simxSetObjectPosition(clientID,dron,-1,(x,0,z),vrep.simx_opmode_oneshot)
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

botonX = Button(ventana,command=moverY,text="<==").place(x=120,y=100)
botonY = Button(ventana,command=moverX,text="==>").place(x=200,y=100)
botonZ = Button(ventana,command=moverZ,text="Eje Z").place(x=160,y=65)
ventana.mainloop()