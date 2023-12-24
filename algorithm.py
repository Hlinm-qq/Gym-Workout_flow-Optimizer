import random
import pandas as pd
import numpy as np
import queue
import json
from heuristic_1 import  heuristic
from itertools import combinations

random.seed(1126)


class Algorithm:
    def __init__(self, userInput):
        df = pd.read_csv("data/equipment.csv")    
        self.getEquipmentStatus(df, defaultSet=True)

        self.equipmentStatus = df        
        self.target = userInput[0]
        self.willWait = userInput[1]
        self.tolerance = userInput[2]
        self.state = [] # initial state

        with open('data/muscle_dict_comple.json', 'r') as file:
            self.jsonData = json.load(file)

    def method(self):

        totalCapacity = list(self.equipmentStatus.number * self.equipmentStatus.capacity)
        possessCapacity = list(totalCapacity - self.equipmentStatus.status)
        cost = [min(times) if totalCapacity[i] == possessCapacity[i] else 0 for i, times in enumerate(self.equipmentStatus.usage_time)]

        fringe = queue.PriorityQueue()
        visited = []

        while(True):
            if not fringe.empty():
                f, self.state = fringe.get()

            if self.isGoal():
                break 

            neighbors = self.getNeigbors()
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.append(neighbor)
                    pathCost = sum(cost[list(self.equipmentStatus.equipment).index(equip)] for equip in neighbor)
                    fringe.put((pathCost, neighbor))
                
        print(f"Goal: {self.state, f}")
        
    def isGoal(self):
        indices = [list(self.equipmentStatus.equipment).index(equip) for equip in self.state]

        for muscle in self.target:
            find = False
            for i in indices:
                if muscle in self.jsonData[str(i)]:
                    find = True                 
            if not find:
                return False
            
        return True

    def getNeigbors(self):
        length = len(self.state) 
        
        if length == 0:
            return [[equip] for equip in self.equipmentStatus.equipment]
        else:
            return [sorted(self.state[:length - 1] + [equip]) for equip in self.equipmentStatus.equipment if equip not in self.state] \
                    +[sorted(self.state + [equip]) for equip in self.equipmentStatus.equipment if equip not in self.state] 

            
    def getTargetMuscleGroup(muscleGroup, defaultSet=True):
        """The specific muscle group the user intends to train.

        Args:
            muscleGroup (list): pre-defined muscle groups list
        """
        # default target muscle groups
        if defaultSet:
            target = [
                "Pectoralis Major (Clavicular Head)",
                "Anterior Deltoids (Front shoulder)",
                "Triceps Brachii (Back of upper arm)",
                "Serratus Anterior (Upper side of ribs)",
                #"Chest",
                #"Shoulder",
                #"Arm",
            ]
            willWait = True
            tolerance = 30
        else:
            pass
        return (target, willWait, tolerance)

    def getEquipmentStatus(self, EquipmentDSet, defaultSet=True):
        """Add two columns to EquipmentDSet
        (1) Real-time status of each piece of gym equipment (the number of available equipments)
        (2) The expected time each equipment will be in use.

        Args:
            EquipmentDSet (df): read from equipment[_].csv
        """
        dset = EquipmentDSet.copy()
        dset = dset.set_index("equipment")
        status = dict()
        usageTime = dict()
        count = 0

        if defaultSet:
            for name in dset.index:
                # get equipment status
                totalCapacity = dset.loc[name]["number"] * dset.loc[name]["capacity"]
                numAvailable = random.randint(0, totalCapacity)
                status[count] = numAvailable
                # get expected time
                if numAvailable == totalCapacity:
                    usageTime[count] = [0]
                elif numAvailable != 0:
                    usageTime[count] = random.sample(
                        range(5, 30), totalCapacity - numAvailable
                    )
                else:
                    usageTime[count] = random.sample(range(5, 30), totalCapacity)
                count += 1
        else:
            pass
        # update equipment information
        EquipmentDSet["status"] = status
        EquipmentDSet["usage_time"] = usageTime
        return None

if __name__ == '__main__':

    userInput = Algorithm.getTargetMuscleGroup(muscleGroup=None, defaultSet=True)

    tomy = Algorithm(userInput)
    tomy.method()


    