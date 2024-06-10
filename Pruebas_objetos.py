## En este script voy a plotear en tiempo real lo que se recibe.

from MedidorRobotObjetc import MedidorRobot
from SensorObject import Sensor
import matplotlib.pyplot as plt


mi_robot = MedidorRobot(_puerto="COM5")

mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO",[1])
mi_robot.send_command("RX_MS_SENSOR_OPTICO",[1])

# Crear la figura y los ejes para los subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))  # 1 fila, 2 columnas

# Iniciar las animaciones para cada sensor
ani1 = mi_robot.ultra_sonido.start_plot(fig, ax1)
ani2 = mi_robot.optico.start_plot(fig, ax2)
ax1.set_title("Medicion Ultrasonido")
ax2.set_title("Medicion sensor optico")
# Ajustar el layout para que no haya solapamiento
plt.tight_layout()

# Mostrar la figura
plt.show()

#TODO hay que ver el tema de si grafico en funcion del tiempo debo guardar el tiempo de cada muestra
#TODO actualizar como lo hago ahora no es recomendable porque es lento, tengo que agarrar todos los datos
#de la queue y plotearlos cada vez que entro
#TODO podria crear otra queue para que de esta forma una se dedique al ploteo y otra al procesamiento.


mi_robot.disconnect()
