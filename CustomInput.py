import random
import pandas as pd


def getWaitingList(numAvailable, EquipmentDf):
    """Generate 2 dicts:
          1. Waiting list (people who want to use equipments)
              (1) The number of people waiting.
              (2) The expected time that the waiting person wants to use the equipment.

    Args:
        EquipmentDf (df): read from equipment[_].csv

    Returns:
        numWait (dict): The number of people waiting.
        wantToUseTime (dict): The expected time.
    """
    # compute the number of waiting number
    dset = EquipmentDf.copy()
    dset = dset.set_index("equipment")
    status = dict()
    usageTime = dict()
    id = 0
    for name in dset.index:
        # get equipment status
        numWait = random.randint(0, 5) if numAvailable[id] == 0 else 0
        status[id] = numWait
        # get expected time
        if numWait == 0:
            usageTime[id] = []
        else:
            usageTime[id] = random.sample(range(5, 30), numWait)
        id += 1

    return (status, usageTime)


def getUsageList(EquipmentDf):
    """Generate 2 dicts:
          1. Usage list (people who are using equipments)
              (1) Real-time status of each piece of gym equipment (the number of available equipments).
              (2) The expected time each equipment will be in use.

    Args:
        EquipmentDf (df): read from equipment[_].csv

    Returns:
        numAvailabe (dict): The number of available equipments.
        UseTime (dict): The expected time each equipment will be in use.
    """
    dset = EquipmentDf.copy()
    dset = dset.set_index("equipment")
    status = dict()
    usageTime = dict()
    id = 0
    for name in dset.index:
        # get equipment status
        totalCapacity = dset.loc[name]["number"] * dset.loc[name]["capacity"]
        numAvailable = random.randint(0, totalCapacity)
        status[id] = numAvailable
        # get expected time
        if numAvailable == totalCapacity:
            usageTime[id] = []
        elif numAvailable != 0:
            usageTime[id] = random.sample(range(5, 30), totalCapacity - numAvailable)
        else:
            usageTime[id] = random.sample(range(5, 30), totalCapacity)
        id += 1

    return (status, usageTime)


if __name__ == "__main__":
    # showMuscleGroup()

    df = pd.read_csv("data/equipment.csv")
    # print(getRandomList(df))
    print(getUsageList(df))
