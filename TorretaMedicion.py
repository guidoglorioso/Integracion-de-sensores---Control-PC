# Objeto especifico de proyecto. 
# Robot con servomotor para ubicar posicion de medicion, Sensores optico y de ultrasonido para medir distancia 
# y sensor de acelerometro y giroscopo para posicion.

# Dependecias
from GestorBasicos import GestorBasicos
from Sensor import sensor
import numpy as np
from FuncionesProcesamiento import *
import matplotlib.pyplot as plt

class TorretaMedicion(GestorBasicos):
    """
    Objeto dedicado a la interaccion con el proyecto de robot medidor de distancias.
    Hereda de la clase GestorBasicos los metodos para usar
    """    
    def __init__(self,_puerto) -> None:
        """Inicialización de objeto para interacción con proyecto.
        
        Args:
            _puerto (str): Nombre del puerto al que se va a conectar el robot (por ejemplo, "COM1").
        """     

        # Inicializo el objeto robot para interactuar con el proyecto
        super().__init__()

        self._command_init()

        # Defino sensores y los asigno al objeto robot
        self.ultra_sonido = sensor(N = 100,name="Sensor_UltraSonido")
        self.optico = sensor(N = 100,name="Sensor_Optico")
        self.angle = sensor(N = 100,name="Angulo_Servomotor")
        self._sensor_init()
        
        # Conecto por serie
        self.Set_interval(interval=30) # 30ms de update
        self.connect(puerto=_puerto)

        # Inicializo la adquisicion de datos de sensores a los objetos "Sensor"
        self.start_sensor_log()

        ## Variables propias del proyecto
        self.ultra_sonido.set_var(3.392639090737473)
        self.optico.set_var(9.341605062534653)
        self.ultra_sonido.set_calibration(-62.0)
        self.optico.set_calibration(-63.93)
        # Aca se ponen parametros especificos del proyecto, por ejemplo valores de calibracion
        # U otras caracteristicas propias.
    
    def disconnect(self):
        """
        Desconecta el robot y fuerza la escritura de los datos de los sensores en archivos CSV antes de cerrar la conexión.
        """
        self.ultra_sonido.force_callback_buff_full()
        self.optico.force_callback_buff_full()
        self.angle.force_callback_buff_full()
        super().disconnect()

    def _command_init(self):
        """
        Inicializa los comandos para interactuar con el robot.
        """        
        # Defino comandos con su identificador
        comando = {
            "RX_MS_SENSOR_ULTRA_SONIDO_ONETIME" : "SENUS1",
            "RX_MS_SENSOR_OPTICO_ONETIME" : "SENOP1",
            "RX_MOV_SERVO" : "MOV1",
            "RX_MS_SENSOR_ULTRA_SONIDO_REGULAR" : "SENUS",
            "RX_MS_SENSOR_OPTICO_REGULAR" : "SENOP",
            "RX_MS_SENSOR_ACELEROMETRO" : "SENAC",
            "RX_MS_SENSOR_GIROSCOPO" : "SENGI",
            "RX_MS_ANGULO": "ANG",
        }

        # Asigno los comandos al objeto robot
        self.set_commands(comandos=comando)
    
    def _sensor_init(self):
        """
        Inicializa los comandos de los sensores que se reciben.
        """        
        sensores = {
            "SENUSD" : self.ultra_sonido,
            "SENOPD" : self.optico,
            "SENANG" : self.angle,
        }
        
        self.set_sensors(sensores)

    def get_sensor_ultrasonido(self):
        """Obtiene el objeto del sensor de ultrasonido.

        Returns:
            Sensor: Objeto del sensor de ultrasonido.
        """
        return self.ultra_sonido
    
    def get_sensor_optico(self):
        """Obtiene el objeto del sensor óptico.

        Returns:
            Sensor: Objeto del sensor óptico.
        """

        return self.optico
    
    def get_sensor_angulos(self):
        """Obtiene el objeto de los angulos.

        Returns:
            Sensor: Objeto de los angulos.
        """

        return self.angle
    
    def set_kalman_filter(self):
        # Definir las matrices A, H, P, Q, R
        A = np.array([[1]])
        H = np.array([[1], [1]])
        P = np.array([[1]])
        Q = np.array([[0.01]])
        R = np.array([[0.1, 0], [0, 0.1]])

        # Inicializar el objeto filtro de Kalman
        self.kf = kalman_filter()
        self.kf.attach_sensors(self.ultra_sonido,self.optico)
        self.kf.init_filter(A, H, P, Q,R)

    def plot_distance_angle(self):
        
        # Configuración del semicírculo (area donde no se puede medir)
        radio = 60
        centro_x = 0
        centro_y = 0
        max_dist = 500
        angulos = np.linspace(-np.pi / 2, np.pi / 2, 180)  # De -90 grados a 90 grados

        # Coordenadas del semicírculo
        x = centro_x + radio * np.cos(angulos)
        y = centro_y + radio * np.sin(angulos)

        # Tamaño de la figura (ancho, alto) 
        figsize = (10, 8)

        # Creación de la figura y el eje con el tamaño especificado
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=figsize)

        # Gráfico del semicírculo
        ax.plot(angulos, [radio]*len(angulos), color='blue')

        # Configuración del rango de los ejes
        ax.set_ylim(0, max_dist)

        # Agregar una grilla circular
        ax.grid(True)
        grid = np.linspace(100, max_dist, 10, dtype=int)  # Ajuste de la grilla

        ax.set_rticks(grid)  # Radio de las líneas de la grilla

        # Personalizar las etiquetas de los ejes
        ax.set_yticklabels(grid)
        ax.set_xticks(np.linspace(-np.pi / 2, np.pi / 2, 5))
        ax.set_xticklabels(['-90°', '-45°', '0°', '45°', '90°'])

        # Limitar la visualización a los cuadrantes deseados

        ax.set_theta_direction(1)
        ax.set_thetamax(90)

        # Título del gráfico
        plt.title('Mapeo de mediciones')

        return fig,ax