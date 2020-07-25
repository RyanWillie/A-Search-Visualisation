#An A* Search program that utilises a Manhattan Distance heuristic
#Visuals are completed within pygame
import pygame
import math

""" Initialise PyGame and required attributes """
pygame.init()
window = pygame.display.set_mode((1000,800))
pygame.display.set_caption("A* Search Visualization")

""" Class to hold all of the required colours """
class Colours:
    red = (255,0,0)
    blue = (0,255,0)
    green = (0,0,255)
    cyan = (3,252,240)
    yellow = (244,252,3)
    pink = (252,3,252)
    white = (255,255,255)
    black = (0,0,0)
    purple = (153,0,204)
    grey = (169,169,169)
    navy = (70,85,110)
colours = Colours

""" Class to hold all of the information for each node in the grid """
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = colours.white
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    #Returns the postition of the nodes
    def getPos(self):
        return self.row, self.col
    
    #Returns a bool is the node has been checked
    def isChecked(self):
        return self.color == colours.red

    #Returns a bool if the node is in the Open list
    def isOpen(self):
        return self.color == colours.green

    #Returns a bool if the node is a Blockade
    def isBlockade(self):
        return self.color == colours.black
    
    #Returns a bool if the node is the starting point
    def isStart(self):
        return self.color == colours.pink

    #Returns a bool if the node is the end point
    def isEnd(self):
        return self.color == colours.cyan

    #Sets the colour back to white
    def resetNode(self):
        self.color = colours.white

    #Sets the node as being checked
    def makeChecked(self):
        self.color = colours.red
    
    
    #Sets the node as being open
    def makeOpen(self):
        self.color = colours.green
        
    
    #Sets the node as being a blockade
    def makeBlockade(self):
        self.color = colours.black
        
    #Set the node as the starting point
    def makeStart(self):
        self.color = colours.pink
    
    #Set the node as the end point
    def makeEnd(self):
        self.color = colours.cyan
    
    #Set the node as being apart of the final path
    def makePath(self):
        self.color = colours.purple

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbour(self, grid):
        self.neighbours = []
        #Check the node below if it is a valid location
        if self.row < self.total_rows -1 and not grid[self.row - 1][self.col].isBlockade(): #Down
            self.neighbours.append(grid[self.rows + 1][self.col])

        #Check the node above if it is a valid location
        if self.row > 0 and not grid[self.row - 1][self.col].isBlockade(): #Up
            self.neighbours.append(grid[self.rows - 1][self.col])

        #Check the node to the left if it is a valid location
        if self.col > 0 and not grid[self.row][self.col - 1].isBlockade(): # Left
            self.neighbours.append(grid[self.rows][self.col-1])

        #Check the node to the right if it is a valid location
        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].isBlockade(): #Right
            self.neighbours.append(grid[self.rows][self.col+ 1])

    def __lt__(self, other):
        return False

"""Heauristic function to calculate the distance to the goal"""
def ManhattanDistance(currentCellX, currentCellY):
    global goalCellX, goalCellY
    return(abs(currentCellX - goalCellX) + abs(currentCellY - goalCellY))

"""Creates a grid object with the required nodes in each location"""
def makeGrid(rows, width):
    grid = []
    #The distance between each grid is the width / the number of rows
    distance = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, distance, rows)
            grid[i].append(node)
    
    return grid

"""Function to draw the gridlines """
def drawGridLines(window, rows, width):
    distance = width // rows
    for i in range(rows):
        pygame.draw.line(window, colours.grey, (0, i * distance), (width, i * distance))
        for j in range(rows):
            pygame.draw.line(window, colours.grey, (j * distance, 0), (j * distance, width))


""" Draws each node on the screen """
def draw(window, grid, rows, width):
    window.fill(colours.white)

    #Creating the Menu
    pygame.draw.rect(window, colours.navy, (width, 0, 200, 800))

    pygame.draw.rect(window, colours.white, (width + 20,30, 50, 50))


    buttonText = pygame.font.Font('freesansbold.ttf', 16)
    text = buttonText.render('Test Text!', True, colours.black, colours.white)
    textRect = text.get_rect()
    textRect.center = (850, 25)
    window.blit(text, textRect)
    #Iterates through the grid and calls each node to draw itself
    for row in grid:
        for node in row:
            node.draw(window)
    #Draws the grid lines over each node
    drawGridLines(window, rows, width)
    pygame.display.update()

def getClickLocation(pos, rows, width):
    distance = width // rows
    y, x = pos
    row = y // distance
    col = x // distance
    return row, col

def main(window, width):
    rows = 50
    grid = makeGrid(rows, width)
    

    start = None
    end = None

    run = True
    started = False

    while(run):
        draw(window, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickLocation(pos, rows, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.makeStart()
                elif not end:
                    end = node
                    end.makeEnd()
                elif not (node.isStart()) and not (node.isEnd()):
                    node.makeBlockade()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getClickLocation(pos, rows, width)
                node = grid[row][col]
                if node.isStart():
                    start = None
                elif node.isEnd():
                    end = None
                node.resetNode()
            if event.type == pygame.KEYDOWN:
                if even.key == pygame.K_SPACE and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.updateNeighbour(grid)
    pygame.quit()

main(window, 800)