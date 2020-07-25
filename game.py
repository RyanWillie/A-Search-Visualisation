import pygame
import math

""" Initialise PyGame and required attributes """
pygame.init()
win = pygame.display.set_mode((800,800))
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
    
    #Sets the node as being checked
    def makeChecked(self):
        self.color = colours.red
        return
    
    #Sets the node as being open
    def makeOpen(self):
        self.color = colours.green
        return
    
    #Sets the node as being a blockade
    def makeBlockade(self):
        self.color = colours.black
        return


