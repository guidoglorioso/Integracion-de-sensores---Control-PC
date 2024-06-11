# README (English)
## Project Structure

This repository contains a Python project designed to interact with a distance measuring robot and abstract away from its specific controllers. The structure of the project is as follows:

**MedidorRobot**: This main object, implemented in the MedidorRobot.py file, represents the distance measuring robot. It provides an interface to control the robot through scripts and routines, allowing for measurements and characterization of the sensors and robot operation. It is primarily oriented towards conducting tests to evaluate the results.

**Robot Sensors**: Within MedidorRobot, specific sensors of the robot are defined, such as the ultrasonic sensor and the optical sensor.

**Robot**: Also included is the Robot object, which abstracts the robot's hardware and provides a generic interface to interact with it.

**Example Usage Scripts**: The repository contains several Python scripts demonstrating how to use the project's functionalities to take measurements, process data, and control the robot.

## Adapting the Project
The project structure is designed to facilitate adaptation to other robots without the need to modify existing controllers. Here's a guide to adapting this project to another robot:

**Create a New MedidorRobot Object**: Create a new Python object similar to the existing MedidorRobot, adapted to the specific requirements of your robot. Define the necessary sensors and any additional functionality required.

**Customize the Robot Sensors**: Within the MedidorRobot object, define the specific sensors for your robot, such as ultrasonic sensors, optical sensors, or others.

**Use the Generic Robot Object**: There's no need to modify the existing Robot object, as it provides a generic interface to interact with the robot's hardware.

## Interacting with the Robot
Interaction with the robot is done through a serial port, allowing commands to be sent to the robot to control its actions and receive data from the sensors. The structure is designed to make it easy to add new commands to control new robot hardware or add new functionalities.

## Robot Controller
The robot controller is located in the [Integracion-de-sensores---Microcontrolador](https://github.com/guidoglorioso/Integracion-de-sensores---Microcontrolador) repository. This controller is designed to interact with the robot's hardware and provide data through the interface established by the Python project. The robot controller receives serial commands to execute specific hardware actions.



# README (Español)
## Estructura del Proyecto
Este repositorio contiene un proyecto en Python diseñado para interactuar con un robot medidor de distancias y abstraerse de sus controladores específicos. La estructura del proyecto es la siguiente:

**MedidorRobot**: Este objeto principal, implementado en el archivo MedidorRobot.py, representa el robot medidor de distancias. Proporciona una interfaz para controlar el robot mediante scripts y rutinas, permitiendo realizar mediciones y caracterizar los sensores y el funcionamiento del robot. Está orientado principalmente a realizar pruebas para evaluar los resultados.

**Sensores del Robot**: Dentro de MedidorRobot, se definen los sensores específicos del robot, como el sensor ultrasónico y el sensor óptico.

**Robot**: También se incluye el objeto Robot, que abstrae el hardware del robot y proporciona una interfaz genérica para interactuar con él.

**Scripts de Ejemplos de Uso**: En el repositorio se encuentran varios scripts de Python que demuestran cómo utilizar las funcionalidades del proyecto para realizar mediciones, procesar datos y controlar el robot.

## Adaptando el Proyecto
La estructura del proyecto está diseñada para facilitar la adaptación a otros robots sin necesidad de modificar los controladores existentes. Aquí tienes una guía para adaptar este proyecto a otro robot:

**Crear un Nuevo Objeto MedidorRobot**: Crea un nuevo objeto en Python similar al MedidorRobot existente, adaptado a los requisitos específicos de tu robot. Define los sensores necesarios y cualquier funcionalidad adicional requerida.

**Personalizar los Sensores del Robot**: Dentro del objeto MedidorRobot, define los sensores específicos de tu robot, como sensores ultrasónicos, ópticos u otros.

**Utilizar el Objeto Robot Genérico**: No es necesario modificar el objeto Robot existente, ya que proporciona una interfaz genérica para interactuar con el hardware del robot.

## Interacción con el Robot
La interacción con el robot se realiza mediante un puerto serie, lo que permite enviar comandos al robot para controlar sus acciones y recibir datos de los sensores.

## Controlador del Robot
El controlador del robot se encuentra en el repositorio [Integracion-de-sensores---Microcontrolador](https://github.com/guidoglorioso/Integracion-de-sensores---Microcontrolador). Este controlador está diseñado para interactuar con el hardware del robot y proporcionar datos a través de la interfaz establecida por el proyecto en Python. El controlador del robot recibe comandos serie para ejecutar acciones de hardware específicas.