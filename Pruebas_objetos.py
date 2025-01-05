from MedidorRobotObjetc import MedidorRobot
from ProcessingFunctions import *
import matplotlib.pyplot as plt
import threading

thread_on = 1

def control_servo():
    while thread_on:

        for angle in range(0,180,5):
            angle_vect.append(angle)
            # Cambio la posicion del servo
            mi_robot.send_command("RX_MOV_SERVO",[angle])

        for angle in range(0,180,2)[::-1]:
            angle_vect.append(angle)
            # Cambio la posicion del servo
            mi_robot.send_command("RX_MOV_SERVO",[angle]) 


mi_robot = MedidorRobot(_puerto= "COM5")


angle_vect = []
mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO",[1])
mi_robot.send_command("RX_MS_SENSOR_OPTICO",[1])

# Crear el thread
thread = threading.Thread(target=control_servo)

# Iniciar el thread
thread.start()

# Definir las matrices A, H, P, Q, R
A = np.array([[1]])
H = np.array([[1], [1]])
P = np.array([[1]])
Q = np.array([[0.01]])
R = np.array([[0.1, 0], [0, 0.1]])


# Inicializar el objeto filtro de Kalman
kf = kalman_filter()
kf.attach_sensors(mi_robot.ultra_sonido,mi_robot.optico)
kf.init_filter(A, H, P, Q)

# Crear la figura y los ejes para los subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))  # 1 fila, 2 columnas

# Resteo los tiempos de ambos sensores
mi_robot.ultra_sonido.start_time()
mi_robot.optico.start_time()
kf.start_time()

# Iniciar las animaciones para cada sensor
ani1 = mi_robot.ultra_sonido.add_plot_raw(fig, ax1)
ani2 = mi_robot.optico.add_plot_raw(fig, ax2)

# Agrego un grafico de datos procesados.
ani3 = kf.add_plot_kalman(fig, ax3)

ax1.set_title("Medicion Ultrasonido")
ax2.set_title("Medicion sensor optico")
ax3.set_title("Medicion Procesada")

# Ajustar el layout para que no haya solapamiento
plt.tight_layout()

# Mostrar la figura
plt.show()

thread_on = 0

mi_robot.disconnect()

