import random
import json


def showMuscleGroup():
    """Show muscle groups by category."""
    muscle_group = dict()
    translator = dict()
    with open(
        "data/category_rev.json",
        "r",
    ) as f:
        muscle_group = json.load(f)
    with open(
        "data/translate_E2C_dict.json",
        "r",
    ) as f:
        translator = json.load(f)

    for category in muscle_group.keys():
        print(f"category: {translator[category]}")
        for subgroup in muscle_group[category]:
            print(f"sub muscle group: {translator[subgroup]}")


def getRandomList(EquipmentDf):
    """Generate a list of lists.
        The number of the list correspondings to the equipment capacity.
        The number of the items in each sublist represents waiting number.
        The content of the items in each sublist represents the expected time.

    Args:
        EquipmentDf (df): read from equipment[_].csv
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


def getWaitingList(EquipmentDf):
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
    _, wantToUseTime = getRandomList(EquipmentDf)
    # compute the number of waiting number
    numWait = dict()
    for i in range(len(EquipmentDf)):
        numWait[i] = len(wantToUseTime[i])
    return numWait, wantToUseTime


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
    numAvailabe, UseTime = getRandomList(EquipmentDf)
    return numAvailabe, UseTime
