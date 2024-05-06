from enum import Enum
from printer import to_excel
from solucion import PlanificadorHorario
import json

def load_data_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def main():
    
    # Cargar datos desde el archivo JSON
    data = load_data_from_json('src\datos.json')

    subjects_name_list = data['subjects']
    dict_subjects_by_time = data['subject_times']
    teachers_names = data['teachers']
    classrooms_names = data['classrooms']
    groups_names = data['groups']
    dict_group_subject_time = data['group_subject_times']
    shifts = data['shifts']
    days = data['days']
    dict_teachers_to_subjects = data['teachers_to_subjects']

    hards_true = data['hards_true']
    hards_false = data['hards_false']
    softs_max = data['softs_max']
    softs_min = data['softs_min']

    solver = PlanificadorHorario(subjects_name_list, dict_subjects_by_time, teachers_names, classrooms_names, groups_names,
                               dict_group_subject_time, shifts, days, dict_teachers_to_subjects)

    for restriction in hards_true: solver.agregar_restricciones_hard_verdaderas(hards_true[restriction]["teachers_names"], hards_true[restriction]["subjects_names"], hards_true[restriction]["classrooms_names"], hards_true[restriction]["groups_names"], hards_true[restriction]["shifts"], hards_true[restriction]["days"])
    for restriction in hards_false: solver.agregar_restricciones_hard_falsas(hards_false[restriction]["teachers_names"], hards_false[restriction]["subjects_names"], hards_false[restriction]["classrooms_names"], hards_false[restriction]["groups_names"], hards_false[restriction]["shifts"], hards_false[restriction]["days"])
    for restriction in softs_max: solver.agregar_restricciones_suaves_maximizar(softs_max[restriction]["teachers_names"], softs_max[restriction]["subjects_names"], softs_max[restriction]["classrooms_names"], softs_max[restriction]["groups_names"], softs_max[restriction]["shifts"], softs_max[restriction]["days"], softs_max[restriction]["alpha"])
    for restriction in softs_min: solver.agregar_restricciones_suaves_minimizar(softs_min[restriction]["teachers_names"], softs_min[restriction]["subjects_names"], softs_min[restriction]["classrooms_names"], softs_min[restriction]["groups_names"], softs_min[restriction]["shifts"], softs_min[restriction]["days"], softs_min[restriction]["alpha"])

    df = solver.resolver_horario()

    to_excel(df)


if __name__ == "__main__":
    main()

