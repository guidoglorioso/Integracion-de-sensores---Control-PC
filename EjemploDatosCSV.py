from MedidorRobotObjetc import MedidorRobot
import matplotlib.pyplot as plt
import time

mi_robot = MedidorRobot(_puerto="COM5")

mi_robot.set_csv_output(extra_text="P1_") ## Activo la salida CSV de los sensores

# Cambio la posicion del servo
mi_robot.send_command("RX_MOV_SERVO",[90])

num_med = []


for i in range(20):

    num_med.append(i)

    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

   
    print(f"medicion {i}")

sensor_us = mi_robot.get_sensor_ultrasonido()
sensor_opt = mi_robot.get_sensor_optico()

# Creación de los gráficos
plt.figure(figsize=(10, 5))

# Gráfico para sensor ultrasonido
plt.subplot(1, 2, 1)


plt.plot(num_med,sensor_us.get_values(), marker='o', color='b')
plt.title('Medición Sensor Ultrasonido')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Gráfico para sensor óptico

plt.subplot(1, 2, 2)

plt.plot(num_med,sensor_opt.get_values(), marker='s', color='r')  
plt.title('Medición Sensor Óptico')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Ajustar el diseño
plt.tight_layout()

# Mostrar los gráficos
plt.show()

mi_robot.disconnect()

