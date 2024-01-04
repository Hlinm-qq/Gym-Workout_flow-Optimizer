import pandas as pd
import numpy as np
import json
from algorithm import *

FILENAME = 'data\workout_type.csv'

def getEquipments(filePath):
  df = pd.read_csv(filePath)['equipment'].values
  return df

allUnitList = []

def jsonToCsv(filePath):
  
  # load json
  with open(filePath, 'r') as fl:
    data = json.load(fl)

  # process json data
  for unit in data['equipment']:
    unitName = unit['name']
    unitExer = []
    unitDes = []
    for exercise in unit['exercises']:
      unitExer.append(exercise['exer_name'])
      unitDes.append(exercise['description'])
    
    allUnitList.append([unitName, unitExer, unitDes])
  print(len(allUnitList))

  # json data to csv
  df_data = pd.DataFrame(allUnitList, columns=['unitName', 'Exercise', 'Description'])
  print(df_data.shape)
  df_data.to_csv('data\workout_type.csv', index=False)

# jsonToCsv('data\workout_type.json')
  
##########################################################################
  
def getExerSuggestion(equipments, filePath=FILENAME):
  df_dummy = pd.read_csv(filePath)['unitName'].values.tolist()

  df_exer = pd.read_csv(filePath)
  columns = df_exer.columns

  allEquipExer = []

  for equipment in equipments:
    idx = df_dummy.index(equipment)
    entry = df_exer.iloc[idx]
    topExer = getExer(entry[columns[1]].split(', '), entry[columns[3]].split(', '))
    allEquipExer.append(topExer)
    

  return allEquipExer

def getExer(exerList, exerDiffList, n=3, condition=False):
  topExer = []

  # return any top-n exercises
  for i in range(n):
    if(not condition):
       topExer.append(exerList[i])
  # return top-n exercise based on rules
  else:
    pass

  return topExer

equipmentList = ['Multi Press Machine', 'Olympic Bench']
allEquipExer = getExerSuggestion(equipmentList)
print(allEquipExer)