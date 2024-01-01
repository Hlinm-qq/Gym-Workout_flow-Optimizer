import pandas as pd
import numpy as np
import queue
import json
from heuristic_1 import heuristic
from itertools import combinations
import input

infinity = 9999999

class Algorithm:
    def __init__(self, userInput):
        df = pd.read_csv("data/equipment.csv")
        self.getEquipmentStatus(df)

        self.equipmentStatus = df
        self.target = userInput[0]
        self.musleGroup = userInput[0]
        self.tolerance = userInput[1]
        self.state = []  # initial state

        with open("data/muscle_dict_comple.json", "r") as file:
            self.jsonData = json.load(file)

    def method(self):
        '''
            state space - all possible equipment combinations
            cost - wait time or infinity if the equipment doesn't train the target muscle 
            heuristic - the more trained muscle in target, the less heuristic
        '''
        cost = []
        for i in self.equipmentStatus.id:
            wait = self.equipmentStatus["expected usage time for occupied equipments"][i]

            # cost[equipment] = wait time or inf if the equipment doesn't train the target muscle  
            if not self.targetEquip(i):
                cost.append(infinity)
            elif self.equipmentStatus["availabel number"][i] == 0:
                for usage in self.equipmentStatus["expected usage time for waiting people"][i]:
                    min_index = wait.index(min(wait))
                    wait[min_index] += usage
                cost.append(min(wait))
            else:
                cost.append(0)
            
        fringe = queue.PriorityQueue()
        visited = []

        while True:
            if not fringe.empty():
                _, self.state = fringe.get()

            if self.isGoal():
                break

            neighbors = self.getNeigbors()

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.append(neighbor)
                    pathCost = sum(
                        cost[list(self.equipmentStatus.equipment).index(equip)]
                        for equip in neighbor
                    )
                    
                    pathCost += self.heuristic(neighbor)
                    fringe.put((pathCost, neighbor))

        indices = [
            list(self.equipmentStatus.equipment).index(equip) for equip in self.state
        ]

        for i in indices:
            print(self.equipmentStatus.equipment[i], end='')
            print(f' - wait for {cost[i]} minutes...')

    def heuristic(self, neighbor):
        indices = [
            list(self.equipmentStatus.equipment).index(equip) for equip in neighbor
        ]

        base = len(self.target)
        
        for muscle in self.target:
            find = False
            for i in indices:
                if muscle in self.jsonData[str(i)]:
                    find = True
            
            if find == True:
                base -= 1
        return base
    
    def targetEquip(self, equip):
        '''
            see whether the equipment trained target muscle
        '''
        for muscle in self.target:
            find = False
            if muscle in self.jsonData[str(equip)]:
                find = True
        
        return find

    def isGoal(self):
        '''
            see whether the current equipments satisfied target muscle group
        '''
        indices = [
            list(self.equipmentStatus.equipment).index(equip) for equip in self.state
        ]

        for muscle in self.target:
            find = False
            for i in indices:
                if muscle in self.jsonData[str(i)]:
                    find = True
            if not find:
                return False

        return True
    

    def alreadyTrained(self, l, equip):
        '''
            see if muscle trained by equip if already trained in l
            *only consider muscle in self.target
        '''
        equipIndex = list(self.equipmentStatus.equipment).index(equip)
        indices = [
            list(self.equipmentStatus.equipment).index(equip) for equip in l
        ]

        for muscle in self.target:
            already = False
            
            for i in indices:
                if muscle in self.jsonData[str(i)]:
                    already = True

            if not already and muscle in self.jsonData[str(equipIndex)]:
                return False 
        
        return True

    def getNeigbors(self):
        length = len(self.state)

        if length == 0:
            return [[equip] for equip in self.equipmentStatus.equipment]
        else:
            neighbors = []
            for equip in self.equipmentStatus.equipment:
                tmp = self.state[: length - 1] 

                if not self.alreadyTrained(tmp, equip):
                    neighbors.append(sorted(tmp + [equip]))

                tmp = self.state[: length] 

                if not self.alreadyTrained(tmp, equip):
                    neighbors.append(sorted(tmp + [equip]))
            
            return neighbors
            

    def getTargetMuscleGroup(muscleGroup, defaultSet=True):
        """The specific muscle group the user intends to train.

        Args:
            muscleGroup (list): pre-defined muscle groups list
        """
        # default target muscle groups and waiting time
        if defaultSet:
            target = [
                "Pectoralis Major (Clavicular Head)",
                "Anterior Deltoids (Front shoulder)",
                "Triceps Brachii (Back of upper arm)",
                "Serratus Anterior (Upper side of ribs)",
                "Back",
                # "Shoulder",
                # "Arm",
            ]
            tolerance = 30
        else:
            # get target muscle groups and waiting time from web
            #target, tolerance = get_user_input()
            pass
        return (target, tolerance)

    def getEquipmentStatus(self, df):
        numAvailable, useTime = input.getUsageList(df)
        numWait, waitTime = input.getWaitingList(numAvailable, df)
        df["availabel number"] = numAvailable
        df["expected usage time for occupied equipments"] = useTime
        df["waiting number"] = numWait
        df["expected usage time for waiting people"] = waitTime

    def showdf(self):
        print(self.equipmentStatus["expected usage time for occupied equipments"])
        print(self.equipmentStatus["expected usage time for waiting people"])

if __name__ == "__main__":
    userInput = Algorithm.getTargetMuscleGroup(muscleGroup=None)

    obj = Algorithm(userInput)
    # obj.showdf()
    
    obj.method()
