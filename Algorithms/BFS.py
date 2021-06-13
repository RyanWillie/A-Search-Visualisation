import pygame
import queue

def BreadthFirstSearch(window, grid, rows, width, startX, startY, startTime, endX, endY):
    q = queue.Queue()
    startingNode = grid[startX][startY]
    q.put(startingNode)

    while not q.empty():
        state = q.get()
        #Check if its the goal node
        if(state.isEnd()):
            print("Goal node found!!!")
            return 

        if not state.isChecked():
            
            stateX, stateY = state.getPos()
                    
            #check right
            if(stateX+1 < 50):
                if(grid[stateX+1][stateY].isOpen()):
                    q.put(grid[stateX+1][stateY])
            #check left
            if(stateX-1 < -1):
                if(grid[stateX-1][stateY].isOpen()):
                    q.put(grid[stateX-1][stateY])
            #check up
            if(stateY-1 < -1):
                if(grid[stateX][stateY-1].isOpen()):
                    q.put(grid[stateX][stateY-1])
            #check down
            if(stateY+1 < 50):
                if(grid[stateX][stateY+1].isOpen()):
                    q.put(grid[stateX][stateY+1])
            state.makeChecked()
        pygame.display.update()
