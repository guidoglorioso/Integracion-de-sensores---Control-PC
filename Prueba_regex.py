# import re

# # Example string
# example_string = "$COMMAND-123-456-789-5#"

# # Regular expression pattern to capture the command and integers
# pattern = r"\$(\w+)-(\d+(?:-\d+)*)#"

# # Match the pattern
# match = re.match(pattern, example_string)

# if match:
#     # Assign the command string to the variable
#     command = match.group(1)
    
#     # Extract all integers
#     integers = list(map(int, match.group(2).split('-')))
    
#     print("Command:", command)
#     print("Integers:", integers)
# else:
#     print("No match found.")

from time import sleep
from TorretaMedicion import TorretaMedicion
import matplotlib.pyplot as plt
from FuncionesProcesamiento import  *

mi_robot = TorretaMedicion(_puerto="COM5")
#mi_robot.set_csv_output(extra_text="prueba_") ## Activo la salida CSV de los sensores

# while True:
#     valores = mi_robot.get_sensor_optico().get_values()
#     print(valores)
#     sleep(1)
    
mi_robot.send_command("RX_TEST",[1,2,3,4,5])

print(mi_robot.test.get_values())

mi_robot.disconnect()   
