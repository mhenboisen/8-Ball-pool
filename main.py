import pygame_functions

#variables

objects = []
balls = []
foul = False
gameOver = False
turn = 0
GRAVITY = 9.81
SPINNING_FRICTION = 0.2
ROLLING_FRICTION = 0.1
RADIUS = 10
BOARD_WIDTH = 1500
BOARD_HEIGHT = 750


#subprograms

#classes

class Object:
    def __init__(self,Pxpos,Pypos,Psprite):
        self.xpos = Pxpos
        self.ypos = Pypos
        self.sprite = Psprite

    def draw(self):
        pass


        
        

#MAIN**********************************

pygame_functions.screenSize(1600,900)

y = Object(0,0,'table.piskel')


pygame_functions.endWait()
