## En este script voy a plotear en tiempo real lo que se recibe.
# NOTA: Si se quiere hacer una rutina y plotear a la vez es necesario hacerlo en un thread
# la rutina.
# Matplotlib NO FUNCIONA en un thread, asique siempre dejarlo en main

from MedidorRobotObjetc import MedidorRobot
import matplotlib.pyplot as plt

def procesamiento(valor):
    return [this_v + 100 for this_v in valor]

mi_robot = MedidorRobot(_puerto="COM5")
mi_robot.send_command("RX_MOV_SERVO",[90]) 
mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO",[1])
mi_robot.send_command("RX_MS_SENSOR_OPTICO",[1])

# Crear la figura y los ejes para los subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))  # 1 fila, 2 columnas

# Resteo los tiempos de ambos sensores
mi_robot.ultra_sonido.start_time()
mi_robot.optico.start_time()

# Iniciar las animaciones para cada sensor
ani1 = mi_robot.ultra_sonido.add_plot_raw(fig, ax1)
ani2 = mi_robot.optico.add_plot_raw(fig, ax2)

# Agrego un grafico de datos procesados.
ani3 = mi_robot.optico.add_plot(fig, ax3,procesamiento)

ax1.set_title("Medicion Ultrasonido")
ax2.set_title("Medicion sensor optico")
ax3.set_title("Medicion Procesada")

# Ajustar el layout para que no haya solapamiento
plt.tight_layout()

# Mostrar la figura
plt.show()

mi_robot.disconnect()
