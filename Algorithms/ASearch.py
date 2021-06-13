#An A* Search program that utilises a Manhattan Distance heuristic
#Visuals are completed within pygame

"""Heauristic function to calculate the distance to the goal"""
def ManhattanDistance(goalCellX, goalCellY, currentCellX, currentCellY):
    return(abs(currentCellX - goalCellX) + abs(currentCellY - goalCellY))


"""Function that evaluates all the neighbours and selects the best move """
#def EvaluateNeighbour(currentCellX, currentCellY):
