from SensorObject import Sensor
import time
import numpy as np

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



       