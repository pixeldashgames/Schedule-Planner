import pandas as pd
from pandas import DataFrame


def to_data_frame(data):
  # Crear un DataFrame a partir de la lista
  df = pd.DataFrame(data)
  return df
  # Mostrar el DataFrame
  # print(df)


def to_excel(df: DataFrame):
  # Asumiendo que 'Profesor', 'Asignatura' y 'Aula' son otras columnas en tu DataFrame que quieres incluir
  df['Info'] = 'Profesor:' + df['Profesor'] + "\n" "Asignatura:" + df['Asignatura'] + "\n" + "Aula:" + df['Aula']
  # df['Teacher'] + ', ' + df['Subject'] + ', ' + df['Classroom']

  with pd.ExcelWriter('./output.xlsx') as writer:
    for group in df['Grupo'].unique():
      # Filtrar el DataFrame por grupo
      df_group = df[df['Grupo'] == group]

      # Reorganizar el DataFrame para que los días sean las columnas y los turnos las filas
      # Ahora, cada celda contendrá la información de 'Info'
      df_pivot = df_group.pivot(index='Turno', columns='Día', values='Info')

      # Escribir el DataFrame reorganizado en una hoja de Excel
      df_pivot.to_excel(writer, sheet_name=group)









