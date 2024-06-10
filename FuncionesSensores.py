from SensorObject import Sensor
import time
import numpy as np

# from filterpy.kalman import KalmanFilter

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



def crear_filtro_kalman(Sensores,TypeFilter):
    """Funcion que recibe N sensores y el nombre del filtro ya definido de kalman que se va a usar

    Args:
        Sensores (Sensor): Vector de sensores
        TypeFilter (str): Nombre del filtro definido

    Returns:
        _type_: Devuelve el objeto de kalman
    """    
    
    #TODO: Hacer la funcion que no sea hardcodeada y permita agregar mas sesnores y modos
    #TODO: Ya que se reciben los sensores, pedir su desvio para usar en la matriz R.


#     if TypeFilter == "FILTER_DISTANCE_TWO_SENSOR":

#         # Crear filtro de Kalman
#         kf = KalmanFilter(dim_x=2, dim_z=2)

#         kf.F = np.array([[1]])  # Matriz de estado
#         kf.H = np.array([[1], [1]])  # Matriz de observación
#         kf.Q = np.array([[0.01]])  # Covarianza del ruido de proceso
#         kf.R = np.array([[0.1, 0], [0, 0.1]])  # Covarianza del ruido de medición
#         kf.P = np.array([[1]])  # Covarianza inicial

#         # Estado inicial
#         kf.x = np.array([0])  # posición
                      
#     return kf



# def actualizar_filtro_kalman(kf, z_ultrasonido, z_optico):
#     z = np.array([[z_ultrasonido],
#                   [z_optico]])
    
#     # Predicción
#     kf.predict()
    
#     # Actualización
#     kf.update(z)
    
#     return kf.x

       