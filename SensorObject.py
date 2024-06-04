from collections import deque
import numpy as np

class Sensor:
    def __init__(self, N = 100):
        self._queue = deque(maxlen=N)
        self._ErrortipoA = 0

    def queue_dim(self, dim):
        """
        Cambia el tamaño de la cola del sensor.

        :param nuevo_tamano: Nuevo tamaño de la cola.
        """
        self._queue = deque(self._queue, maxlen=dim)

    def queue_insert(self, valor):
        """
        Escribe un valor en la cola del sensor.

        :param valor: Valor a escribir en la cola.
        """
        # Hago que sea circular, si se llena borro el primer dato que se ingreso
        if self._queue.count == self._queue.maxlen:
            self._queue.popleft()

        self._queue.append(valor)

    def queue_state(self):
        return len(self._queue)
    def queue_pop(self):
        return self._queue.pop()
    def get_values(self):
    # Convertimos la deque a una lista para obtener todos sus valores
        return [(valor  - self._ErrortipoA) for valor in list(self._queue)]
    
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