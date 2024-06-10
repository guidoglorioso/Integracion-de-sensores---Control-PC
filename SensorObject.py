from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import time


class Sensor:
    def __init__(self, N = 100):
        self._queue = deque(maxlen=N)
        
        self._ErrortipoA = 0
        self._time_start_plot = time.time()

    def queue_dim(self, dim):
        """
        Cambia el tamaño de la cola del sensor.

        :param nuevo_tamano: Nuevo tamaño de la cola.
        """
        self._queue = deque(self._queue, maxlen=dim)

    def queue_insert(self, valor):
        """
        Escribe un valor en la cola del sensor. Se agrega tambien el momento en el que se agrega el valor

        :param valor: Valor a escribir en la cola.
        """
        # Hago que sea circular, si se llena borro el primer dato que se ingreso
        if self._queue.count == self._queue.maxlen:
            self._queue.popleft()

        self._queue.append([valor,time.time()])

    def queue_state(self):
        return len(self._queue)
    
    def queue_pop(self):
        return self._queue.pop()
    
    def get_values(self):
    # Convertimos la deque a una lista para obtener todos sus valores
        return [(valor[0]  - self._ErrortipoA) for valor in list(self._queue)]
    
    def get_values_time(self):
    # Convertimos la deque a una lista para obtener todos sus valores y sus tiempos
        return [[(valor[0]  - self._ErrortipoA),valor[1]] for valor in list(self._queue)]
    
    def queue_clear(self):
        self._queue.clear()

    def media_movil(self, ventana):
        """
        Calcula la media móvil de un vector de datos.
        
        Args:
            vector (list): El vector de datos.
            ventana (int): El tamaño de la ventana de la media móvil.
        
        Returns:
            list: La media móvil calculada.
        """
        media_movil_resultado = []
        vector = self.get_values()
        n = len(vector)
        
        for i in range(n):
            # Calcular el límite inferior y superior de la ventana
            inicio = max(0, i - ventana + 1)
            fin = min(n, i + 1)
            
            # Calcular la media de los elementos dentro de la ventana
            suma_ventana = sum(vector[inicio:fin])
            media_ventana = suma_ventana / (fin - inicio)
            
            # Agregar la media de la ventana al resultado
            media_movil_resultado.append(media_ventana)
        
        return media_movil_resultado

    def setCalibracion(self, calib):
        self._ErrortipoA = calib
        return 
    
    def GetMean(self):
        return np.mean(self.get_values())
    
    ## Metodos para plotear en tiempo real los datos del sensor

    def start_time(self):
        self._time_start_plot = time.time()
        
        
    def add_plot(self, fig, ax, func_procesamiento):
        """Función para agregar un gráfico actualizable a un eje con datos procesados por una función.

        Args:
            fig (matplotlib.figure.Figure): Figura de matplotlib donde se agregará el gráfico.
            ax (matplotlib.axes.Axes): Ejes de matplotlib donde se agregará el gráfico.
            func_procesamiento (function): Función de procesamiento que toma datos crudos y devuelve procesados.

        Returns:
            matplotlib.animation.FuncAnimation: Objeto de animación de matplotlib para el gráfico actualizable.
        """
        # Datos iniciales vacíos
        x_data = [0]
        y_data = [0]

        # Configurar el gráfico inicial
        line, = ax.plot([], [], lw=2)
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Valor')

        # Función de actualización para animación
        def update_plot(_):
            nonlocal x_data, y_data
            
            # Datos sin procesar
            data_raw = []
            last_t = x_data[-1] + self._time_start_plot 
            
            # Ejemplo de cómo obtener datos desde MedidorRobot (ajustar según tu implementación)
            for y, x in self.get_values_time():  # Suponiendo que get_values_time devuelve (y, x)
                if last_t < x:
                    x_data.append(x - self._time_start_plot)
                    data_raw.append(y)
            
            # Procesar los datos utilizando la función de procesamiento
            nuevos_datos_procesados = func_procesamiento(data_raw)
            
            # Actualizar los datos
            y_data.extend(nuevos_datos_procesados)

            # Ajustar el gráfico
            # Ajusto el grafico y devuelvo el plot
            indice = 0
            for _indice, _valor in enumerate(x_data):
                if _valor > x_data[-1] - 10:
                    indice = _indice
                    break

                
            if x_data and y_data:
                line.set_data(x_data, y_data)
                ax.set_xlim(max(0, x_data[-1] - 10), max(10, x_data[-1]))  # Mostrar los últimos 10 segundos
                ax.set_ylim(min(y_data[indice:]) - 10, max(y_data[indice:]) + 10)  # Ajustar el límite Y dinámicamente
            
        
            return line,

        # Configurar animación
        ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=True)
        
        return ani
    
    def add_plot_raw(self,fig, ax):
        def buff(value):
            return value
        return self.add_plot(fig, ax,buff)
        