"""
    input:
        - occupancy status V
        - queue status V
        - expected time per person V
        - willingness to wait
        - available time (duration of wait tolerance)

        -- chatGpt input
        -- 
"""

def timeleft2Score(secondsLeft, tolerance):
    """
        tolerance       : how long user is willing to wait
    """
    None
    return secondsLeft/tolerance * 100

def queue2Score(queueNumList: [[]], tolerance):
    """
        queueNumList    : list of wait time per person in queue for each machine
        tolerance       : how long user is willing to wait
    """
    machineNum = len(queueNumList)
    cost = 0

    for n in machineNum:
        for time in queueNumList[n]:
            cost += timeleft2Score(time, tolerance)

    return cost

def heuristic(willWait: bool, tolerance, queueNumList):
    """
        willWait        : is the user willing to wait
        queueNumList    : list of wait time per person in queue for each machine
        tolerance       : how long user is willing to wait
    """
    waitVar = 1 if willWait else 2

    cost = (waitVar * 0.5) * queue2Score(queueNumList, tolerance)

    return cost


