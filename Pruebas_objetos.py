from RobotObject import Robot
from SensorObject import Sensor
import time
mi_robot = Robot()

## TODO: poner todo en carpetas
# https://www.google.com/search?sca_esv=1fa53ef552df2eb8&rlz=1C1VDKB_enAR1046AR1046&sxsrf=ADLYWIJ9wfsUCxYr9Mr4Uj-8TR8PZwMZGQ:1717458533512&q=how+to+add+path+for+class+in+vscode+python&tbm=vid&source=lnms&prmd=visnbmtz&sa=X&ved=2ahUKEwiHqLnOz8CGAxUjr5UCHeuJCPQQ0pQJegQIDBAB&biw=1536&bih=729&dpr=1.25#fpstate=ive&vld=cid:c5c7c42d,vid:Ad-inC3mJfU,st:0


mi_robot.connect(puerto="COM5")


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
    # "TX_SENSOR_OPTICO" : "SENOPD",
    # "TX_SENSOR_ULTRA_SONIDO" : "SENUSD",

}

mi_robot.set_commands(comandos=comando)

ultra_sonido = Sensor()
optico = Sensor()
acelerometro_x = Sensor()
acelerometro_y = Sensor()
acelerometro_z = Sensor()
giroscopio_x = Sensor()
giroscopio_y = Sensor()
giroscopio_z = Sensor()

sensores = {
    "SENUSD" : ultra_sonido,
    "SENOPD" : optico,
    # "SENACX" : acelerometro_x,
    # "SENACY" : acelerometro_y,
    # "SENACZ" : acelerometro_z,
    # "SENGIX" : giroscopio_x,
    # "SENGIY" : giroscopio_y,
    # "SENGIZ" : giroscopio_z,

}

mi_robot.set_sensors(sensores)
mi_robot.start_sensor_log()

mi_robot.send_command("RX_MOV_SERVO",[90])
time.sleep(0.5)

mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO",[1])
time.sleep(0.5)
mi_robot.send_command("RX_MS_SENSOR_OPTICO",[1])
#mi_robot.send_command("RX_MS_SENSOR_ULTRA_SONIDO_ONETIME")

time.sleep(0.5)
while True:
    time.sleep(0.5)
    if ultra_sonido.queue_state() >0:
        print(f"US: {ultra_sonido.queue_pop()}")
    if optico.queue_state() >0:
        print(f"IR:{optico.queue_pop()}")    


mi_robot.disconnect()
