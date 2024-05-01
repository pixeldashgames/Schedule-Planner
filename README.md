# Schedule Planner

## Integrantes ##

- Leonardo Amaro Rodríguez C411
- Alfredo Montero López C411
- Anthuán Montes de Oca C411

# Informe: Planificador de Horarios

## Descripción del Proyecto
El proyecto consiste en desarrollar un planificador de horarios utilizando la biblioteca OR-Tools en Python. El objetivo es generar horarios escolares o universitarios que cumplan con todas las restricciones y condiciones establecidas. El sistema debe considerar asignaturas, profesores, aulas, grupos de estudiantes, días y turnos.

## Componentes del Proyecto

1. **`solucion.py`**:
   - Contiene la lógica principal para resolver el problema del horario.
   - Utiliza OR-Tools para crear un modelo de restricciones con variables, restricciones y una función objetivo.
   - Verifica si la solución propuesta cumple con todas las condiciones (por ejemplo, disponibilidad de profesores, capacidad de las aulas, etc.).

2. **`utils.py`**:
   - Define clases para representar los parámetros del problema:
     - `Asignatura`: Representa una materia académica.
     - `Profesor`: Representa un docente.
     - `Aula`: Representa un espacio físico.
     - `Grupo`: Representa un grupo de estudiantes.
     - Otras clases para días, turnos, etc.

3. **`main.py`**:
   - Ejecuta el proceso de planificación del horario.
   - Inicializa los parámetros del problema (asignaturas, profesores, aulas, grupos, etc.).
   - Llama al solucionador desde `solucion.py`.
   - Recibe la solución optimizada del horario.

4. **`printer.py`**:
   - Contiene métodos para formatear y exportar la solución del horario.
   - Convierte la solución en un archivo Excel (llamado `output.xlsx`) con hojas separadas para cada grupo.
### Input
El programa lee la información de los parámetros del problema desde datos.json. Este archivo contiene la información de las asignaturas, profesores, aulas, grupos y restricciones del problema.
### Output
El programa genera un archivo Excel llamado output.xlsx que contiene el horario optimizado para cada grupo. Cada hoja del archivo Excel representa el horario de un grupo en particular.
## Reporte técnico
El modelo de optimización utilizado en este código es un problema de programación de restricciones (Constraint Programming, CP) que se resuelve utilizando la biblioteca OR-Tools de Google. 

El problema modelado es la planificación de horarios para un conjunto de grupos, asignaturas, profesores y aulas.  El modelo se basa en las siguientes entidades:
- Asignaturas: Cada asignatura tiene un tiempo asignado que representa la cantidad de horas que se deben programar para esa asignatura.
- Profesores: Cada profesor tiene una lista de asignaturas que puede enseñar.
- Grupos: Cada grupo tiene un conjunto de asignaturas que debe tomar.
- Aulas: Las aulas son los lugares donde se imparten las asignaturas.

Las restricciones del modelo son las siguientes:  
- Restricción de asignatura: Para cada grupo, todas las asignaturas deben ser programadas el número de horas especificado.
- Restricción de profesor: Un profesor solo puede estar en un aula a la vez.
- Restricción de aula: Solo se puede programar una asignatura en un aula en un turno específico.

El objetivo del modelo es encontrar una asignación de asignaturas a aulas y profesores que cumpla con todas las restricciones.  El código también incluye la capacidad de agregar restricciones opcionales, que son restricciones que el modelo intentará cumplir pero que no son obligatorias. Estas restricciones opcionales se pueden utilizar para modelar preferencias, como la preferencia de un profesor por enseñar en ciertos turnos o la preferencia de un grupo por tener ciertas asignaturas en ciertos días.  El modelo se resuelve utilizando el solucionador de programación de restricciones de OR-Tools. Una vez que se encuentra una solución, el código genera un horario que cumple con todas las restricciones y preferencias.

## Beneficios del Proyecto
- **Automatización**: Reduce el esfuerzo manual en la creación de horarios.
- **Optimización**: Encuentra una solución óptima considerando diversas restricciones.
- **Escalabilidad**: Puede manejar grandes conjuntos de datos y requerimientos de programación complejos.

## Mejoras Futuras
- Incorporar restricciones adicionales (preferencias de estudiantes, disponibilidad de aulas, etc.).
- Mejorar la interfaz de usuario para la entrada y visualización.

## Conclusión
El Planificador de Horarios optimiza el proceso de creación de horarios, garantizando eficiencia y precisión. Al aprovechar OR-Tools, proporciona una solución inteligente que satisface los requisitos de las instituciones educativas.