import pandas as pd
import numpy as np
import json
from math import floor, ceil
# from algorithm import Algorithm

FILENAME = 'data\workout_type.csv'
EASY = 4
MEDIUM = 3
HARD = 2

# allUnitList = []

# def jsonToCsv(filePath):
  
#   # load json
#   with open(filePath, 'r') as fl:
#     data = json.load(fl)

#   # process json data
#   for unit in data['equipment']:
#     unitName = unit['name']
#     unitExer = []
#     unitDes = []
#     for exercise in unit['exercises']:
#       unitExer.append(exercise['exer_name'])
#       unitDes.append(exercise['description'])
    
#     allUnitList.append([unitName, unitExer, unitDes])
#   print(len(allUnitList))

#   # json data to csv
#   df_data = pd.DataFrame(allUnitList, columns=['unitName', 'Exercise', 'Description'])
#   print(df_data.shape)
#   df_data.to_csv('data\workout_type.csv', index=False)

# # jsonToCsv('data\workout_type.json')
  
##########################################################################
  
def getExerSuggestion(equipments, filePath=FILENAME):
  # dummy as index
  df_dummy = pd.read_csv(filePath)['unitName'].values.tolist()
  df_dummy = [x.lower() for x in df_dummy]

  # read file
  df_exer = pd.read_csv(filePath)
  columns = df_exer.columns

  allEquipExer = {}
  topOutput = []
  easyOutput = []
  mediumOutput = []
  hardOutput = []

  # iterate over all equipments 
  for equipment in equipments:
    idx = df_dummy.index(equipment)
    entry = df_exer.iloc[idx]

    (topExer, hardExer, mediumExer, easyExer,
     topDes, hardDes, mediumDes, easyDes,
     topPro, hardPro, mediumPro, easyPro) = getExer(entry[columns[1]].split(', '), 
                                            entry[columns[2]].split(', '), 
                                            entry[columns[3]].split(', '), 
                                            entry[columns[4]].split(', '), 
                                            entry[columns[6]].split(', '), 
                                            n=3,
                                            condition=True)
    
    if len(topExer):
      topOutput = suggestExerCount(topExer, topPro)
    if len(easyExer):
      easyOutput = suggestExerCount(easyExer, easyPro, EASY)
    if len(mediumExer):
      mediumOutput = suggestExerCount(mediumExer, mediumPro, MEDIUM)
    if len(hardExer):
      hardOutput = suggestExerCount(hardExer, hardPro, HARD)

    allEquipExer[equipment] = { 'topExer': [topExer, topDes, topOutput],
                                'hardExer': [hardExer, hardDes, hardOutput], 
                                'mediumExer': [mediumExer, mediumDes, mediumOutput], 
                                'easyExer': [easyExer, easyDes, easyOutput]}
    
  return allEquipExer

def getExer(exerList, exerDesc, exerDiffList, 
            exerCount, exerTime, n=3, condition=False):
  topExer = []
  hardExer = []
  mediumExer = []
  easyExer = []

  topDes = []
  hardDes = []
  mediumDes = []
  easyDes = []

  topPro = [[], []]
  hardPro = [[], []]
  mediumPro = [[], []]
  easyPro = [[], []]

  for i in range(n):
    exerDescription = exerDesc[i]
    exerCount_ = exerCount[i]
    exerTime_ = exerTime[i]

  # return any top-n exercises
    if(not condition):
       topExer.append(exerList[i])
       topDes.append(exerDescription)
       topPro[0].append(exerCount_)
       topPro[1].append(exerTime_)

  # return top-n exercise based on rules
    else:
      if int(exerDiffList[i]) < 2:
        easyExer.append(exerList[i])
        easyDes.append(exerDescription)
        easyPro[0].append(exerCount_)
        easyPro[1].append(exerTime_)
      elif int(exerDiffList[i]) < 4:
        mediumExer.append(exerList[i])
        mediumDes.append(exerDescription)
        mediumPro[0].append(exerCount_)
        mediumPro[1].append(exerTime_)
      else:
        hardExer.append(exerList[i])
        hardDes.append(exerDescription)
        hardPro[0].append(exerCount_)
        hardPro[1].append(exerTime_)

  return (topExer, hardExer, mediumExer, easyExer,
          topDes, hardDes, mediumDes, easyDes,
          topPro, hardPro, mediumPro, easyPro)

def suggestExerCount(exers, properties, minute=EASY):
  """
    exers: exercise list
    properties: [[Count], [secondPerCount]]
    minute: exercise length (how long to do the exercise)
  """

  # count how long to do 1 exercise
  exerCount = len(exers)
  minutePerExer = floor(minute / exerCount)

  output = []

  for i in range(exerCount):
    count = floor(minutePerExer*60 / int(properties[1][i]))
    sets = count / int(properties[0][i])
    setStr = f'{int(sets)}' if sets <= floor(sets) else f'{floor(sets)} - {ceil(sets)}'
    isPlural = 'sets' if sets > 1 else 'set'

    output.append(f'=> {int(properties[0][i])} times for {setStr} {isPlural}')

  return output

def getSuggestion(equipmentList):
  allEquipExer = getExerSuggestion(equipmentList)

  for equipment in allEquipExer:
    equipExer = allEquipExer[equipment]

    totalTime = 0
    top = []
    easy = []
    medium = []
    hard = []

    if len(equipExer["topExer"][0]):
      pass
    
    if len(equipExer["easyExer"][0]):
      totalTime += EASY*len(equipExer["easyExer"][0])
      for i in range(len(equipExer["easyExer"][0])):
        easy.append(f'{equipExer["easyExer"][0][i]} {equipExer["easyExer"][2][i]}\n')

    if len(equipExer["mediumExer"][0]):
      totalTime += MEDIUM*len(equipExer["mediumExer"][0])
      for i in range(len(equipExer["mediumExer"][0])):
        medium.append(f'{equipExer["mediumExer"][0][i]} {equipExer["mediumExer"][2][i]}\n')

    if len(equipExer["hardExer"][0]):
      totalTime += HARD*len(equipExer["hardExer"][0])
      for i in range(len(equipExer["hardExer"][0])):
        hard.append(f'{equipExer["hardExer"][0][i]} {equipExer["hardExer"][2][i]}\n')

    combined = easy + medium + hard

    # print(f'{equipment} for <{totalTime} minutes')
    # # print(f'topExer: {", ".join(equipExer["topExer"])}')
    # print(f'easy: {", ".join(easy)}')
    # print(f'medium: {", ".join(medium)}')
    # print(f'hard: {", ".join(hard)}')
    # print()

    return combined, totalTime

# equipmentList = ['Leg Press and Hack Squat Machine'.lower()]
# combined, totalTime = getSuggestion(equipmentList)
# print(combined, totalTime)