from MedidorRobotObjetc import MedidorRobot
from SensorObject import Sensor
import matplotlib.pyplot as plt

mi_robot = MedidorRobot(_puerto= "COM5")


# Definir las matrices A, H, P, Q, R
import numpy as np
from ProcessingFunctions import *
A = np.array([[1]])
H = np.array([[1], [1]])
P = np.array([[1]])
Q = np.array([[0.01]])
R = np.array([[0.1, 0], [0, 0.1]])

# Inicializar el objeto filtro de Kalman
kf = kalman_filter()
kf.init_filter(A, H, P, Q,R)

angle_vect = []
for angle in range(0,180,5):

    angle_vect.append(angle)
    # Cambio la posicion del servo
    mi_robot.send_command("RX_MOV_SERVO",[angle]) 

    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")



# Creación de los gráficos
plt.figure(figsize=(10, 5))

# Gráfico para sensor ultrasonido
plt.subplot(1, 3, 1)
sensor_us_values = mi_robot.get_sensor_ultrasonido().get_values()
plt.plot(angle_vect,sensor_us_values, marker='o', color='b')
plt.title('Medición Sensor Ultrasonido')
plt.xlabel('Ángulo (grados)')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Gráfico para sensor óptico
plt.subplot(1, 3, 2)
sensor_opt_values = mi_robot.get_sensor_optico().get_values()
plt.plot(angle_vect,sensor_opt_values, marker='s', color='r')  
plt.title('Medición Sensor Óptico')
plt.xlabel('Ángulo (grados)')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Gráfico kalman
plt.subplot(1, 3, 3)
valores_kalman = kf.procesar_datos(sensor_us_values,sensor_opt_values)
valores_kalman = [ valor[0] for valor in valores_kalman ]
plt.plot(angle_vect,valores_kalman, marker='s', color='r')  
plt.title('Medición Filtro Kalman')
plt.xlabel('Ángulo (grados)')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Ajustar el diseño
plt.tight_layout()

# Mostrar los gráficos
plt.show()

mi_robot.disconnect()

