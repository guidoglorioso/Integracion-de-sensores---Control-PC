from TorretaMedicion import TorretaMedicion
from FuncionesProcesamiento import *
import matplotlib.pyplot as plt
import numpy as np
import time 
mi_robot = TorretaMedicion(_puerto = "COM5")



def media_movil_misma_longitud(arr):
    """Calcula la media móvil con ventana de 3 y devuelve la misma cantidad de valores."""
    try:
        # Verificar que la entrada sea un np.array
        if not isinstance(arr, np.ndarray):
            raise TypeError("La entrada debe ser un array de NumPy.")

        # Verificar que el array no esté vacío
        if arr.size == 0:
            raise ValueError("El array de entrada está vacío.")

        # Definir la ventana de media móvil
        kernel = np.ones(10) / 10

        # Aplicar la convolución con modo 'same' para mantener la longitud original
        resultado = np.convolve(arr, kernel, mode='same')

        return resultado
    
    except Exception as e:
            print(f"Error: {e}")
            return np.array([])  # Devolver array vacío en caso de error




# Inicializo kalman
mi_robot.set_kalman_filter()

mi_robot.send_command("RX_MOV_SERVO",[0])
mi_robot.set_csv_output(extra_text="CSV_Prueba_") ## Activo la salida CSV de los sensores
# Resteo los tiempos de ambos sensores
mi_robot.ultra_sonido.start_time()
mi_robot.optico.start_time()
mi_robot.kf.start_time()

for angle in range(0,190,5):

    
    # Pido medicion de sensor ultrasonido    
    mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_SENSOR_OPTICO_ONETIME")

    # Pido medicion de sensor optico 
    mi_robot.send_command("RX_MS_ANGULO")

    # Cambio la posicion del servo
    
    mi_robot.send_command("RX_MOV_SERVO",[angle])
    


## PLOTEO LAS MEDICIONES OBTENIDAS EN FUNCION DEL ANGULO
mi_robot.kf.update_kalman_filter()
distancias_mediciones_kf = np.array(mi_robot.kf.kalman_sensor.get_values())
distancias_mediciones = np.array(mi_robot.ultra_sonido.get_values())
angulos_mediciones = np.array(mi_robot.get_sensor_angulos().get_values())

mi_robot.plot_distance_angle()
#plt.scatter(np.deg2rad(angulos_mediciones-90),distancias_mediciones_kf,label="Sensor Kalman Filter")
plt.scatter(np.deg2rad(angulos_mediciones-90),distancias_mediciones,label="Sensor Ultrasonido")
plt.scatter(np.deg2rad(angulos_mediciones-90),media_movil_misma_longitud(distancias_mediciones),label="Media movil - Sensor us")
distancias_mediciones = np.array(mi_robot.optico.get_values())
plt.scatter(np.deg2rad(angulos_mediciones-90),distancias_mediciones,color ="red",label="Sensor Optico")
plt.legend()
# Mostrar el gráfico
plt.show()


mi_robot.disconnect()



