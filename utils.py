import copy

class Profesor:
    def __init__(self, nombre: str):
        self.nombre = nombre


class ProfesorDesconocido(Profesor):
    def __init__(self):
        super().__init__('Desconocido')


class Asignatura:
    def __init__(self, nombre: str, grupos_posibles, profesores_posibles):

        self.nombre = nombre
        self.grupos_posibles: list[str] = copy.deepcopy(grupos_posibles)
        self.profesores: dict[str, Profesor] = copy.deepcopy(profesores_posibles)
        self.grupos_actuales: set[str] = set()
        self.desconocido: Profesor = ProfesorDesconocido()
        self.lista_profesores: list[Profesor] = [self.desconocido]
        self._nombre_profesor = None

    @property
    def nombre_profesor(self):
        return [x.nombre for x in self.lista_profesores]

    def agregar_grupo(self, nombre_asignatura: str, nombre_grupo: str, nombre_profesor: str):
        if not self.nombre == nombre_asignatura:
            raise Exception(f"La asignatura {self.nombre} no es {nombre_asignatura}")

        # Si el profesor es desconocido, cambiarlo por el actual
        if isinstance(self.lista_profesores[0], ProfesorDesconocido):
            if not nombre_profesor in self.profesores:
                raise Exception(f"El profesor {nombre_profesor} no está declarado para dar la asignatura {self.nombre}")
            self.lista_profesores = [self.profesores[nombre_profesor]]

        if not nombre_grupo in self.grupos_posibles:
            raise Exception(f"El grupo {nombre_grupo} no está entre los posibles grupos {self.grupos_posibles}")
        self.grupos_actuales.add(nombre_grupo)

class AsignaturaDesconocida(Asignatura):
    def __init__(self):
        super().__init__('Desconocida', [], {})


class Aula:
    def __init__(self, nombre: str, dict_asignaturas):
        """
        Inicializa el objeto con el nombre proporcionado y el diccionario de asignaturas.

        Parámetros:
            nombre (str): El nombre del aula.
            dict_asignaturas (dict[str, Asignatura]): Un diccionario que contiene asignaturas.

        Retorna:
            None
        """
        self.nombre = nombre
        self.desconocida = AsignaturaDesconocida()
        self.asignaturas_posibles: dict[str, Asignatura] = copy.deepcopy(dict_asignaturas)
        self.asignatura: Asignatura = self.desconocida
        self._nombre_asignatura = None
        self.grupos: set[str] = set()

    @property
    def nombre_asignatura(self):
        return self.asignatura.nombre

    @property
    def cantidad_grupos(self):
        return len(self.grupos)

    def agregar_asignatura_en_grupo_y_carrera(self, nombre_asignatura: str, nombre_grupo: str, nombre_profesor: str):
        # Comprobar si la asignatura es válida para asignar
        if not (isinstance(self.asignatura, AsignaturaDesconocida) or self.nombre_asignatura == nombre_asignatura):
            raise Exception(f"En el aula {self.nombre} se da la asignatura {self.nombre_asignatura} y se quiere dar {nombre_asignatura}")
        # Comprobar si es desconocida, luego verificar que en dicha aula se pueda dar esa asignatura
        if isinstance(self.asignatura, AsignaturaDesconocida):
            if not nombre_asignatura in self.asignaturas_posibles:
                raise Exception(f"La asignatura {nombre_asignatura} no es posible darla en el aula {self.nombre}")
            # Se asigna la asignatura a dar
            self.asignatura: Asignatura = self.asignaturas_posibles[nombre_asignatura]

        # Añadir el grupo al conjunto de grupos
        self.grupos.add(nombre_grupo)

        # Añadir el grupo a la asignatura
        self.asignatura.agregar_grupo(nombre_asignatura, nombre_grupo, nombre_profesor)

class Turnos:
    def __init__(self, nombre: str, dia: str, nombres_aulas, dict_asignaturas):
        self.nombre: str = nombre
        self.dia: str = dia
        self.nombres_aulas: list[str] = copy.deepcopy(nombres_aulas)
        self.aulas: dict[str:Aula] = {}
        # Instancia las aulas posibles para ese turno
        for item in self.nombres_aulas:
            self.aulas[item] = Aula(item, copy.deepcopy(dict_asignaturas))

        self.profesor_aula: dict[str, str] = {}
        """Diccionario para asignar a cada profesor una única aula"""
        self.profesor_por_asignatura: dict[str, str] = {}
        """Diccionario que asigna a cada nombre de profesor una asignatura a enseñar.
        Esto es para comprobar que un profesor en un turno no imparta más de 1 clase a la vez"""

    def agregar_asignatura_con_aula(self, nombre_turno: str, nombre_aula: str, nombre_asignatura: str,
                                 nombre_grupo: str, nombre_profesor: str):
        # Si no es el mismo turno, lanza una excepción
        if not self.nombre == str(nombre_turno):
            raise Exception(f'Este es el turno {self.nombre} y se quiere añadir en el turno {nombre_turno}')
        # Si esa aula no está asignada a este turno, lanza una excepción
        if not nombre_aula in self.aulas:
            raise Exception(f'El aula {nombre_aula} no está en este turno')

        # Comprueba que el profesor no esté asignado a ninguna asignatura o imparta la misma asignatura a asignar
        if nombre_profesor in self.profesor_por_asignatura and self.profesor_por_asignatura[nombre_profesor] != nombre_asignatura:
            raise Exception(
                f"El profesor {nombre_profesor} imparte la asignatura: {self.profesor_por_asignatura[nombre_profesor]} no la asignatura: {nombre_asignatura}")

        # Si no está en el diccionario, añádelo
        if nombre_profesor not in self.profesor_por_asignatura:
            self.profesor_por_asignatura[nombre_profesor] = nombre_asignatura

         # Añadir en las aulas
        self.aulas[nombre_aula].agregar_asignatura_en_grupo_y_carrera(nombre_asignatura, nombre_grupo, nombre_profesor)

class Grupo:
    def __init__(self, nombre: str, materias_por_tiempo):
        self.nombre = nombre
        self.materias_por_tiempo: dict[str, int] = copy.deepcopy(materias_por_tiempo)
        self.contador_materias_actual_por_tiempo: dict[str, int] = {}
        # Inicializa lo que tengo de tiempo real hasta ahora en 0
        for nombre_materia in self.materias_por_tiempo.keys():
            self.contador_materias_actual_por_tiempo[nombre_materia] = 0

    def agregar_materia_turno(self, nombre_materia: str):
        if nombre_materia not in self.contador_materias_actual_por_tiempo:
            raise Exception(f"La materia {nombre_materia} no está definida para el grupo {self.nombre}")
        self.contador_materias_actual_por_tiempo[nombre_materia] += 1

    def verificar_todo_correcto(self):
        for nombre_materia in self.materias_por_tiempo.keys():
            tiempo_prometido = self.materias_por_tiempo[nombre_materia]
            tiempo_real = self.contador_materias_actual_por_tiempo[nombre_materia]
            if tiempo_prometido != tiempo_real:
                raise Exception(
                    f"En el grupo {self.nombre}, la materia {nombre_materia} debería tener {tiempo_prometido} horas de clase a la semana y tiene {tiempo_real}")

class CalendarioBase:
    def __init__(self, nombres_materias, nombres_profesores,
                 posibles_profesores_por_materia,
                 grupos_por_asignatura_por_tiempo_semanal,
                 cantidad_dias=5, cantidad_turnos=3,
                 nombres_aulas = ["1", "2", "postgrado"], nombres_grupos = ["C111", "C112"]):
       
        self.cantidad_dias = cantidad_dias
        self.cantidad_turnos = cantidad_turnos
        self.nombres_materias: list[str] = nombres_materias
        self.nombres_profesores: list[str] = nombres_profesores
        self.posibles_profesores_por_materia: dict[str, list[str]] = posibles_profesores_por_materia
        self.nombres_aulas = nombres_aulas
        self.nombres_grupos = nombres_grupos
        self.grupos_por_asignatura_por_tiempo_semanal = grupos_por_asignatura_por_tiempo_semanal

class Calendario(CalendarioBase):
    def __add_to_dict_grupos_posibles_por_asignatura(self, nombre_grupo: str, lista_asignaturas):
        """
        Añade al diccionario que tiene como clave el nombre de la asignatura los posibles grupos que pueden recibir esta.
        :param nombre_grupo:
        :param lista_asignaturas:
        :return:
        """
        for nombre_asignatura in lista_asignaturas:
            if nombre_asignatura not in self.nombres_materias:
                raise Exception(f"La asignatura {nombre_asignatura} no está en {self.nombres_materias}")
            # Comprueba si la asignatura ya está guardada
            if nombre_asignatura not in self.asignatura_a_grupos_posibles:
                mi_conjunto = set()
                mi_conjunto.add(nombre_grupo)
                self.asignatura_a_grupos_posibles[nombre_asignatura] = mi_conjunto
            else:
                self.asignatura_a_grupos_posibles[nombre_asignatura].add(nombre_grupo)

    def __iniciar_profesores(self):
        for nombre_profesor in self.nombres_profesores:
            self.diccionario_profesores[nombre_profesor] = Profesor(nombre_profesor)

    def __iniciar_grupos(self):
        for nombre_grupo in self.nombres_grupos:
            if nombre_grupo not in self.grupos_por_asignatura_por_tiempo_semanal:
                raise Exception(f"El grupo {nombre_grupo} no tiene clases asignadas")
            # El diccionario que tiene como clave el nombre de la asignatura y como valor el tiempo que debe impartirse
            # está en una semana
            diccionario: dict[str, int] = self.grupos_por_asignatura_por_tiempo_semanal[nombre_grupo]
            grupo = Grupo(nombre_grupo, copy.deepcopy(diccionario))
            self.diccionario_grupos[nombre_grupo] = grupo
            # Ahora añadir en la asignatura que este es un grupo posible
            lista_nombres_asignaturas = list(diccionario.keys())
            self.__add_to_dict_grupos_posibles_por_asignatura(nombre_grupo, lista_nombres_asignaturas)

    def __obtener_profesores_posibles_por_asignatura(self, nombre_asignatura: str) :
        """
        Dado un nombre de materia, devuelve un diccionario que tiene el nombre del profesor y el profesor.

        :param nombre_asignatura:
        :return dict[str, Profesor]:
        """
        resultado: dict[str, Profesor] = {}
        if nombre_asignatura not in self.posibles_profesores_por_materia:
            raise Exception(f"La asignatura: {nombre_asignatura} no tiene asignados profesores")
        lista_profesores_posibles = self.posibles_profesores_por_materia[nombre_asignatura]
        for nombre_profesor in lista_profesores_posibles:
            if nombre_profesor not in self.diccionario_profesores:
                raise Exception(f"El profesor {nombre_profesor} no existe")
            profesor = self.diccionario_profesores[nombre_profesor]
            resultado[nombre_profesor] = profesor
        if len(resultado) < 1:
            raise Exception(f"Se debe asignar al menos un profesor a la asignatura {nombre_asignatura}")
        return resultado

    def __iniciar_asignaturas(self):
        for nombre_asignatura in self.nombres_materias:
            # Seleccionar los profesores para la materia
            diccionario_profesores = self.__obtener_profesores_posibles_por_asignatura(nombre_asignatura)
            temp = Asignatura(nombre_asignatura, list(copy.deepcopy(self.asignatura_a_grupos_posibles[nombre_asignatura])),
                              copy.deepcopy(diccionario_profesores))
            self.diccionario_asignaturas[nombre_asignatura] = temp

    def __iniciar_turnos(self):
        for i in range(1, self.cantidad_dias + 1):
            for j in range(1, self.cantidad_turnos + 1):
                self.turnos[i, j] = Turnos(str(j), str(i), self.nombres_aulas, copy.deepcopy(self.diccionario_asignaturas))
                # día, turno

    def __iniciar(self):
        self.__iniciar_grupos()
        self.__iniciar_profesores()
        self.__iniciar_asignaturas()
        self.__iniciar_turnos()

    def __init__(self, nombres_materias, nombres_profesores,
                 posibles_profesores_por_materia,
                 grupos_por_asignatura_por_tiempo_semanal,
                 cantidad_dias=5, cantidad_turnos=3,
                 nombres_aulas = ["1", "2", "postgrado"], nombres_grupos = ["C111", "C112"]):
        super().__init__(nombres_materias, nombres_profesores, posibles_profesores_por_materia,
                         grupos_por_asignatura_por_tiempo_semanal, cantidad_dias, cantidad_turnos,
                         nombres_aulas, nombres_grupos)

        self.desconocido = 'Desconocido'
        self.diccionario_asignaturas: dict[str, Asignatura] = {}
        self.turnos: dict[tuple[int, int], Turnos] = {}
        self.diccionario_grupos: dict[str, Grupo] = {}
        self.asignatura_a_grupos_posibles: dict[str, set[str]] = {}
        self.diccionario_profesores: dict[str, Profesor] = {}

        # Llamar al método __iniciar para inicializar los diccionarios
        self.__iniciar()

    def __agregar_asignatura_a_grupo(self, nombre_asignatura: str, nombre_grupo: str):
        if nombre_grupo not in self.diccionario_grupos:
            raise Exception(f"El grupo {nombre_grupo} no está definido")
        if nombre_asignatura not in self.diccionario_asignaturas:
            raise Exception(f"La asignatura {nombre_asignatura} no está definida")
        
         # Añadir la asignatura al grupo
        grupo = self.diccionario_grupos[nombre_grupo]
        # Se dice que se dio un turno de esta asignatura
        grupo.agregar_materia_turno(nombre_asignatura)

    def agregar(self, nombre_grupo: str, nombre_aula: str, nombre_profesor: str, nombre_dia: str, nombre_turno: str,
            nombre_asignatura: str):

        nombre_dia = int(nombre_dia)
        nombre_turno = int(nombre_turno)
        clave = (nombre_dia, nombre_turno)
        if not clave in self.turnos:
            raise Exception("El día o turno no es válido")

        turno = self.turnos[clave]

        turno.agregar_asignatura_con_aula(str(nombre_turno), nombre_aula, nombre_asignatura, nombre_grupo, nombre_profesor)

        # Añadir al grupo que se dio un turno de la asignatura
        self.__agregar_asignatura_a_grupo(nombre_asignatura, nombre_grupo)

    def finalizar(self):
        """
        Realiza las comprobaciones finales.
        :return:
        """
        nombres_grupos = self.diccionario_grupos.keys()
        for nombre_grupo in nombres_grupos:
            grupo = self.diccionario_grupos[nombre_grupo]
            # Comprueba que cada grupo recibió la cantidad de clases acordadas
            grupo.verificar_todo_correcto()

class Restricciones_Adicionales_Fuertes(CalendarioBase):
    def __init__(self, nombres_materias, nombres_profesores,
                 posibles_profesores_por_materia,
                 grupos_por_asignatura_por_tiempo_semanal,
                 cantidad_dias=5, cantidad_turnos=3,
                 nombres_aulas = ["1", "2", "postgrado"], nombres_grupos = ["C111", "C112"]):
        
        super().__init__(nombres_materias, nombres_profesores, posibles_profesores_por_materia,
                         grupos_por_asignatura_por_tiempo_semanal, cantidad_dias, cantidad_turnos,
                         nombres_aulas, nombres_grupos)
