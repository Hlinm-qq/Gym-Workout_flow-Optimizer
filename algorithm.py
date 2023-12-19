import random

random.seed(1126)


class Algorithm:
    def __init__(self):
        pass

    def method(self):
        pass

    def getTargetMuscleGroup(self, muscleGroup, defaultSet=True):
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
                "Chest",
                "Shoulder",
                "Arm",
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
