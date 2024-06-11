from MedidorRobotObjetc import MedidorRobot
import matplotlib.pyplot as plt
from ProcessingFunctions import  *

mi_robot = MedidorRobot(_puerto="COM5")

# Cambio la posicion del servo
mi_robot.send_command("RX_MOV_SERVO",[90]) 

num_mediciones = 30

n_med = []
for i in range(num_mediciones):
    n_med.append(i)

    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

    print(f"medicion {i}")


# # Creación de los gráficos
# plt.figure(figsize=(10, 5))

# # Gráfico para sensor ultrasonido
# plt.subplot(1, 2, 1)
# sensor_us = mi_robot.get_sensor_ultrasonido()
# print(f"valores: {sensor_us.get_values()}")
# plt.plot(n_med,sensor_us.get_values(), marker='o', color='b')
# plt.title('Medición Sensor Ultrasonido')
# plt.xlabel('Medicion N°')
# plt.ylabel('Distancia (mm)')
# plt.grid(True)

# # Gráfico para sensor óptico
# plt.subplot(1, 2, 2)
# sensor_opt = mi_robot.get_sensor_optico()
# plt.plot(n_med,sensor_opt.get_values(), marker='s', color='r')  
# plt.title('Medición Sensor Óptico')
# plt.xlabel('Medicion N°')
# plt.ylabel('Distancia (mm)')
# plt.grid(True)

# # Ajustar el diseño
# plt.tight_layout()

# # Mostrar los gráficos
# plt.show()

## ahora con los sensores calibrados

calibracion_sensores([mi_robot.ultra_sonido,mi_robot.optico])
time.sleep(2)

mi_robot.ultra_sonido.queue_clear()
mi_robot.optico.queue_clear()

for i in range(num_mediciones):

    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

    print(f"medicion {i}")


# Creación de los gráficos
plt.figure(figsize=(10, 5))

# Gráfico para sensor ultrasonido
plt.subplot(1, 2, 1)
sensor_us = mi_robot.get_sensor_ultrasonido()
plt.plot(n_med,sensor_us.get_values(), marker='o', color='b')
plt.title('Medición Sensor Ultrasonido')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Gráfico para sensor óptico
plt.subplot(1, 2, 2)
sensor_opt = mi_robot.get_sensor_optico()

plt.plot(n_med,sensor_opt.get_values(), marker='s', color='r')  
plt.title('Medición Sensor Óptico')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Ajustar el diseño
plt.tight_layout()

# Mostrar los gráficos
plt.show()

mi_robot.disconnect()

