
import vrep
import sys
import math
import time

posZ = 2
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
while (x>-1.27):
    y=-1.33*x
    x=x-0.0075
    vrep.simxSetObjectPosition(clientID,dron,-1,(x,y,posZ),vrep.simx_opmode_oneshot)
    time.sleep(ts)