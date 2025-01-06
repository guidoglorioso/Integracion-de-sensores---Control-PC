from collections import deque
import numpy as np
import matplotlib.animation as animation
import time
from typing import Callable, Optional
import csv

class Sensor:
    def __init__(self, N = 100,name : str = "sensor"):
        """
        Inicializa un objeto Sensor.

        Args:
            N (int, optional): Tamaño máximo de la cola de datos. Defaults to 100.
            name (str, optional): Nombre del sensor. Defaults to "sensor".
        """

        # Queue para almacenar datos. El largo es de N valores. Una vez llenado se pisan (buff circular)
        self._largo_queue = N
        self._queue = deque(maxlen=N)
        
        # Variables caracteristicos de cada sensor
        self._ErrortipoA = 0 # Error tipo A
        self._var = 0        # Varianza

        # Tiempo cero para la adquisicion de datos. Las muestras se referencian a este tiempo
        self._init_time = time.time()
        self._last_update = None

        # Callback de buffer lleno. Cuando se reciben N datos nuevos esta funcion es invocada.
        self._callback_buff_full = None
        self._contador_buff = 0

        # Nombre del sensor. Se usa para escribir en CSV.
        self._name_sensor = name

   

    def queue_dim(self, dim):
        """
        Cambia el tamaño de la cola del sensor.

        Args:
            dim (int): Nuevo tamaño de la cola.
        """
        self._queue = deque(self._queue, maxlen=dim)

    def queue_insert(self, valor):
        """
        Escribe un valor en la cola del sensor. Se agrega tambien el momento en el que se agrega el valor

        Args:
            valor: Valor a escribir en la cola.
        """
        
        # Chequeo si la queue recibio "_largo_queue" datos nuevos
        if  self._contador_buff >= self._largo_queue:
            self._contador_buff = 0
            if self._callback_buff_full !=None:
                self._callback_buff_full() # Invoco a la callback en caso de haber sido definida
        self._contador_buff +=1

        # Hago que sea circular, si se llena borro el primer dato que se ingreso
        if self._queue.count == self._queue.maxlen:
            self._queue.popleft()

        self._last_update = time.time()

        self._queue.append([valor - self._ErrortipoA,self._last_update])

    def set_callback_buff_full(self, callback: Optional[Callable] = None):
        """Funcion que setea la callback de buffer lleno y activa o desactiva su invocacion. \n
        Por defecto esta funcion desactiva el llamado de la callback. Pasando el argumento "callback" como una\n
        funcion activa su invocacion. 

        Args:
            callback (function): funcion a invocar. En caso de "None" no se invoca la callback.
        """        
        self._callback_buff_full = callback

    def force_callback_buff_full(self):
        """Fuerza a que se guarden los datos que quedaron en el buffer
        """        

        #Guardo los datos que hayan quedado en la queue en caso de que el CSV este activado
        if self._callback_buff_full != None:
            self._callback_buff_full() 

    def queue_state(self):
        """
        Devuelve la cantidad de datos en la cola.

        Returns:
            int: Cantidad de datos en la cola.
        """       
        return len(self._queue)
    
    def queue_pop(self):
        """
        Saca un valor de la cola (valor ingresado más reciente).

        Returns:
            list: Valor recibido y tiempo de recepción.
        """     
        return self._queue.pop()
    
    def get_values(self,last_time = None):
        """
        Devuelve todos los valores de la cola sin borrarlos.

        Args:
            last_time (float, optional): Permite obtener los valores adquiridos después de este momento. Defaults to None.

        Returns:
            list: Vector de valores medidos.
        """
        # Convertimos la deque a una lista para obtener todos sus valores
        if last_time != None:
                return [valor[0]  for valor in list(self._queue) if valor[1] > last_time]
   
        return [valor[0]  for valor in list(self._queue)]
    
    def get_values_time(self,last_time = None):
        """
        Devuelve los valores de la cola con sus tiempos.

        Args:
            last_time (float, optional): Permite obtener los valores adquiridos después de este momento. Defaults to None.

        Returns:
            list: Vector de valores medidos con sus tiempos.
        """

        if last_time != None:
            return [[valor[0],valor[1]] for valor in list(self._queue) if valor[1] > last_time]
   
        # Convierto la deque a una lista para obtener todos sus valores y sus tiempos
        return [[valor[0],valor[1]] for valor in list(self._queue)]
    
    def queue_clear(self):
        """Limpia la cola."""
        self._queue.clear()

    def media_movil(self, ventana):
        """
        Calcula la media móvil de un vector de datos.

        Args:
            ventana (int): Tamaño de la ventana de la media móvil.

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

    def set_calibration(self, calib):
        """
        Establece el error tipo A.

        Args:
            calib: Error tipo A.
        """
        self._ErrortipoA = calib
        return 
    
    def get_mean(self):
        """
        Calcula la media de los valores medidos.

        Returns:
            float: Media de los valores medidos.
        """
        return np.mean(self.get_values())
    
    def calculate_var(self):
        """
        Calcula la varianza de los valores medidos.

        Returns:
            float: Varianza de los valores medidos.
        """      

        return np.std(self.get_values())
    
    def get_var(self):
        """
        Devuelve la varianza del sensor.

        Returns:
            float: Varianza del sensor
        """        
        return self._var
    
    def set_var(self,var):
        """
        Setea la varianza del sensor.

        Args:
            var (float): Varianza del sensor
        """        
        self._var = var

    def get_last_update_time(self):
        """Devuelve el tiempo de la ultima actualizacion. En caso de nunca haber cargado nada se devuelte none

        Returns:
            time: tiempo de ultima actualizacion
        """
        return self._last_update
    
    def get_init_time(self):
        """Devuelve el tiempo de la inicializacion. 

        Returns:
            time: tiempo de la inicializacion
        """
        return self._init_time
    ## Metodos para plotear en tiempo real los datos del sensor

    def start_time(self):
        """Inicializa el tiempo de referencia de inicio para la adquisición de datos."""
        self._init_time = time.time()
        
        
    def add_plot(self, fig, ax, func_procesamiento):
        """
        Agrega un gráfico actualizable a un eje con datos procesados por una función.\n
        Importante: Se debe conservar el valor devuelto por esta funcion. De no ser asi no funciona correctamente
        
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
            time_to_plot = 30
            nonlocal x_data, y_data
            
            # Datos sin procesar
            data_raw = []
            # Tiempo de la ultima medicion
            last_t = x_data[-1] + self._init_time 
            
            # Tomo los valores medidos a partir de un cierto tiempo
            for y, x in self.get_values_time(last_time=last_t):  
                x_data.append(x - self._init_time)
                data_raw.append(y)
            
            # Procesar los datos utilizando la función de procesamiento
            nuevos_datos_procesados = func_procesamiento(data_raw)
            
            # Actualizar los datos agregando los nuevos datos obtenidos 
            y_data.extend(nuevos_datos_procesados)

            # Ajusto el grafico y devuelvo el plot
            # Obtengo el indice del ultimo valor que entra en el grafico
            indice = 0
            for _indice, _valor in enumerate(x_data):
                if _valor > x_data[-1] - time_to_plot:
                    indice = _indice
                    break
                
            if x_data and y_data:
                line.set_data(x_data, y_data)
                ax.set_xlim(max(0, x_data[-1] - time_to_plot), max(time_to_plot, x_data[-1]))  # Mostrar los últimos 10 segundos
                ax.set_ylim(min(y_data[indice:]) - 10, max(y_data[indice:]) + 10)  # Ajustar el límite Y dinámicamente
                #ax.set_ylim(40,80)
            return line,

        # Configurar animación
        ani = animation.FuncAnimation(fig, update_plot, interval=50, blit=False)
        
        return ani
    
    def add_plot_raw(self,fig, ax):
        """
        Agrega en forma dinamica un grafico con la informacion "cruda" del sensor

        Args:
            fig (matplotlib.figure.Figure): Figura de matplotlib donde se agregará el gráfico.
            ax (matplotlib.axes.Axes): Ejes de matplotlib donde se agregará el gráfico.
        """        
        def buff(value):
            return value
        return self.add_plot(fig, ax,buff)
        
    def write_to_csv(self,filename: str):
        """Escribe los datos del sensor en un archivo CSV.

        Args:
            filename (str): Nombre del archivo CSV.
            sensor (SensorObject.Sensor): Objeto del sensor.
        """
        
        # Verificar si el archivo existe y si está vacío para escribir el encabezado
        try:
            with open(filename, 'r') as csvfile:
                has_header = csvfile.readline() != ''
        except FileNotFoundError:
            has_header = False

        with open(filename, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)

            # Escribir el encabezado si el archivo no tiene
            if not has_header:
                csvwriter.writerow(['InitTime'])
                csvwriter.writerow([self._init_time])
                csvwriter.writerow(['Timestamp', 'Sensor Data'])

            # Escribir los datos del sensor en el archivo CSV
            data = self.get_values_time()

            for this_data in data:
                # Escribo el momento en el que se recibio (respecto al momento en el que se inicio el objeto), 
                timestamp, sensor_data = this_data[1] - self._init_time, this_data[0]
                csvwriter.writerow([timestamp, sensor_data])