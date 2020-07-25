#An A* Search program that utilises a Manhattan Distance heuristic
#Visuals are completed within pygame
global goalCellX, goalCellY, XMax, YMax, Cost

"""Heauristic function to calculate the distance to the goal"""
def ManhattanDistance(currentCellX, currentCellY):
    global goalCellX, goalCellY
    return(abs(currentCellX - goalCellX) + abs(currentCellY - goalCellY))

"""Function that evaluates all the neighbours and selects the best move """
#def EvaluateNeighbour(currentCellX, currentCellY):
goalCellX = 3
goalCellY = 3
print(ManhattanDistance(1,1))
