from MedidorRobotObjetc import MedidorRobot
from ProcessingFunctions import *
import numpy as np

mi_robot = MedidorRobot(_puerto = "COM5")

### Inicia rutina 
mi_robot.send_command("RX_MOV_SERVO",[90]) 
# Definir matrices del filtro de Kalman

# Definir las matrices A, H, P, Q, R
A = np.array([[1]])
H = np.array([[1], [1]])
P = np.array([[1]])
Q = np.array([[0.01]])
R = np.array([[0.1, 0], [0, 0.1]])

# Inicializar el objeto filtro de Kalman
kf = kalman_filter()
kf.attach_sensors(mi_robot.ultra_sonido,mi_robot.optico)
kf.init_filter(A, H, P, Q,R,adapt=False)


for i in range(70):

    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

sensor_us_values = mi_robot.ultra_sonido.get_values()[-40:]

sensor_opt_values = mi_robot.optico.get_values()[-40:]
valores_kalman = kf.procesar_datos(sensor_us_values,sensor_opt_values)
valores_kalman = [ valor[0] for valor in valores_kalman ]

print(f"La media del ultrasonido es: {np.mean(sensor_us_values)}, la varianza es de: {np.var(sensor_us_values)}")
print(f"La media del optico es: {np.mean(sensor_opt_values)}, la varianza es de: {np.var(sensor_opt_values)}")
print(f"La media del kalman es: {np.mean(valores_kalman)}, la varianza es de: {np.var(valores_kalman)}")



mi_robot.disconnect()



