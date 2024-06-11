# Objeto especifico de proyecto. 
# Robot con servomotor para ubicar posicion de medicion, Sensores optico y de ultrasonido para medir distancia 
# y sensor de acelerometro y giroscopo para posicion.


# Dependecias
from RobotObject import Robot
from SensorObject import Sensor

class MedidorRobot(Robot):
    """Objeto dedicado a la interaccion con el proyecto de robot medidor de distancias.
    Hereda de la clase robot los metodos para usar
    """    
    def __init__(self,_puerto) -> None:
        """Inicializacion de objeto para interaccion con proyecto.
        """       

        # Inicializo el objeto robot para interactuar con el proyecto
        super().__init__()

        self._command_init()

        # Defino sensores y los asigno al objeto robot
        self.ultra_sonido = Sensor()
        self.optico = Sensor()

        self._sensor_init()
        
        # Conecto por serie
        self.connect(puerto=_puerto)

        # Inicializo la adquisicion de datos de sensores a los objetos "Sensor"
        self.start_sensor_log()

        ## Variables propias del proyecto
        self.ultra_sonido.Set_var(3.392639090737473)
        self.optico.Set_var(9.341605062534653)
        # Aca se ponen parametros especificos del proyecto, por ejemplo valores de calibracion
        # U otras caracteristicas propias.

    def _command_init(self):
        """Comandos para interactuar con el robot
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
        """Comandos de sensores que se reciben
        """        
        sensores = {
            "SENUSD" : self.ultra_sonido,
            "SENOPD" : self.optico,
        }
        
        self.set_sensors(sensores)

    def get_sensor_ultrasonido(self):
        return self.ultra_sonido
    
    def get_sensor_optico(self):
        return self.optico