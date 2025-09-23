from pygame_functions import *

#variables

targetFps = 144

objects = []
balls = []
BALL_SPRITES = ['1ball.png','2ball.png','3ball.png','4ball.png','5ball.png','6ball.png','7ball.png','8ball.png','9ball.png','10ball.png','11ball.png','12ball.png','13ball.png','14ball.png','15ball.png','cueball.png',]

foul = False
gameOver = False
ballInHand = False
turn = 0
fps = 0
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

#function to get the cross product of two vectors

def crossProduct(vectorA,vectorB):
	result = [0,0,0]
	result[0] = vectorA[1]*vectorB[2] - vectorA[2]*vectorB[1]
	result[1] = -vectorA[0]*vectorB[2] - vectorA[2]*vectorB[0]
	result[2] = vectorA[0]*vectorB[1] - vectorA[1]*vectorB[0]

	return result

    
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
                
    def dragBall(self):
        if spriteClicked(self.sprite):
            self.xpos = mouseX()
            self.ypos = mouseY()
            moveSprite(self.sprite,self.xpos,self.ypos,centre=True)


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

ballInHandLabel = newLabel('Ball not in hand',20,'arial','black',0,0,'white')
fpsLabel = newLabel('0',20,'arial','black',0,25,'white')
showLabel(ballInHandLabel)
showLabel(fpsLabel)

while not gameOver:

    #detect collisions of balls
    for i in range(len(balls)):
        if balls[i].detectCollisions(objects):
            print(i+1)
                
    
    #toggle ball in hand
    if spriteClicked(ballInHandLabel):
        if ballInHand:
            ballInHandLabel.update('ball not in hand','black','white')
            ballInHand = False
        else:
            ballInHandLabel.update('ball in hand','black','white')
            ballInHand = True
        pause(100)

    #allows ball in hand program to run
    if ballInHand == True:
        balls[15].dragBall()

    #update fps
    fps = 'fps: ' + str(tick(targetFps).__round__(0))[:-2]
    fpsLabel.update(fps,'black','white')

endWait()
