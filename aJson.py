class Base:
    def __init__(self, nombre: str | int):
        self.nombre = nombre

class Curso:
    def __init__(self, nombre: int):
        self.nombre = nombre

class Asignatura(Base):
    def __init__(self, nombre: str):
        super().__init__(nombre)

class Profesor(Base):
    def __init__(self, nombre: str):
        super().__init__(nombre)

class Turno:
    def __init__(self, dia: int, turno: int, profesor: str, asignatura: str, aula: str):
        self.dia = dia
        self.turno = turno
        self.profesor = profesor
        self.asignatura = asignatura
        self.aula = aula

    def to_dict(self):
        return {
            'dia': self.dia,
            'turno': self.turno,
            'profesor': self.profesor,
            'asignatura': self.asignatura,
            'aula': self.aula
        }

class Grupo(Base):
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.calendario: dict[tuple[int, int], Turno] = {}

    def agregar(self, dia: int, turno: int, profesor: str, asignatura: str, aula: str):
        tupla = (dia, turno)
        if tupla in self.calendario:
            raise Exception(f"El turno {turno} el día {dia} ya estaba asignado")
        self.calendario[tupla] = Turno(dia, turno, profesor, asignatura, aula)

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'calendario': {str(k): v.to_dict() for k, v in self.calendario.items()}
        }

def grupos_a_json(grupos: dict[str, Grupo]):
    # Obtener solo los valores del diccionario
    valores_grupo: list[Grupo] = grupos.values()
    grupos_dict = [grupo.to_dict() for grupo in valores_grupo]
    return grupos_dict
