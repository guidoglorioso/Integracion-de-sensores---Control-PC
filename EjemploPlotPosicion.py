from MedidorRobotObjetc import MedidorRobot
from ProcessingFunctions import *
import matplotlib.pyplot as plt
import numpy as np

mi_robot = MedidorRobot(_puerto = "COM5")

# Inicializo kalman
mi_robot.set_kalman_filter()

mi_robot.send_command("RX_MOV_SERVO",[45])

# Resteo los tiempos de ambos sensores
mi_robot.ultra_sonido.start_time()
mi_robot.optico.start_time()
mi_robot.kf.start_time()

for angle in range(45,145,5):

    
    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_ANGULO")

    # Cambio la posicion del servo
    mi_robot.send_command("RX_MOV_SERVO",[angle])


## PLOTEO LAS MEDICIONES OBTENIDAS EN FUNCION DEL ANGULO
distancias = mi_robot.kf.actualizar_filtro_kalman()
distancias_mediciones = np.array([this_dist[0] for this_dist in distancias ])
angulos_mediciones = np.array(mi_robot.get_sensor_angulos().get_values())

mi_robot.plot_distance_angle()

plt.scatter(np.deg2rad(angulos_mediciones-90),distancias_mediciones)

# Mostrar el gráfico
plt.show()


mi_robot.disconnect()



