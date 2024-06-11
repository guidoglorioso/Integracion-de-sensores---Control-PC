# Objeto especifico de proyecto. 
# Robot con servomotor para ubicar posicion de medicion, Sensores optico y de ultrasonido para medir distancia 
# y sensor de acelerometro y giroscopo para posicion.

# Dependecias
from RobotObject import Robot
from SensorObject import Sensor

class MedidorRobot(Robot):
    """
    Objeto dedicado a la interaccion con el proyecto de robot medidor de distancias.
    Hereda de la clase robot los metodos para usar
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
        self.ultra_sonido = Sensor(N = 100,name="Sensor_UltraSonido")
        self.optico = Sensor(N = 100,name="Sensor_Optico")

        self._sensor_init()
        
        # Conecto por serie
        self.connect(puerto=_puerto)

        # Inicializo la adquisicion de datos de sensores a los objetos "Sensor"
        self.start_sensor_log()

        ## Variables propias del proyecto
        self.ultra_sonido.set_var(3.392639090737473)
        self.optico.set_var(9.341605062534653)
        # Aca se ponen parametros especificos del proyecto, por ejemplo valores de calibracion
        # U otras caracteristicas propias.
    
    def disconnect(self):
        """
        Desconecta el robot y fuerza la escritura de los datos de los sensores en archivos CSV antes de cerrar la conexión.
        """
        self.ultra_sonido.force_callback_buff_full()
        self.optico.force_callback_buff_full()
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
            "RX_RECORRIDO_SERVO" : "MOVR",
            "RX_MS_SENSOR_ULTRA_SONIDO" : "SENUS",
            "RX_MS_SENSOR_OPTICO" : "SENOP",
            "RX_MS_SENSOR_ACELEROMETRO" : "SENAC",
            "RX_MS_SENSOR_GIROSCOPO" : "SENGI",
            "RX_RECORRIDO_SERVO" : "MOVR",
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