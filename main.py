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
    data = load_data_from_json('datos.json')

    subjects_name_list = data['subjects']
    dict_subjects_by_time = data['subject_times']
    teachers_names = data['teachers']
    classrooms_names = data['classrooms']
    groups_names = data['groups']
    dict_group_subject_time = data['group_subject_times']
    shifts = data['shifts']
    days = data['days']
    dict_teachers_to_subjects = data['teachers_to_subjects']

    solver = PlanificadorHorario(subjects_name_list, dict_subjects_by_time, teachers_names, classrooms_names, groups_names,
                               dict_group_subject_time, shifts, days, dict_teachers_to_subjects)

    df = solver.resolver_horario()

    to_excel(df)


if __name__ == "__main__":
    main()

