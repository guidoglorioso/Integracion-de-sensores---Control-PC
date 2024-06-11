from SensorObject import Sensor
import time
import numpy as np
import matplotlib.animation as animation
from filterpy.kalman import KalmanFilter

def calibracion_sensores(Sensores : list[Sensor]):
    """Rutina para calibrar sensores. Se debe colocar el dispositivo quieto con los sensores \n
    estables. La rutina de calibracion tomará un numero de mediciones de ambos sensores y fijara
    su parametro "calibracion".

    Args:
        Sensores (list[Sensor]): lista de sensores que miden una misma variable
    """ 
    medias = []  
    for this_sensor in Sensores:
        medias.append(this_sensor.GetMean())

    media_total = np.mean(medias)
    for this_sensor,media in zip(Sensores,medias):
        this_sensor.setCalibracion(media - media_total)
        print(media - media_total)


class kalman_filter:
    def __init__(self):

        self.kf = None

        self.sensor1 = None
        self.sensor2 = None

        self.last_update = 0
        self._time_start_plot = time.time()

    def init_filter(self, A, H, P, Q, R = None):
        """Inicializa un filtro de Kalman con las matrices especificadas.
        Args:
        - A: Matriz de transición de estado (nxn).
        - H: Matriz de medición (mxn).
        - P: Matriz de covarianza del estado inicial (nxn).
        - Q: Matriz de covarianza del proceso (nxn).
        - R: Matriz de covarianza del ruido de medición (mxm).
        """    
        if R is None:
            R = np.array([[self.sensor1.Get_var(), 0], [0, self.sensor2.Get_var()]])
        self.kf = KalmanFilter(dim_x=A.shape[0], dim_z=H.shape[0])

        self.kf.F = A  # Matriz de transición de estado
        self.kf.H = H  # Matriz de medición
        self.kf.P = P  # Matriz de covarianza del estado inicial
        self.kf.Q = Q  # Matriz de covarianza del proceso
        self.kf.R = R  # Matriz de covarianza del ruido de medición

    def attach_sensors(self,s_ultrasonido : Sensor, s_optico : Sensor):
        self.sensor1 = s_ultrasonido
        self.sensor2 = s_optico

    def actualizar_filtro_kalman(self):
        """
        Estima la distancia utilizando el filtro de Kalman actualizado con la medición z.

        Args:
        - kf: Objeto de filtro de Kalman inicializado.
        - z: Valor de medición (vector de longitud mx1).

        Returns:
        - x: Estado estimado (vector de longitud nx1).
        """
        if not self.sensor1 or not self.sensor2 :
            return None
        
        values = []

        values_sensor1 = self.sensor1.get_values(last_time=self.last_update)
        values_sensor2 = self.sensor2.get_values(last_time=self.last_update)
        self.last_update = time.time()


        max_len = max(len(values_sensor1),len(values_sensor2))
        values_sensor1 = values_sensor1[:max_len]
        values_sensor2 = values_sensor2[:max_len]
        for value_s1, value_s2 in zip(values_sensor1,values_sensor2):
            z = np.array([[value_s1],[value_s2]])
            self.kf.predict()      # Predicción del siguiente estado
            self.kf.update(z)      # Actualización con la nueva medición
            values.append([self.kf.x[0][0],time.time()])
            

        return values
    
    def add_plot_kalman(self, fig, ax):
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
            
            data = self.actualizar_filtro_kalman()
            if data is None:
                return line
            
            for y, x in data:  # Suponiendo que get_values_time devuelve (y, x)
                x_data.append(x - self._time_start_plot)
                y_data.append(y)
            
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
    
    def start_time(self):
        self._time_start_plot = time.time()