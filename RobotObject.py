# Dependecias
import serial
import SensorObject 
import threading
import re
import time

class Robot:
    """Objeto dedicado a la interaccion con el sistema "Robot"
    """    

    def __init__(self) -> None:
        """Inicializacion de objeto.
        """        
        
        ##  Inicializo valores iniciales para comunicacion serie
        self.serial_port = "COM1"
        self.serial_baudrate = 115200
        self.serial_timeout = 1 # ms
        self.serial_connection = False

        ## sensores
        self._sensores = False

        ## Seteo por defecto el verbose
        self.verbose = False

        ## Tiempo de demora entre comandos por default y tiempo actual
        self._command_interval = 200 / 1000 # 200ms
        self._last_command_time = time.time()

    ## Funciones conexion serie

    def connect(self, puerto : str): 
        """Inicializacion puerto serie. Intenta conectarse a un puerto especifico con datos por defecto
        baudrate = 115200, timeout = 1ms, bytesize = 8, parity = "N", stopbits = 1.

        Args:
            puerto (str): String con el nombre del puerto: "COMx"
        """        
        try:
            self.serial_port =puerto
            self.serial_connection = serial.Serial(self.serial_port, self.serial_baudrate, timeout=self.serial_timeout,)
            self.print_verbose(f"Conectado a {self.serial_port} a {self.serial_baudrate} baudios.")
        except serial.SerialException as e:
            self.serial_connection = False
            self.print_verbose(f"No se pudo conectar al puerto {self.serial_port}: {e}")

    def disconnect(self):
        """
        Desconexion del puerto serie. 
        """        
        self._stop_thread_sensor() # Finalizo los threads
        
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.print_verbose(f"Desconectado de {self.serial_port}.")

    def _read_data(self) -> str :
        """
        Lee toda una linea de datos del puerto serie.\n
        
        Returns:
            str:  Datos leídos del puerto serie, devuelve NONE en caso de fallo.
        """        
                
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().decode('utf-8').strip()
                self.print_verbose(data)
                return data
            except serial.SerialException as e:
                self.print_verbose(f"Error al leer del puerto {self.port}: {e}")
        return 0

    def _write_data(self, data:str):
        """
        Escribe datos en el puerto serie previamente conectado.\n
        ver metodo:\n
        connect()

        Args:
            data (str): Datos a escribir en el puerto serie.
        """        
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(data.encode('utf-8'))
                self.print_verbose(f"Datos enviados: {data}")
            except serial.SerialException as e:
                self.print_verbose(f"Error al escribir en el puerto {self.serial_port}: {e}")

    ## Seteo de comandos para el robot

    def set_commands(self, comandos: dict):
        """Asignacion de comandos para acciones. \n 
        Ejemplo de uso:\n
        comandos = {\n
        "MOVER ADELANTE" : "$MOV1",\n
        "MOVER ATRAS" : "$MOV2",\n
        "MOVER COSTADO" : "$MOV3"\n
        }\n
        set_commands(comandos)\n

        Args:
            comandos (dict): Diccionario con keys "Nombres de comandos" y values "Trama del comando"

        """        
        if not isinstance(comandos, dict):
            raise TypeError("El parámetro 'comandos' debe ser un diccionario")

        for comando, trama in comandos.items():
            if not isinstance(comando, str):
                raise ValueError("Las claves del diccionario deben ser cadenas (str)")
            if not isinstance(trama, str):
                raise ValueError("Los valores del diccionario deben ser cadenas (str)")

        self._comandos = comandos

    def get_commands(self)->dict:
        """Devuelve la lista de comandos seteados y sus tramas.

        Returns:
            dict: Lista de comandos y sus tramas
        """        
        return self._comandos
    
    def send_command(self, comando: str, data: list[int] = []):
        """ Envía la trama asociada al comando por el puerto serie.\n
        Nota: Entre comandos se requiere un tiempo minimo, en caso de que no haya transcurrido \n
        ese tiempo esta funcion se bloquea y espera a que se cumpla el tiempo entre comandos.
        El tiempo entre comandos esta determinado por el metodo Set_interval().

        Args:
            comando (str): comando a enviar
            data (list[int]): parametros que se quieren enviar en el comando (0 a 255)

        """   
        # Control de errores
         
        if not self.serial_connection or not self.serial_connection.is_open:
            self.print_verbose("Error: No está conectado al puerto serie.")
            return

        if comando not in self._comandos:
            self.print_verbose(f"Error: Comando '{comando}' no está definido.")
            return
        
        #Armo la trama
        trama = "$"
        trama += self._comandos[comando] ## Agarro la trama correspondiente.
        
        # Detecto si hay argumentos para enviar y los concateno
        if len(data) > 0:
            trama += "-" 

        for this_data in data:
            trama += str(this_data)
            
        trama += "#"

        # Chequeo que haya pasado el tiempo minimo entre comandos
        current_time = time.time()
        time_since_last_command = current_time - self._last_command_time

        # Si todavia no termino la espera bloqueo la funcion hasta que se cumpla el tiempo
        if time_since_last_command < self._command_interval:
            wait_time = self._command_interval - time_since_last_command
            self.print_verbose(f"Esperando {wait_time:.2f} segundos para enviar el próximo comando.")
            time.sleep(wait_time)

        # Envio la trama por serie
        self._write_data(trama)

        # Actualizo el tiempo del ultimo comando enviado
        self._last_command_time = time.time()

        self.print_verbose(f"Comando '{comando}' enviado: {trama}")
        

    def Set_interval(self, interval):
        """" Funcion que permite cambiar el tiempo de demora entre comandos.
        El tiempo maximo que se puede asignar son 2 Seg
        Args:
            interval (_type_): tiempo entre comandos en mS
        """        
        if interval<2000:
            self._command_interval = interval / 1000
        else:
            self.print_verbose("Valor maximo de intervalo 2000mS")

    #######################################################################
    ## Configuracion de un sensor

    def set_sensors(self, mapeo_comandos: dict):
        """
        Guarda los comandos y objetos sensores para luego poder ser usados.\n
        Ejemplo de uso:\n

        sensor_ultrasonido = Sensor()\n
        sensor_infrarrojo = Sensor()\n
        mapeo_comandos = {\n
            "Sen1": sensor_ultrasonido,\n
            "Sen2": sensor_infrarrojo\n
        }\n

        Args:
        mapeo_comandos (dict): Diccionario que mapea comandos a sensores.

        """
        # Verificar si mapeo_comandos es un diccionario
        if not isinstance(mapeo_comandos, dict):
            self.print_verbose("Error: Se esperaba un diccionario.")
            return

        # Verificar si los valores del diccionario son instancias de la clase Sensor
        for comando, sensor in mapeo_comandos.items():
            if not isinstance(sensor, SensorObject.Sensor):
                self.print_verbose(f"Error: El valor asociado al comando '{comando}' no es una instancia de la clase Sensor.")
                return
        self._sensores = mapeo_comandos
            
    def _map_sensor(self, sensor_comand : dict):
        """Esta funcion recibe un diccionario que asocia un comando a un objeto Sensor.
        Luego cuando se recibe ese comando se llamara al objeto sensor asociado y se ingresara el
        valor por medio de "queue_insert()"
        Ejemplo de uso:

        sensor_ultrasonido = Sensor()
        sensor_infrarrojo = Sensor()
        mapeo_comandos = {
            "Sen1": sensor_ultrasonido,
            "Sen2": sensor_infrarrojo
        }

        map_sensor(mapeo_comandos)

        Args:
            sensor_comand (dict): Diccionario con key "comando" y valor asignado el objeto a asociar
        """        
        def recibir_trama(trama):
            for comando, objeto in sensor_comand.items():
                if comando in trama: # Chequeo coincidencia con la trama
                    apariciones = self.extraer_valor(trama,comando)
                    if apariciones != None:
                        for aparicion in apariciones:
                            objeto.queue_insert(aparicion)

        return recibir_trama
    


    def extraer_valor(self, cadena,comando):
    # Busca el patrón indicado en una cadena y devuelve todos los numeros enteros que le sigan
        patron = rf'\$\{comando}(\d+)#'
    # Realiza la búsqueda en la cadena
        coincidencia = re.findall(patron, cadena)
    
        if coincidencia:
            # Devuelve el valor numérico encontrado
            return [int(this_coincidencia) for this_coincidencia in coincidencia]
        else:
            # Si no encuentra coincidencias, devuelve None o un valor predeterminado
            return None
    
    def _stop_thread_sensor(self):
        """
        Termina el thread para recibir datos a sensores.
        """        
        self._flag_thread_sensor = False

    def mannage_Rx(self):
        """Thread para recibir datos. Para matar este thread usar: _stop_thread_sensor()\n
        Para revivirlo usar start_sensor_log()
        """        
        self._flag_thread_sensor = True
        while self._flag_thread_sensor: ## Es un proceso corriendo
            if self.serial_connection.in_waiting > 0:
                dato_recibido = self._read_data()
                self.Function_recept(dato_recibido)
                self.print_verbose(f"Dato recibido:{dato_recibido}")

    def start_sensor_log(self):
        """Arranca el proceso de asignacion de datos por serie a los sensores.
        """        
        if self._sensores: 
            self.Function_recept = self._map_sensor(self._sensores)
            # Crear un hilo para leer datos del puerto serie
            self.hilo_lectura = threading.Thread(target=self.mannage_Rx, daemon=True)
            self.hilo_lectura.start()
        else:
            self.print_verbose("No se agregaron los sensores")

    
    ###########################################################################

    def verbose(self,mode = False):
        """Prender o apagar verbose

        Args:
            mode (bool, optional): Defaults to False.
        """
        self.verbose = mode

    def print_verbose(self, text):
        """verbose de funciones

        Args:
            text (): texto a imprimir
        """        
        if self.verbose == True:
            print(text)
