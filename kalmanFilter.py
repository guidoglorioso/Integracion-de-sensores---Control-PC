from RobotObject import Robot
from SensorObject import Sensor
from FuncionesSensores import *
import matplotlib.pyplot as plt
import numpy as np

mi_robot = Robot()
mi_robot.connect(puerto="COM5")

# Defino comandos con su identificador
comando = {
    "RX_MS_SENSOR_ULTRA_SONIDO_ONETIME" : "SENUS1",
    "RX_MS_SENSOR_OPTICO_ONETIME" : "SENOP1",
    "RX_MOV_SERVO" : "MOV1",
    "RX_RECORRIDO_SERVO" : "MOVR",
    "RX_MS_SENSOR_ULTRA_SONIDO" : "SENUS",
    "RX_MS_SENSOR_OPTICO" : "SENOP",
    "RX_MS_SENSOR_ACELEROMETRO" : "SENAC",
    "RX_MS_SENSOR_GIROSCOPO" : "SENGI",
    "RX_RECORRIDO_SERVO" : "MOVR",

}

# Asigno los comandos al objeto robot
mi_robot.set_commands(comandos=comando)

# Defino sensores y los asigno al objeto robot
ultra_sonido = Sensor()
optico = Sensor()

sensores = {
    "SENUSD" : ultra_sonido,
    "SENOPD" : optico,
}

mi_robot.set_sensors(sensores)

# Inicializo la adquisicion de datos de sensores a los objetos "Sensor"
mi_robot.start_sensor_log()

### Inicia rutina 
mi_robot.send_command("RX_MOV_SERVO",[90]) 
# Definir matrices del filtro de Kalman

kf = crear_filtro_kalman([optico,ultra_sonido],"FILTER_DISTANCE_TWO_SENSOR")

for i in range(50):

    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

    # Calculo por kalman
    
    actualizar_filtro_kalman(kf,ultra_sonido.queue_pop())

    print(f"medicion {i}")

mediciones_ultrasonido = ultra_sonido.get_values()
mediciones_optico = optico.get_values()


num_med = range(len(mediciones_ultrasonido))
# Creación de los gráficos
plt.figure(figsize=(10, 5))

# Gráfico para sensor ultrasonido
plt.subplot(1, 3, 1)
plt.plot(num_med,mediciones_ultrasonido, marker='o', color='b')
plt.title('Medición Sensor Ultrasonido')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Gráfico para sensor óptico
plt.subplot(1, 3, 2)
num_med = range(len(mediciones_optico))
plt.plot(num_med,mediciones_optico, marker='s', color='r')  
plt.title('Medición Sensor Óptico')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)
num_med = range(len(valores_kalman))
# Gráfico para sensor óptico
plt.subplot(1, 3, 3)
plt.plot(num_med,valores_kalman, marker='s', color='r')  
plt.title('Estimacion Kalman')
plt.xlabel('Medicion N°')
plt.ylabel('Distancia (mm)')
plt.grid(True)

# Ajustar el diseño
plt.tight_layout()

# Mostrar los gráficos
plt.show()

### Termina rutina

mi_robot.disconnect()

##############



