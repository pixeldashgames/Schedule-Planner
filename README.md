# Schedule Planner

## Integrantes ##

- Leonardo Amaro Rodríguez C411
- Alfredo Montero López C411
- Anthuán Montes de Oca C411


## Como usar el programa
Para ejecutar el programa solamente tiene que ejecutar el archivo main.py usando el comando `py main.py`.

Para entrar los datos solo tiene que llenar los datos en datos.json .

El json tiene la forma:

      {
   
         "subjects": [],   // Nombres de las asignaturas

         "subject_times": { asignatura : número },   // Cantidad de turnos por semana que debe tener cada asignatura

         "teachers": [],   // Nombres de todos los profesores

         "classrooms": [],  // Nombres de las aulas

         "groups": [],  // Nombres de los grupos

         "group_subject_times": { grupo : { asignatura : frecuencia }}, // Frecuencia que debe tener cada asignatura por cada grupo en la semana

         "shifts": [],  // Turnos existentes en el día

         "days": [],  // Días de la semana que se van programar

         "teachers_to_subjects": { profesor : [ asignatura ] }  // Asignación de cada profesor a su asignatura correspondiente

         "hards_true": {
            "(nombre de la restriccion)": {  
            "teachers_names": [],
            "subjects_names": [],
            "classrooms_names": []
            "groups_names": []],
            "shifts": [],
            "days": []
            },
            ...
         },  // Restricciones que deben cumplirse

         "hards_false": {

            "(nombre de la restriccion)":{  
               "teachers_names": [],
               "subjects_names": [],
               "classrooms_names": [],
               "groups_names": [],
               "shifts": [],
               "days": []
            },
            ...
         }, // Restricciones que deben  no cumplirse

         "softs_max": {
            (nombre de la restriccion):{  
               "teachers_names": [],
               "subjects_names": [],
               "classrooms_names": [],
               "groups_names": [],
               "shifts": [],
               "days": [],
               "alpha": (number)
            },
            ...
         },

         "softs_min": {
            (nombre de la restriccion):{  
               "teachers_names": [],
               "subjects_names": [],
               "classrooms_names": [],
               "groups_names": [],
               "shifts": [],
               "days": [],
               "alpha": (number)
            },
            ...
         },
      }

Se puede basar en los datos de ejemplo ya existentes en el json.

# Informe: Planificador de Horarios

## Descripción del Proyecto
Este proyecto fue realizado para dar solución al problema de la confección del horario de MATCOM. El objetivo de este trabajo es diseñar e implementar una aplicación para la confección automática del horario en MATCOM.  Se tienen en cuenta las restricciones reales a la hora de confeccionar el horario en la facultad.

El proyecto se desarrolló utilizando la biblioteca OR-Tools en Python. El sistema considera asignaturas, profesores, aulas, grupos de estudiantes, días y turnos.

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
# Reporte técnico
El modelo de optimización utilizado en este código es un problema de programación de restricciones (Constraint Programming, CP) que se resuelve utilizando la biblioteca OR-Tools de Google. 

La Programación de Restricciones es un paradigma de programación declarativa que permite codificar problemas de decisión complejos modelando sus restricciones y buscando soluciones que las satisfagan. En lugar de especificar un procedimiento paso a paso para llegar a la solución, en la Programación de Restricciones se describe el problema en términos de variables y restricciones sobre estas variables.

El solucionador de Programación de Restricciones de OR-Tools, llamado CP-SAT, utiliza un algoritmo de búsqueda basado en backtracking para explorar el espacio de soluciones, y técnicas de propagación de restricciones para reducir este espacio.

El modelo matemático subyacente en la Programación de Restricciones es un problema de satisfacción de restricciones (CSP), que se puede formular de la siguiente manera:

Se tiene un conjunto de variables, cada una con un dominio de posibles valores.
Se tienen restricciones que especifican las combinaciones de valores que las variables pueden tomar.
El objetivo es encontrar una asignación de valores a las variables que satisfaga todas las restricciones. En algunos casos, también se puede buscar la mejor solución según una función objetivo.

El problema modelado es la planificación de horarios para un conjunto de grupos, asignaturas, profesores y aulas.  El modelo se basa en las siguientes entidades:
- Asignaturas: Cada asignatura tiene un tiempo asignado que representa la cantidad de horas que se deben programar para esa asignatura.
- Profesores: Cada profesor tiene una lista de asignaturas que puede enseñar.
- Grupos: Cada grupo tiene un conjunto de asignaturas que debe tomar.
- Aulas: Las aulas son los lugares donde se imparten las asignaturas.

Las restricciones del modelo son las siguientes:  
- Restricciones de asignación de asignaturas a grupos: En la clase PlanificadorHorario, se crea una variable booleana para cada combinación de profesor, asignatura, aula, grupo, turno y día. Luego, se agrega una restricción al modelo que dice que la suma de estas variables para una asignatura y grupo dados, en todos los profesores, aulas, turnos y días, debe ser igual al tiempo asignado a esa asignatura. Esto significa que cada asignatura debe ser asignada a cada grupo para el número correcto de turnos. 
- Restricciones de asignación de profesores: En la clase RestriccionProfesor, se crea una variable booleana para cada combinación de día, turno, profesor y aula. Luego, se agrega una restricción al modelo que dice que la suma de estas variables para un profesor dado, en un día y turno específicos, y en todas las aulas, debe ser menor o igual a 1. Esto significa que un profesor solo puede estar en una aula en un turno y día específicos. 
- Restricciones de asignación de aulas: En la clase RestriccionAula, se crea una variable booleana para cada combinación de día, turno, asignatura y aula. Luego, se agrega una restricción al modelo que dice que la suma de estas variables para una asignatura dada, en un día y turno específicos, y en todas las aulas, debe ser menor o igual a 1. Esto significa que una asignatura solo puede ser asignada a una aula en un turno y día específicos.
- Restricciones opcionales: Las restricciones opcionales se manejan a través de los métodos agregar_restricciones_hard_opcionales, agregar_restricciones_hard_falsas, agregar_restricciones_hard_verdaderas, agregar_restricciones_suaves_maximizar y agregar_restricciones_suaves_minimizar. Estos métodos permiten agregar restricciones adicionales al modelo que pueden ser verdaderas o falsas, y que el modelo intentará maximizar o minimizar.
El objetivo del modelo es encontrar una asignación de asignaturas a aulas y profesores que cumpla con todas las restricciones.  El código también incluye la capacidad de agregar restricciones opcionales, que son restricciones que el modelo intentará cumplir pero que no son obligatorias. El modelo se resuelve utilizando el solucionador de programación de restricciones de OR-Tools. Una vez que se encuentra una solución, el código genera un horario que cumple con todas las restricciones y preferencias.

## Beneficios del Proyecto
- **Automatización**: Reduce el esfuerzo manual en la creación de horarios.
- **Optimización**: Encuentra una solución óptima considerando diversas restricciones.
- **Escalabilidad**: Puede manejar grandes conjuntos de datos y requerimientos de programación complejos.

## Mejoras Futuras
- Incorporar restricciones adicionales (preferencias de estudiantes, disponibilidad de aulas, etc.).
- Mejorar la interfaz de usuario para la entrada y visualización.

## Conclusión
El Planificador de Horarios optimiza el proceso de creación de horarios, garantizando eficiencia y precisión. Al aprovechar OR-Tools, proporciona una solución inteligente que satisface los requisitos de las instituciones educativas.