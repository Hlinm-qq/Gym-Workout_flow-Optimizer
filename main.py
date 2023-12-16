from algorithm import *

import pandas as pd


df = pd.read_csv("equipment.csv")
print(df.head())

equipList = df['equipment']
equipNumList = df['number']

# catch/hardcode muscle part each equipment is for
# e.g. 
#     {
#         treadmill: leg, ...
#         rowing machine: ...
#     }

userIn = input("what do you want to train on ?")

def processUserInput(userIn):
    """
        return equipment list that applies with user need
    """
    pass

def getSuggestion():
    """
        return the suggestion of algorithm
    """
    equipmentList = processUserInput(userIn)

