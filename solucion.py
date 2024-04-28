from ortools.constraint_solver.pywrapcp import IntVar
from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import CpModel
from utils import Calendario
from printer import to_data_frame
from aJson import Grupo

class BaseDeResoluciónDeHorarios:
    def _verificar_existencia_en_lista(self, lista_a_verificar: list[str | int], lista_correcta: list[str | int], tipo_nombre: str):
        """
        Este método verifica que para las restricciones que se añaden, los profesores son los que se añadieron inicialmente.
        :param lista_a_verificar: La lista que se verifica para las nuevas restricciones.
        :param lista_correcta: La lista guardada en esta instancia de la clase.
        :param tipo_nombre: Si es un profesor, asignatura o aula.
        :return:
        """
        for elemento in lista_a_verificar:
            if elemento not in lista_correcta:
                raise Exception(f'El {tipo_nombre}: {elemento} no existe')

    def verificar_asignaturas_por_tiempo(self, lista_nombres_asignaturas: list[str], diccionario_asignaturas_por_tiempo: dict[str, int]):
        longitud_diccionario = len(diccionario_asignaturas_por_tiempo)
        longitud_lista = len(lista_nombres_asignaturas)
        if longitud_lista != longitud_diccionario:
            raise Exception(f'La longitud de lista_nombres_asignaturas:{longitud_lista} y la longitud de las claves de diccionario_asignaturas_por_tiempo:{longitud_diccionario} ')
        for elemento in lista_nombres_asignaturas:
            if elemento not in diccionario_asignaturas_por_tiempo:
                raise Exception(f'La asignatura {elemento} no tiene tiempo asignado')

    def verificar_asignatura_por_grupo(self, diccionario_asignaturas_por_tiempo: dict[str, int],
                                       diccionario_grupo_asignatura_tiempo: dict[str, dict[str, int]], nombres_grupos: list[str]):
        """
        Verifica que en cada grupo se tengan asignaturas correctas y que estas tengan al menos el mínimo de horas estipulado.
        :param diccionario_asignaturas_por_tiempo:
        :param diccionario_grupo_asignatura_tiempo:
        :param nombres_grupos:
        :return:
        """
        # Comprobar que los nombres de los grupos coinciden, es decir, que lo que está en el diccionario sea correcto.
        self._verificar_existencia_en_lista(diccionario_grupo_asignatura_tiempo.keys(), nombres_grupos, "Grupo")

        # Comprobar por los grupos.
        for grupo in nombres_grupos:
            # Si el grupo no tiene materias.
            if grupo not in diccionario_grupo_asignatura_tiempo:
                raise Exception(f'El grupo:{grupo} no tiene asignaturas asignadas')
            # Asignaturas por equipos.
            diccionario_grupo_asignatura = diccionario_grupo_asignatura_tiempo[grupo]
            # Ver por cada asignatura asignada a los equipos.
            for asignatura in diccionario_grupo_asignatura.keys():
                # Comprobar que el tiempo asignado a la asignatura en ese grupo sea mayor o igual al asignado globalmente.
                tiempo_asignado_grupo_asignatura: int = diccionario_grupo_asignatura[asignatura]
                # Comprobar que la asignatura asignada a este grupo exista, dado que diccionario_asignaturas_por_tiempo se verificó contra las asignaturas anteriormente.
                if asignatura not in diccionario_asignaturas_por_tiempo:
                    raise Exception(f'En el grupo:{grupo} la asignatura: {asignatura} no existe')
                tiempo_minimo_asignatura: int = diccionario_asignaturas_por_tiempo[asignatura]
                # Si el tiempo asignado a la asignatura es menor que el mínimo, se lanza un error.
                if tiempo_asignado_grupo_asignatura < tiempo_minimo_asignatura:
                    raise Exception(
                        f'En el grupo:{grupo} la asignatura {tiempo_asignado_grupo_asignatura} horas y tiene un mínimo de {tiempo_minimo_asignatura} horas')

    def verificar_nombres_asignaturas(self, lista_nombres: list[str], conjunto_nombres_totales: set[str], nombre_profesor: str):
        for nombre in lista_nombres:
            if nombre not in conjunto_nombres_totales:
                raise Exception(f'El profesor:{nombre_profesor} tiene la asignatura:{nombre} y esta no existe')
            
    def verificar_profesores(self, nombres_profesores: list[str], diccionario_profesores_a_asignaturas: dict[str, list[str]],
                             lista_nombres_asignaturas: list[str]):
        for profesor in nombres_profesores:
            if profesor not in diccionario_profesores_a_asignaturas:
                raise Exception(f'El profesor:{profesor} no tiene asignaturas asignadas')
            lista_asignaturas_profesor: list[str] = diccionario_profesores_a_asignaturas[profesor]

            # Verificar que existan menos o igual cantidad de asignaturas asignadas al profesor que las que realmente existen.
            longitud_lista_asignaturas_profesor = len(lista_asignaturas_profesor)
            if longitud_lista_asignaturas_profesor > len(lista_nombres_asignaturas):
                raise Exception(
                    f'El profesor:{profesor} no puede tener más asignaturas asignadas:{longitud_lista_asignaturas_profesor} que las asignaturas reales:{len(lista_nombres_asignaturas)}')
            # Verificar que las asignaturas que tenga el profesor sean válidas.
            self.verificar_nombres_asignaturas(lista_asignaturas_profesor, set(lista_nombres_asignaturas), profesor)

    def verificar(self, lista_nombres_materias: list[str], dict_materias_por_tiempo: dict[str:int], lista_nombres_profesores: list[str],
                  lista_nombres_grupos: list[str], dict_grupo_materia_tiempo: dict[str, dict[str:int]],
                  dict_profesores_a_materias: dict[str, list[str]]):
        self.verificar_asignaturas_por_tiempo(lista_nombres_materias, dict_materias_por_tiempo)
        self.verificar_asignatura_por_grupo(dict_materias_por_tiempo, dict_grupo_materia_tiempo, lista_nombres_grupos)
        self.verificar_profesores(lista_nombres_profesores, dict_profesores_a_materias, lista_nombres_materias)

    def __init__(self, lista_nombres_materias: list[str], dict_materias_por_tiempo: dict[str, int], lista_nombres_profesores: list[str],
                 lista_nombres_aulas: list[str],
                 lista_nombres_grupos: list[str], dict_grupo_materia_tiempo: dict[str, dict[str, int]], turnos: list[int],
                 dias: list[int], dict_profesores_a_materias: dict[str, list[str]]):

        # Verificar que los datos no tengan errores entre ellos
        self.verificar(lista_nombres_materias, dict_materias_por_tiempo, lista_nombres_profesores, lista_nombres_grupos, dict_grupo_materia_tiempo,
                       dict_profesores_a_materias)

        self.lista_nombres_materias: list[str] = lista_nombres_materias
        self.dict_materias_por_tiempo: dict[str:int] = dict_materias_por_tiempo
        self.lista_nombres_profesores: list[str] = lista_nombres_profesores
        self.lista_nombres_aulas: list[str] = lista_nombres_aulas
        self.lista_nombres_grupos: list[str] = lista_nombres_grupos
        self.dict_grupo_materia_tiempo: dict[str, dict[str, int]] = dict_grupo_materia_tiempo
        self.turnos: list[int] = turnos
        self.dias: list[int] = dias
        self.dict_profesores_a_materias: dict[str, list[str]] = dict_profesores_a_materias

        self._variables: dict = {}

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, valor):
        self._variables = valor

class RestriccionAula(BaseDeResoluciónDeHorarios):
    def __init__(self, lista_nombres_materias: list[str], dict_materias_por_tiempo: dict[str, int], lista_nombres_profesores: list[str],
                 lista_nombres_aulas: list[str],
                 lista_nombres_grupos: list[str], dict_grupo_materia_tiempo: dict[str, dict[str, int]], turnos: list[int],
                 dias: list[int], dict_profesores_a_materias: dict[str, list[str]], modelo: CpModel):
        super().__init__(lista_nombres_materias, dict_materias_por_tiempo, lista_nombres_profesores,
                         lista_nombres_aulas,
                         lista_nombres_grupos, dict_grupo_materia_tiempo, turnos,
                         dias, dict_profesores_a_materias)

        self.modelo = modelo

        self.iniciar()

    def iniciar(self):
        self.crear_variables()
        self.restriccion_natural_variables()

    def crear_variables(self):
        """
        Crea la variable necesaria para indicar que
        se debe de asignar en un turno a un aula una
        sola asignatura
        """
        # Solo se puede asignar a un aula una materia un día x
        # Crear variables para esto

        for dia in self.dias:
            for turno in self.turnos:
                for materia in self.lista_nombres_materias:
                    for aula in self.lista_nombres_aulas:
                        self.variables[dia, turno, materia, aula] = self.modelo.NewBoolVar(
                            f'Variable auxiliar: aula:{aula},asignatura:{materia},turno:{turno},dia:{dia}   '
                        )

    def restriccion_natural_variables(self):
        # Que en un turno de un día x en un aula solo se pueda dar una materia
        for dia in self.dias:
            for turno in self.turnos:
                for aula in self.lista_nombres_aulas:
                    s = sum(self.variables[dia, turno, materia, aula]
                            for materia in self.lista_nombres_materias
                            )
                    self.modelo.add(s <= 1)

class RestriccionProfesor(BaseDeResoluciónDeHorarios):
    def __init__(self, lista_nombres_materias: list[str], dict_materias_por_tiempo: dict[str, int], lista_nombres_profesores: list[str],
                 lista_nombres_aulas: list[str],
                 lista_nombres_grupos: list[str], dict_grupo_materia_tiempo: dict[str, dict[str, int]], turnos: list[int],
                 dias: list[int], dict_profesores_a_materias: dict[str, list[str]], modelo: CpModel):
        super().__init__(lista_nombres_materias, dict_materias_por_tiempo, lista_nombres_profesores,
                         lista_nombres_aulas,
                         lista_nombres_grupos, dict_grupo_materia_tiempo, turnos,
                         dias, dict_profesores_a_materias)

        self.modelo = modelo

        self.iniciar()

    def iniciar(self):
        # Crear las variables para el tipo de restricción del profesor en una sola aula
        self.crear_variables()
        # Declarar la restricción sobre las variables anteriores que un profesor en un
        # turno puede estar a lo sumo en un aula
        self.restriccion_natural_variables()

    def crear_variables(self):
        # Variable para decir que un profesor puede estar en una sola aula en un turno en específico
        for dia in self.dias:
            for turno in self.turnos:
                for profesor in self.lista_nombres_profesores:
                    for aula in self.lista_nombres_aulas:
                        self.variables[dia, turno, profesor, aula] = self.modelo.NewBoolVar(
                            f'Variable auxiliar: profesor:{profesor},aula:{aula},turno:{turno},dia:{dia}   '
                        )

    def restriccion_natural_variables(self):
        """
        Aquí toma las variables inicializadas en esta clase y dice
        que un profesor en un día y turno puede estar a lo sumo en un aula.
        """
        # Que un profesor solo puede estar en un aula a la vez
        for dia in self.dias:
            for turno in self.turnos:
                for profesor in self.lista_nombres_profesores:
                    s = sum(self.variables[dia, turno, profesor, aula]
                            for aula in self.lista_nombres_aulas
                            )
                    self.modelo.add(s <= 1)


class RestriccionesOpcionales(BaseDeResoluciónDeHorarios):
    def __init__(self, lista_nombres_materias: list[str], dict_materias_por_tiempo: dict[str, int], lista_nombres_profesores: list[str],
                 lista_nombres_aulas: list[str],
                 lista_nombres_grupos: list[str], dict_grupo_materia_tiempo: dict[str, dict[str, int]], turnos: list[int],
                 dias: list[int], dict_profesores_a_materias: dict[str, list[str]], modelo: CpModel):
        super().__init__(lista_nombres_materias, dict_materias_por_tiempo, lista_nombres_profesores,
                         lista_nombres_aulas,
                         lista_nombres_grupos, dict_grupo_materia_tiempo, turnos,
                         dias, dict_profesores_a_materias)

        self.modelo = modelo


class PlanificadorHorario(BaseDeResoluciónDeHorarios):
    def _lista_para_dataframe(self, profesor, asignatura, aula, grupo, turno, dia) -> list[dict]:
        datos = []
        # Agregar los datos a la lista como un diccionario
        datos.append({
            'Profesor': profesor,
            'Asignatura': asignatura,
            'Aula': aula,
            'Grupo': grupo,
            'Turno': turno,
            'Día': dia
        })
        return datos

    def _obtener_dic_materias_a_profesores(self, profesores: list[str], asignaturas: list[str],
                                           dict_profesores_a_materias: dict[str, list[str]]) -> dict[str, list[str]]:
        respuesta: dict[str, list[str]] = {}
        # Inicializar el diccionario
        for nombre_asignatura in asignaturas:
            respuesta[nombre_asignatura] = []

        # Asignar profesores a cada asignatura
        for nombre_profesor in profesores:
            lista_asignaturas: list[str] = dict_profesores_a_materias[nombre_profesor]
            for nombre_asignatura in lista_asignaturas:
                respuesta[nombre_asignatura].append(nombre_profesor)

        return respuesta

    def __init__(self, lista_nombres_materias: list[str], dict_materias_por_tiempo: dict[str, int],
                 lista_nombres_profesores: list[str], lista_nombres_aulas: list[str],
                 lista_nombres_grupos: list[str], dict_grupo_materia_tiempo: dict[str, dict[str, int]], turnos: list[int],
                 dias: list[int], dict_profesores_a_materias: dict[str, list[str]]):
        super().__init__(lista_nombres_materias, dict_materias_por_tiempo, lista_nombres_profesores,
                         lista_nombres_aulas,
                         lista_nombres_grupos, dict_grupo_materia_tiempo, turnos,
                         dias, dict_profesores_a_materias)

        self.dict_materias_a_profesores = self._obtener_dic_materias_a_profesores(lista_nombres_profesores,
                                                                                  lista_nombres_materias,
                                                                                  dict_profesores_a_materias)

        # Crear el modelo
        self.modelo = cp_model.CpModel()

        # Objeto calendario para verificar que las soluciones satisfacen las restricciones
        self.calendario = Calendario(lista_nombres_materias, lista_nombres_profesores, self.dict_materias_a_profesores,
                                     self.dict_grupo_materia_tiempo, len(self.dias),
                                     len(self.turnos),
                                     lista_nombres_aulas, lista_nombres_grupos)

        # Argumentos para instanciar las clases de restricciones que involucran más variables
        args = (lista_nombres_materias, dict_materias_por_tiempo, lista_nombres_profesores, lista_nombres_aulas,
                lista_nombres_grupos,
                dict_grupo_materia_tiempo, turnos, dias, dict_profesores_a_materias, self.modelo)
        # Instanciar las restricciones del profesor
        self._restricciones_profesor = RestriccionProfesor(*args)
        # Instanciar las restricciones del aula
        self._restricciones_aula = RestriccionAula(*args)

        # Diccionario de grupo a su lista de asignaturas:
        self.dict_grupo_asignatura: dict[str, list[str]] = {}

        # Llamar al método de inicio
        self.iniciar()

    @property
    def restricciones_profesor(self):
        return self._restricciones_profesor

    def crear_diccionario_grupos_asignaturas(self):
        for grupo in self.lista_nombres_grupos:
            lista_asignaturas = []
            diccionario = self.dict_grupo_materia_tiempo[grupo]
            for asignatura in self.lista_nombres_materias:
                if asignatura in diccionario:
                    lista_asignaturas.append(asignatura)

            if grupo in self.dict_grupo_asignatura:
                raise Exception(f"El grupo {grupo} no puede existir dos veces")
            self.dict_grupo_asignatura[grupo] = lista_asignaturas

    def iniciar(self):
        self._crear_variables_problema()

        self.crear_diccionario_grupos_asignaturas()

        # Llamar las restricciones fuertes

        self.iniciar_restricciones_hard()

        # Luego las de prueba

    def iniciar_restricciones_hard(self):
        """
        Inicializa las restricciones hard
        """
        self._restricciones_hard_globales()
        self._restricciones_hard_profesores()
        self._restricciones_hard_aulas()

    def _crear_variables_problema(self):
        """
        Instancia el problema original.
        """
        self.vars = {}
        for dia in self.dias:
            for turno in self.turnos:
                for grupo in self.lista_nombres_grupos:
                    for asignatura in self.lista_nombres_materias:
                        for aula in self.lista_nombres_aulas:
                            for profesor in self.lista_nombres_profesores:
                                self.vars[profesor, asignatura, aula, grupo, turno, dia] = self.modelo.NewBoolVar(
                                    f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}')

    def obtener_variable(self, nombre_profesor: str, nombre_asignatura: str, nombre_aula: str, nombre_grupo: str, turno_int: int,
                        dia_int: int):
        try:
            if not (isinstance(turno_int, int) and isinstance(dia_int, int)):
                raise Exception(f"El turno:{type(turno_int)} o el dia:{type(dia_int)} no se ha dado como entero")
            if not (nombre_profesor, nombre_asignatura, nombre_aula, nombre_grupo, turno_int, dia_int) in self.vars:
                raise Exception(
                    f"La llave {(nombre_profesor, nombre_asignatura, nombre_aula, nombre_grupo, turno_int, dia_int)} , no se encuentra en las variables globales")
            return self.vars[nombre_profesor, nombre_asignatura, nombre_aula, nombre_grupo, turno_int, dia_int]
        except Exception as e:
            raise Exception(f'Error en obtener_variable: {str(e)}')
        
    def _verificar_si_grupo_no_puede_tomar_asignatura_y_profesor(self, nombre_asignatura: str, nombre_grupo: str, nombre_profesor: str):
        diccionario = self.dict_grupo_materia_tiempo[nombre_grupo]
        return nombre_asignatura in diccionario and nombre_asignatura in self.dict_profesores_a_materias[nombre_profesor]


    def verificar_si_grupo_puede_tomar_asignatura(self, nombre_asignatura: str, nombre_grupo: str):
        dic = self.dict_grupo_materia_tiempo[nombre_grupo]
        return nombre_asignatura in dic

    def _obtener_lista_de_asignaturas_posibles_para_grupo(self, nombre_grupo: str) -> list[str]:
        if nombre_grupo not in self.dict_grupo_asignatura:
            raise Exception(f'El grupo {nombre_grupo} no se encuentra en el dict_grupo_asignatura')
        return self.dict_grupo_asignatura[nombre_grupo]

    def _restricciones_hard_globales(self):
        """
        Restricciones hard globales
        """
        # Asegurar que todos los turnos de cada asignatura se asignen a cada grupo
        for grupo in self.lista_nombres_grupos:
            for asignatura in self._obtener_lista_de_asignaturas_posibles_para_grupo(grupo):
                s = sum(
                    self.vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in self.lista_nombres_profesores for aula in
                    self.lista_nombres_aulas
                    for turno in self.turnos for dia in self.dias if
                    self._verificar_si_grupo_no_puede_tomar_asignatura_y_profesor(asignatura, grupo, profesor))
                self.modelo.add(s == self.dict_materias_por_tiempo[asignatura])

        # Asegurar que las asignaturas que no corresponden a un grupo tengan suma 0
        for grupo in self.lista_nombres_grupos:
            s = sum(self.vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in self.lista_nombres_profesores for aula in
                    self.lista_nombres_aulas
                    for turno in self.turnos for dia in self.dias
                    for asignatura in self.lista_nombres_materias
                    if asignatura
                    not in self._obtener_lista_de_asignaturas_posibles_para_grupo(grupo))
            self.modelo.add(s == 0)

        # Asegurar que un grupo pueda estar en un turno en una sola aula dando una sola asignatura
        for dia in self.dias:
            for turno in self.turnos:
                for grupo in self.lista_nombres_grupos:
                    s = sum(self.vars[profesor, asignatura, aula, grupo, turno, dia] for profesor in self.lista_nombres_profesores
                            for asignatura in self.lista_nombres_materias
                            for aula in self.lista_nombres_aulas
                            if asignatura in self.dict_profesores_a_materias[profesor])
                    self.modelo.add(s <= 1)

    def _restricciones_hard_profesores(self):
        """
        Aquí se inicializa la restricción de que un profesor en un turno solo puede estar en un aula al mismo tiempo.
        :return:
        """

        # Para todos los grupos, aseguramos que se den todos los turnos, pero también que un profesor esté en un solo aula.
        for asignatura in self.lista_nombres_materias:
            for grupo in self.lista_nombres_grupos:
                for profesor in self.lista_nombres_profesores:
                    for aula in self.lista_nombres_aulas:
                        for turno in self.turnos:
                            for dia in self.dias:
                                if asignatura in self.dict_profesores_a_materias[profesor]:
                                    self.modelo.AddBoolAnd([self.vars[profesor, asignatura, aula, grupo, turno, dia],
                                                        # Variables para las restricciones del profesor
                                                        self.restricciones_profesor.variables[dia, turno, profesor, aula]]).OnlyEnforceIf(
                                        # El OnlyEnforceIf asegura que este AND sea verdadero si se cumple en el anterior
                                        self.vars[profesor, asignatura, aula, grupo, turno, dia])

    def _restricciones_hard_aulas(self):
        """
        Restricciones hard para aulas
        """
        # Asegurar que solo se pueda tener una materia en un turno por aula
        for asignatura in self.lista_nombres_materias:
            for grupo in self.lista_nombres_grupos:
                for profesor in self.lista_nombres_profesores:
                    for aula in self.lista_nombres_aulas:
                        for turno in self.turnos:
                            for dia in self.dias:
                                if asignatura in self.dict_profesores_a_materias[profesor]:
                                    self.modelo.AddBoolAnd([self.vars[profesor, asignatura, aula, grupo, turno, dia],
                                                        self._restricciones_aula.variables[
                                                            dia, turno, asignatura, aula]]).OnlyEnforceIf(
                                        # El OnlyEnforceIf asegura que este AND sea verdadero si se cumple en el anterior
                                        self.vars[profesor, asignatura, aula, grupo, turno, dia])

    def resolver_horario(self, mostrar_todas_las_excepciones: bool = True, devolver_dataFrame=True):
        """
        Resuelve el problema del horario
        :return:
        """

        # Crear el solucionador y resolver
        solucionador = cp_model.CpSolver()
        estado = solucionador.Solve(self.modelo)

        if estado == cp_model.INFEASIBLE:
            return f'"No se puede resolver",\n "Código de estado:", {solucionador.status_name()} \n "Número de nodos explorados:", {solucionador.NumBranches(),},"Tiempo de ejecución:", {solucionador.WallTime()}'

        lista_resultado = []
        dict_grupo_resultado: dict[str, Grupo] = {}
        if estado == cp_model.OPTIMAL or estado == cp_model.FEASIBLE:
            for profesor in self.lista_nombres_profesores:
                for asignatura in self.dict_profesores_a_materias[profesor]:
                    for aula in self.lista_nombres_aulas:
                        for grupo in self.lista_nombres_grupos:
                            for turno in self.turnos:
                                for dia in self.dias:
                                    if solucionador.Value(self.vars[profesor, asignatura, aula, grupo, turno, dia]) == 1:
                                        to_print = f'profesor:{profesor},asignatura:{asignatura},aula:{aula},grupo:{grupo},turno:{turno},dia:{dia}'
                                        # print(to_print)
                                        lista_resultado += self._lista_para_dataframe(profesor, asignatura, aula, grupo, turno, dia)
                                        # Añadir al dict de Grupos para devolver en caso de querer un DataFrame
                                        if grupo in dict_grupo_resultado:
                                            dict_grupo_resultado[grupo].agregar(dia, turno, profesor, asignatura, aula)
                                        else:
                                            x = Grupo(grupo)
                                            x.agregar(dia, turno, profesor, asignatura, aula)
                                            dict_grupo_resultado[grupo] = x

                                        if mostrar_todas_las_excepciones:
                                            self.calendario.agregar(grupo, aula, profesor, str(dia), str(turno), asignatura)
                                        else:
                                            try:
                                                self.calendario.agregar(grupo, aula, profesor, str(dia), str(turno), asignatura)
                                            except Exception as e:
                                                raise Exception(f'En {to_print} se lanzó el error: \n {e}')

        # Verificar que se cumpla la cantidad de horas clases por grupo de asignaturas por semana
        self.calendario.finalizar()
        if devolver_dataFrame:
            return to_data_frame(lista_resultado)
        else:
            return dict_grupo_resultado

    def _verificar_restricciones(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                nombres_aulas: list[str], nombres_grupos: list[str]
                                , turnos_int: list[int], dias_int: list[int]):
        """
        Chequea que las restricciones tengan sus valores en la entrada original
        :param nombres_profesores:
        :param nombres_asignaturas:
        :param nombres_aulas:
        :param nombres_grupos:
        :param turnos_int:
        :param dias_int:
        :return:
        """
        self._verificar_existencia_en_lista(nombres_profesores, self.lista_nombres_profesores, "Profesor")
        self._verificar_existencia_en_lista(nombres_asignaturas, self.lista_nombres_materias, "Asignatura")
        self._verificar_existencia_en_lista(nombres_aulas, self.lista_nombres_aulas, "Aula")
        self._verificar_existencia_en_lista(nombres_grupos, self.lista_nombres_grupos, "Grupo")
        self._verificar_existencia_en_lista(turnos_int, self.turnos, "Turno")
        self._verificar_existencia_en_lista(dias_int, self.dias, "Día")

    def _crear_sumatoria_para_restriccion_hard_opcional(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                                        nombres_aulas: list[str], nombres_grupos: list[str]
                                                        , turnos_int: list[int], dias_int: list[int]):
        """Crea la sumatoria de las combinaciones
        de las listas que se le pasan para que después se puedan asignar
        si se debe cumplir la restricción s==1 o no s==0"""
        self._verificar_restricciones(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos, turnos_int, dias_int)
        try:
            s = sum(self.obtener_variable(nombre_profesor, nombre_asignatura, nombre_aula, nombre_grupo, turno_int, dia_int)
                    for nombre_profesor in nombres_profesores for nombre_asignatura in nombres_asignaturas for nombre_aula in nombres_aulas
                    for nombre_grupo in nombres_grupos for turno_int in turnos_int for dia_int in dias_int
                    if nombre_asignatura in self.dict_profesores_a_materias[nombre_profesor])

            return s
        except Exception as e:
            raise Exception(f"Error al crear la sumatoria para las restricciones opcionales: {str(e)}")

    # Chequear los profesores
    def agregar_restricciones_hard_opcionales(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                            nombres_aulas: list[str], nombres_grupos: list[str]
                                            , turnos_int: list[int], dias_int: list[int], contar_igual_a: int):
        """Se da una lista de anterior que tiene añade una condición hard que la
        combinatoria de lo que está en las listas sume contar_igual_a, o sea, se tiene que cumplir.
        OJO: Peligroso de usar, se recomienda usar agregar_restricciones_hard_falsas si se quiere restringir o
        agregar_restricciones_hard_verdaderas si se quiere obligar a que suceda.
        """
        self._verificar_restricciones(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos, turnos_int, dias_int)

        try:
            s = self._crear_sumatoria_para_restriccion_hard_opcional(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos,
                                                                    turnos_int, dias_int)
            if not isinstance(contar_igual_a, int):
                raise Exception(f"No es un número, es un {type(contar_igual_a)}")
            self.modelo.add(s == contar_igual_a)
            if contar_igual_a < 0:
                raise Exception(f'contar_igual_a debe ser >= 0 y es {contar_igual_a}')
        except Exception as e:
            raise Exception(f'Error al agregar restricciones opcionales: {str(e)}')

    def agregar_restricciones_hard_falsas(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                        nombres_aulas: list[str], nombres_grupos: list[str]
                                        , turnos_int: list[int], dias_int: list[int]):
        """Se da una lista de anterior que tiene añade una condición hard que la
        combinatoria de lo que está en las listas sume 0, o sea, se tiene que cumplir."""

        self.agregar_restricciones_hard_opcionales(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos,
                                                turnos_int, dias_int, 0)

    def agregar_restricciones_hard_verdaderas(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                            nombres_aulas: list[str], nombres_grupos: list[str]
                                            , turnos_int: list[int], dias_int: list[int]):
        """Se da una lista de anterior que tiene añade una condición hard que la
        combinatoria de lo que está en las listas sume 1, o sea, se tiene que cumplir."""

        self.agregar_restricciones_hard_opcionales(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos,
                                                turnos_int, dias_int, 1)

    def agregar_restricciones_suaves_maximizar(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                            nombres_aulas: list[str], nombres_grupos: list[str]
                                            , turnos_int: list[int], dias_int: list[int], valor_alpha: int):
        if valor_alpha <= 0:
            raise Exception(f"El valor_alpha debe ser estrictamente positivo y es {valor_alpha}")
        """
        Agrega una condición suave que trata de optimizar para que se cumpla.
        Al maximizar un valor positivo, da prioridad a que se cumpla.
        """

        s = self._crear_sumatoria_para_restriccion_hard_opcional(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos,
                                                                turnos_int, dias_int)

        self.modelo.Maximize(valor_alpha * s)

    def agregar_restricciones_suaves_minimizar(self, nombres_profesores: list[str], nombres_asignaturas: list[str],
                                            nombres_aulas: list[str], nombres_grupos: list[str]
                                            , turnos_int: list[int], dias_int: list[int], valor_alpha: int):
        """
        Agrega una condición suave que trata de optimizar para que se cumpla.
        Al minimizar un valor positivo, da prioridad a que no se cumpla o se cumpla lo menos posible.
        """

        if valor_alpha <= 0:
            raise Exception(f"El valor_alpha debe ser estrictamente positivo y es {valor_alpha}")

        s = self._crear_sumatoria_para_restriccion_hard_opcional(nombres_profesores, nombres_asignaturas, nombres_aulas, nombres_grupos,
                                                                turnos_int, dias_int)

        self.modelo.Minimize(valor_alpha * s)
