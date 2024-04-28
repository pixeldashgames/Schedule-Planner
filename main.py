from enum import Enum
from printer import to_excel
from solucion import PlanificadorHorario

class Asignaturas(Enum):
    Programacion = "Programación"
    ProgramacionCp = "ProgramaciónCp"
    Algebra = "Álgebra"
    AlgebraCP = "ÁlgebraCP"
    Analisis = "Análisis"
    AnalisisCp = "AnálisisCp"
    Logica = "Lógica"
    LogicaCp = "LógicaCp"

    def __str__(self):
        return self.value

class Profesores(Enum):
    Piad = "Piad"
    Idania = "Idania"
    Celia = "Celia"
    Yudivian = "Yudivian"
    DanielL = "DanielL"
    OmarL = "OmarLógica"
    CarmenL = "CarmenL"
    ErnestoA = "ErnestoAnálisis"
    CristinaA = "CristinaA"
    MercedesA = "MercedesA"
    DalianisAL = "DalianisÁlgebra"
    PepeAl = "PepeÁlgebra"
    CayetanaAL = "CayetanaÁlgebra"
    PacoP = "PacoProgramación"
    HectorP = "HéctorProgramación"
    CarlaP = "CarlaProgramación"

    def __str__(self):
        return self.value
    
def main():
    subjects_name_list = [Asignaturas.Programacion,
                          Asignaturas.ProgramacionCp,
                          Asignaturas.Algebra,
                          Asignaturas.AlgebraCP,
                          Asignaturas.Analisis,
                          Asignaturas.AnalisisCp,
                          Asignaturas.Logica,
                          Asignaturas.LogicaCp]
    subjects_name_list = [str(x) for x in subjects_name_list]

    dict_subjects_by_time = {Asignaturas.Programacion: 1,
                             Asignaturas.ProgramacionCp: 2,
                             Asignaturas.Algebra: 1,
                             Asignaturas.AlgebraCP: 2,
                             Asignaturas.Analisis: 1,
                             Asignaturas.AnalisisCp: 2,
                             Asignaturas.Logica: 1,
                             Asignaturas.LogicaCp: 1}

    dict_subjects_by_time = {str(x): dict_subjects_by_time[x] for x in dict_subjects_by_time.keys()}

    teachers_names = [
        Profesores.Piad,
        Profesores.Idania,
        Profesores.Celia,
        Profesores.Yudivian,
        Profesores.DanielL,
        Profesores.OmarL,
        Profesores.CarmenL,
        Profesores.ErnestoA,
        Profesores.CristinaA,
        Profesores.MercedesA,
        Profesores.DalianisAL,
        Profesores.PepeAl,
        Profesores.CayetanaAL,
        Profesores.PacoP,
        Profesores.HectorP,
        Profesores.CarlaP,
    ]
    teachers_names = [str(x) for x in teachers_names]

    classrooms_names = [f'{x}' for x in range(1, 6)] + ["Postgrado"]

    groups_names = [f"C11{x}" for x in range(1, 7)]

    dict_group_subject_time = {}

    for item in groups_names:
        dict_group_subject_time[item] = dict_subjects_by_time

    shifts = [1, 2, 3]
    days = [x for x in range(1, 6)]

    dict_teachers_to_subjects = {
        Profesores.Piad: [Asignaturas.Programacion],
        Profesores.Idania: [Asignaturas.Analisis],
        Profesores.Celia: [Asignaturas.Algebra],
        Profesores.Yudivian: [Asignaturas.Logica],
        Profesores.DanielL: [Asignaturas.LogicaCp],
        Profesores.OmarL: [Asignaturas.LogicaCp],
        Profesores.CarmenL: [Asignaturas.LogicaCp],
        Profesores.ErnestoA: [Asignaturas.AnalisisCp],
        Profesores.CristinaA: [Asignaturas.AnalisisCp],
        Profesores.MercedesA: [Asignaturas.AnalisisCp],
        Profesores.DalianisAL: [Asignaturas.AlgebraCP],
        Profesores.PepeAl: [Asignaturas.AlgebraCP],
        Profesores.CayetanaAL: [Asignaturas.AlgebraCP],
        Profesores.PacoP: [Asignaturas.ProgramacionCp],
        Profesores.HectorP: [Asignaturas.ProgramacionCp],
        Profesores.CarlaP: [Asignaturas.ProgramacionCp],
    }

    dict_teachers_to_subjects = {str(x): [str(y) for y in dict_teachers_to_subjects[x]] for x in dict_teachers_to_subjects.keys()}
    nue = "nueva"
    profe_new = "profeNuevo"
    grupo_nuevo = "GrupoNuevo"
    count = 1
    subjects_name_list.append(nue)
    dict_subjects_by_time[nue] = count
    teachers_names.append(profe_new)
    groups_names.append(grupo_nuevo)
    ddd = {}
    ddd[nue] = count

    dict_group_subject_time[grupo_nuevo] = ddd
    dict_teachers_to_subjects[profe_new] = [nue]

    solver = PlanificadorHorario(subjects_name_list, dict_subjects_by_time, teachers_names, classrooms_names, groups_names,
                               dict_group_subject_time, shifts, days, dict_teachers_to_subjects)

    df = solver.resolver_horario()

    to_excel(df)


if __name__ == "__main__":
    main()

