import pandas as pd
import numpy as np
import queue
import json
from heuristic_1 import heuristic
from itertools import combinations
from output import get_user_input
import input


class Algorithm:
    def __init__(self, userInput):
        df = pd.read_csv("data/equipment.csv")
        self.getEquipmentStatus(df)

        self.equipmentStatus = df
        self.target = userInput[0]
        self.tolerance = userInput[1]
        self.state = []  # initial state

        with open("data/muscle_dict_comple.json", "r") as file:
            self.jsonData = json.load(file)

    def method(self):
        totalCapacity = list(
            self.equipmentStatus.number * self.equipmentStatus.capacity
        )
        possessCapacity = list(totalCapacity - self.equipmentStatus.status)
        cost = [
            min(times) if totalCapacity[i] == possessCapacity[i] else 0
            for i, times in enumerate(self.equipmentStatus.usage_time)
        ]

        fringe = queue.PriorityQueue()
        visited = []

        while True:
            if not fringe.empty():
                f, self.state = fringe.get()

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
                    fringe.put((pathCost, neighbor))

        print(f"Goal: {self.state, f}")

    def isGoal(self):
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

    def getNeigbors(self):
        length = len(self.state)

        if length == 0:
            return [[equip] for equip in self.equipmentStatus.equipment]
        else:
            return [
                sorted(self.state[: length - 1] + [equip])
                for equip in self.equipmentStatus.equipment
                if equip not in self.state
            ] + [
                sorted(self.state + [equip])
                for equip in self.equipmentStatus.equipment
                if equip not in self.state
            ]

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
                # "Chest",
                # "Shoulder",
                # "Arm",
            ]
            tolerance = 30
        else:
            # get target muscle groups and waiting time from web
            target, tolerance = get_user_input()
        return (target, tolerance)

    def getEquipmentStatus(self, df):
        numWait, waitTime = input.getUsageList(df)
        numAvailabe, useTime = input.getWaitingList(df)
        df["waiting number"] = numWait
        df["expected usage time for waiting people"] = waitTime
        df["availabel number"] = numAvailabe
        df["expected usage time for occupied equipments"] = useTime


if __name__ == "__main__":
    userInput = Algorithm.getTargetMuscleGroup(muscleGroup=None)

    tomy = Algorithm(userInput)
    tomy.method()
