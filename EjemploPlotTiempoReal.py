## En este script voy a plotear en tiempo real lo que se recibe.
# NOTA: Si se quiere hacer una rutina y plotear a la vez es necesario hacerlo en un thread
# la rutina.
# Matplotlib NO FUNCIONA en un thread, asique siempre dejarlo en main

from TorretaMedicion import TorretaMedicion
import matplotlib.pyplot as plt
import numpy as np
# Historial global para almacenar los valores previos
historial = []

def procesamiento(lista):
    """Calcula la media móvil con ventana de 3, mnteniendo valores previos."""
    global historial  # Usamos una variable global para almacenar los datos previos

    try:
        # Verificar que la entrada sea válida
        if not isinstance(lista, (list, np.ndarray)):
            raise TypeError("La entrada debe ser una lista o un array de NumPy.")

        # Convertir a array de NumPy para facilidad de cálculo
        lista = np.array(lista, dtype=float)

        # Verificar que la lista no esté vacía
        if lista.size == 0:
            raise ValueError("La lista de entrada está vacía.")

        # Agregar los nuevos valores al historial
        historial.extend(lista.tolist())

        # Mantener solo los últimos valores necesarios
        if len(historial) > 3:
            historial = historial[-3:]  # Solo se guardan los últimos 3 valores

        # Si aún no hay suficientes datos, devolver lista vacía
        if len(historial) < 3:
            return lista

        # Calcular la media móvil con los valores actuales en historial
        kernel = np.ones(3) / 3
        resultado = np.convolve(historial, kernel, mode='valid')

        return resultado.tolist()[:-len(lista)]
    
    except Exception as e:
        print(f"Error: {e}")
        return lista  # En caso de error, devolver lista vacía
    
mi_robot = TorretaMedicion(_puerto="COM5")
mi_robot.send_command("RX_MOV_SERVO",[90]) 
mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_REGULAR",[10])
mi_robot.send_command("RX_MS_SENSOR_OPTICO_REGULAR",[10])

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
