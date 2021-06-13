#Visuals are completed within pygame
import pygame
import math
import sys
import time
import queue

#Import Algorimths
import Algorithms.ASearch as ASearch
import Algorithms.BFS as BFS
import Algorithms.DFS as DFS
import Algorithms.IDFS as IDFS


""" Initialise PyGame and required attributes """
pygame.init()
window = pygame.display.set_mode((1000,800))
pygame.display.set_caption("Search Algorithm Visualization")



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

    #Returns the postition of the node
    def getPos(self):
        return self.row, self.col
    
    #Returns a bool is the node has been checked
    def isChecked(self):
        return self.color == colours.red

    #Returns a bool if the node is in the Open list
    def isOpen(self):
        return self.color == colours.white

    #Returns a bool if the node is a wall
    def isWall(self):
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
        self.color = colours.white
    
    #Sets the node as being a blockade
    def makeWall(self):
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
        
        #Check the node to the right if it is a valid location
        if self.col < self.total_rows -1 and not grid[self.row][self.col + 1].isWall(): #Right
            self.neighbours.append(grid[self.row][self.col+ 1])

        #Check the node to the left if it is a valid location
        if self.col > 0 and not grid[self.row][self.col - 1].isWall(): # Left
            self.neighbours.append(grid[self.row][self.col-1])

        #Check the node below if it is a valid location
        if self.row < self.total_rows -1 and not grid[self.row - 1][self.col].isWall(): #Down
            self.neighbours.append(grid[self.row + 1][self.col])

        #Check the node above if it is a valid location
        if self.row > 0 and not grid[self.row - 1][self.col].isWall(): #Up
            self.neighbours.append(grid[self.row - 1][self.col])


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

""" Draws the menu screen"""
def drawMenu(window, selected, time):
    "Adding in Title"
    TitleFont = pygame.font.Font('freesansbold.ttf', 16)
    Titletext = TitleFont.render('Algorithm Visualizer', True, colours.white, colours.navy)
    TitletextRect = Titletext.get_rect()
    TitletextRect.center = (900, 25)
    window.blit(Titletext, TitletextRect)

    TitleTextSmall = pygame.font.Font('freesansbold.ttf', 10)
    Titletext2 = TitleTextSmall.render('By Ryan Williamson', True, colours.white, colours.navy)
    TitletextRect2 = Titletext2.get_rect()
    TitletextRect2.center = (900, 45)
    window.blit(Titletext2, TitletextRect2)

    Titletext3 = TitleFont.render('Uninformed Search', True, colours.white, colours.navy)
    TitletextRect3 = Titletext3.get_rect()
    TitletextRect3.center = (900, 75)
    window.blit(Titletext3, TitletextRect3)

    Titletext4 = TitleFont.render('Informed Search', True, colours.white, colours.navy)
    TitletextRect4 = Titletext4.get_rect()
    TitletextRect4.center = (900, 200)
    window.blit(Titletext4, TitletextRect4)


    """------------------Adding in Algorithm Selector----------------------- """
    if(selected == 1):
        pygame.draw.circle(window, colours.black, (820, 100), 5)
        pygame.draw.circle(window, colours.white, (820, 120), 5)
        pygame.draw.circle(window, colours.white, (820, 140), 5)
        pygame.draw.circle(window, colours.white, (820, 220), 5)
        pygame.draw.circle(window, colours.white, (820, 240), 5)
        pygame.draw.circle(window, colours.white, (820, 260), 5)
    elif selected == 2:
        pygame.draw.circle(window, colours.white, (820, 100), 5)
        pygame.draw.circle(window, colours.black, (820, 120), 5)
        pygame.draw.circle(window, colours.white, (820, 140), 5)
        pygame.draw.circle(window, colours.white, (820, 220), 5)
        pygame.draw.circle(window, colours.white, (820, 240), 5)
        pygame.draw.circle(window, colours.white, (820, 260), 5)
    elif selected == 3:
        pygame.draw.circle(window, colours.white, (820, 100), 5)
        pygame.draw.circle(window, colours.white, (820, 120), 5)
        pygame.draw.circle(window, colours.black, (820, 140), 5)
        pygame.draw.circle(window, colours.white, (820, 220), 5)
        pygame.draw.circle(window, colours.white, (820, 240), 5)
        pygame.draw.circle(window, colours.white, (820, 260), 5)
    elif selected == 4:
        pygame.draw.circle(window, colours.white, (820, 100), 5)
        pygame.draw.circle(window, colours.white, (820, 120), 5)
        pygame.draw.circle(window, colours.white, (820, 140), 5)
        pygame.draw.circle(window, colours.black, (820, 220), 5)
        pygame.draw.circle(window, colours.white, (820, 240), 5)
        pygame.draw.circle(window, colours.white, (820, 260), 5)
    elif selected == 5: 
        pygame.draw.circle(window, colours.white, (820, 100), 5)
        pygame.draw.circle(window, colours.white, (820, 120), 5)
        pygame.draw.circle(window, colours.white, (820, 140), 5)
        pygame.draw.circle(window, colours.white, (820, 220), 5)
        pygame.draw.circle(window, colours.black, (820, 240), 5)
        pygame.draw.circle(window, colours.white, (820, 260), 5)
    elif selected == 6:
        pygame.draw.circle(window, colours.white, (820, 100), 5)
        pygame.draw.circle(window, colours.white, (820, 120), 5)
        pygame.draw.circle(window, colours.white, (820, 140), 5)
        pygame.draw.circle(window, colours.white, (820, 220), 5)
        pygame.draw.circle(window, colours.white, (820, 240), 5)
        pygame.draw.circle(window, colours.black, (820, 260), 5)

    buttonTextSmall = pygame.font.Font('freesansbold.ttf', 12)
    MenuOption1 = buttonTextSmall.render('Breadth First Search', True, colours.white, colours.navy)
    MenuOptionRect1 = MenuOption1.get_rect()
    MenuOptionRect1.center = (900, 100)
    window.blit(MenuOption1, MenuOptionRect1)

    MenuOption2 = buttonTextSmall.render('Depth First Search', True, colours.white, colours.navy)
    MenuOptionRect2 = MenuOption2.get_rect()
    MenuOptionRect2.center = (900, 120)
    window.blit(MenuOption2, MenuOptionRect2)

    MenuOption3 = buttonTextSmall.render('Iterative Deepening Search', True, colours.white, colours.navy)
    MenuOptionRect3 = MenuOption3.get_rect()
    MenuOptionRect3.center = (910, 140)
    window.blit(MenuOption3, MenuOptionRect3)

    MenuOption4 = buttonTextSmall.render('Greedy Search', True, colours.white, colours.navy)
    MenuOptionRect4 = MenuOption4.get_rect()
    MenuOptionRect4.center = (900, 220)
    window.blit(MenuOption4, MenuOptionRect4)

    MenuOption5 = buttonTextSmall.render('A* Search', True, colours.white, colours.navy)
    MenuOptionRect5 = MenuOption5.get_rect()
    MenuOptionRect5.center = (900, 240)
    window.blit(MenuOption5, MenuOptionRect5)

    MenuOption6 = buttonTextSmall.render('Hill Climbing Search', True, colours.white, colours.navy)
    MenuOptionRect6 = MenuOption6.get_rect()
    MenuOptionRect6.center = (900, 260)
    window.blit(MenuOption6, MenuOptionRect6)
    """ ------------- Adding in statistics ------------------ """
    StatsView1 = buttonTextSmall.render('Time Taken: ' + str(time)[:4], True, colours.white, colours.navy)
    StatsViewRect1 = MenuOption4.get_rect()
    StatsViewRect1.center = (860, 400)
    window.blit(StatsView1, StatsViewRect1)

    StatsView1 = buttonTextSmall.render('Path Length: 10', True, colours.white, colours.navy)
    StatsViewRect1 = MenuOption4.get_rect()
    StatsViewRect1.center = (860, 420)
    window.blit(StatsView1, StatsViewRect1)

    


""" Draws each node on the screen """
def draw(window, grid, rows, width, selected, runTime):
    window.fill(colours.white)

    #Creating the area for the Menu
    pygame.draw.rect(window, colours.navy, (width, 0, 200, 800))
    #pygame.draw.rect(window, colours.white, (width + 20,30, 50, 50))
    drawMenu(window, selected, runTime)
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
    selected = 1
    grid = makeGrid(rows, width)

    start = None
    end = None

    run = True
    started = False

    while(run):
        if started:
            draw(window, grid, rows, width, selected, time.time() - startTime)
        else: 
            draw(window, grid, rows, width, selected, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickLocation(pos, rows, width)
                #print("Row: " + str(row) + " Col: " + str(col) )
                if row >= 50:
                    """They've clicked the menu, find out what element"""
                    if col == 6:
                        selected = 1
                    elif col == 7:
                        selected = 2
                    elif col == 8:
                        selected = 3
                    elif col == 13:
                        selected = 4
                    elif col == 14:
                        selected = 5
                    elif col == 16:
                        selected = 6
                else:
                    node = grid[row][col]
                    if not start:
                        start = node
                        startX = row
                        startY = col
                        start.makeStart()
                    elif not end:
                        end = node
                        endX = row
                        endY = col
                        end.makeEnd()
                    elif not (node.isStart()) and not (node.isEnd()):
                        node.makeWall()

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
                """ Check if the game should be started"""
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    startTime = time.time()
                    for row in grid:
                        for node in row:
                            node.updateNeighbour(grid)
                    if selected == 1:
                        BFS.BreadthFirstSearch(window, grid, rows, width, startX, startY, startTime, endX, endY)
                    elif selected == 2:
                        DFS.DepthFirstSearch()
                    elif selected == 3:
                        BFS.BreadthFirstSearch(window, grid, rows, width, startX, startY, startTime, endX, endY)
                    elif selected == 4:
                        BFS.BreadthFirstSearch(window, grid, rows, width, startX, startY, startTime, endX, endY)

    pygame.quit()
    sys.exit()

main(window, 800)