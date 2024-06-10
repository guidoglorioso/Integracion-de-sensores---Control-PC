from MedidorRobotObjetc import MedidorRobot
from SensorObject import Sensor
import matplotlib.pyplot as plt

mi_robot = MedidorRobot(_puerto= "COM5")


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
plt.subplot(1, 2, 1)
sensor_us = mi_robot.get_sensor_ultrasonido()
plt.plot(angle_vect,sensor_us.get_values(), marker='o', color='b')
plt.title('Medición Sensor Ultrasonido')
plt.xlabel('Ángulo (grados)')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Gráfico para sensor óptico
plt.subplot(1, 2, 2)
sensor_opt = mi_robot.get_sensor_optico()
plt.plot(angle_vect,sensor_opt.get_values(), marker='s', color='r')  
plt.title('Medición Sensor Óptico')
plt.xlabel('Ángulo (grados)')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Ajustar el diseño
plt.tight_layout()

# Mostrar los gráficos
plt.show()

mi_robot.disconnect()

