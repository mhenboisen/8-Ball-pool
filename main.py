from pygame_functions import *

#variables

objects = []
balls = []
#BALL_SPRITES = ['1ball.png','2ball.png','3ball.png','4ball.png','5ball.png','6ball.png','7ball.png','8ball.png','1ball.png','2ball.png','3ball.png','4ball.png','5ball.png','6ball.png','7ball.png','cueball.png',]
BALL_SPRITES = ['1ball.png','1ball.png','1ball.png','1ball.png','1ball.png','1ball.png','1ball.png','8ball.png','2ball.png','2ball.png','2ball.png','2ball.png','2ball.png','2ball.png','2ball.png','cueball.png',]

foul = False
gameOver = False
turn = 0
GRAVITY = 9.81
SPINNING_FRICTION = 0.2
ROLLING_FRICTION = 0.1
RADIUS = 12
BOARD_WIDTH = 1500
BOARD_HEIGHT = 750


#subprograms

#procedure to set all the balls into the correct positions
def rackBalls():
    balls[0].moveBall(1175,450)
    balls[8].moveBall(1196,462)
    balls[10].moveBall(1196,438)
    balls[11].moveBall(1217,474)
    balls[7].moveBall(1217,450)
    balls[14].moveBall(1217,426)
    balls[4].moveBall(1238,486)
    balls[1].moveBall(1238,462)
    balls[12].moveBall(1238,438)
    balls[3].moveBall(1238,414)
    balls[6].moveBall(1259,498)
    balls[13].moveBall(1259,474)
    balls[2].moveBall(1259,450)
    balls[5].moveBall(1259,426)
    balls[9].moveBall(1259,402)
    balls[15].moveBall(425,450)
    
#classes

class Object:
    def __init__(self,Pxpos,Pypos,Psprite):
        self.xpos = Pxpos
        self.ypos = Pypos
        self.sprite = makeSprite(Psprite)

    def moveBall(self,newX,newY):
        self.xpos = newX
        self.ypos = newY

        self.draw()

    def draw(self):
        moveSprite(self.sprite,self.xpos,self.ypos)
        showSprite(self.sprite)

class Ball(Object):
    def __init__(self,Pxpos,Pypos,Psprite):
        super().__init__(Pxpos,Pypos,Psprite)

    def detectCollisions(self,objects):
        for object in objects:
            if object.sprite != self.sprite:
                if touching(object.sprite,self.sprite):
                    return True



        
        

#MAIN**********************************

screenSize(1600,900)

setBackgroundImage('table.png')

#at the start of the game, all of the balls will be on the table 
#the cue ball is ball 16
for i in range (len(BALL_SPRITES)):
    balls.append(Ball(0,0,BALL_SPRITES[i]))

for ball in balls:
    objects.append(ball)
rackBalls()

while not gameOver:

    for i in range(len(balls)):
        if balls[i].detectCollisions(objects):
            print(i+1)
                

    tick(30)



endWait()
