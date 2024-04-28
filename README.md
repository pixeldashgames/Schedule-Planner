# Schedule Planner

## Integrantes ##

- Leonardo Amaro
- Alfredo Montero
- Anthuán Montes de Oca

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

## Beneficios del Proyecto
- **Automatización**: Reduce el esfuerzo manual en la creación de horarios.
- **Optimización**: Encuentra una solución óptima considerando diversas restricciones.
- **Escalabilidad**: Puede manejar grandes conjuntos de datos y requerimientos de programación complejos.

## Mejoras Futuras
- Incorporar restricciones adicionales (preferencias de estudiantes, disponibilidad de aulas, etc.).
- Mejorar la interfaz de usuario para la entrada y visualización.

## Conclusión
El Planificador de Horarios optimiza el proceso de creación de horarios, garantizando eficiencia y precisión. Al aprovechar OR-Tools, proporciona una solución inteligente que satisface los requisitos de las instituciones educativas.