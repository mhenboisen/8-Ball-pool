from pygame_functions import *
import math

#variables

targetFps = 60

objects = []
balls = []
BALL_SPRITES = ["1ball.png",'2ball.png','3ball.png','4ball.png','5ball.png','6ball.png','7ball.png','8ball.png','9ball.png','10ball.png','11ball.png','12ball.png','13ball.png','14ball.png','15ball.png','cueball.png',]
BORDER_SPRITES = ['horizontal_border.png','vertical_border.png']
foul = False
gameOver = False
ballInHand = False
turn = 0
fps = targetFps
GRAVITY = 9.81
SPINNING_FRICTION = 0.2
ROLLING_FRICTION = 0.01
BALL_RESTITUTION = 0.98
CUSHION_RESTITUTION = 0.95
RADIUS = 12
BOARD_WIDTH = 1500
BOARD_HEIGHT = 750


#subprograms

#procedure to set all the balls into the correct positions
def rackBalls():
    balls[0].moveObject(1175,450)
    balls[8].moveObject(1196,462)
    balls[10].moveObject(1196,438)
    balls[11].moveObject(1217,474)
    balls[7].moveObject(1217,450)
    balls[14].moveObject(1217,426)
    balls[4].moveObject(1238,486)
    balls[1].moveObject(1238,462)
    balls[12].moveObject(1238,438)
    balls[3].moveObject(1238,414)
    balls[6].moveObject(1259,498)
    balls[13].moveObject(1259,474)
    balls[2].moveObject(1259,450)
    balls[5].moveObject(1259,426)
    balls[9].moveObject(1259,402)
    balls[15].moveObject(425,450)

#function to get the cross product of two vectors

def crossProduct(vectorA,vectorB):
	result = [0,0,0]
	result[0] = vectorA[1]*vectorB[2] - vectorA[2]*vectorB[1]
	result[1] = -vectorA[0]*vectorB[2] - vectorA[2]*vectorB[0]
	result[2] = vectorA[0]*vectorB[1] - vectorA[1]*vectorB[0]

	return result

def initialiseBorders():
    ballInHandLabel = newLabel('Ball not in hand',20,'arial','black',0,0,'white')
    bordersLabel = newLabel('borders on',20,'arial','black',0,25,'white')
    fpsLabel = newLabel('0',20,'arial','black',0,50,'white')

    showLabel(ballInHandLabel)
    showLabel(bordersLabel)
    showLabel(fpsLabel)

    
#classes

class Object:
    def __init__(self,Pxpos,Pypos,Psprite,Prestitution):
        self.xpos = Pxpos
        self.ypos = Pypos
        self.png = Psprite
        self.sprite = makeSprite(self.png)
        self.restitution = Prestitution

    def moveObject(self,newX,newY):
        self.xpos = newX
        self.ypos = newY

        self.draw()

    def draw(self):
        moveSprite(self.sprite,self.xpos,self.ypos,centre=True)
        showSprite(self.sprite)

class Ball(Object):
    def __init__(self,Pxpos,Pypos,Psprite,Prestitution):
        super().__init__(Pxpos,Pypos,Psprite,Prestitution)
        self.png = Psprite
        self.yspeed = 0
        self.xspeed = 0
        self.yacceleration = 0
        self.xacceleration = 0
        self.yangular = 0
        self.xangular = 0

    def detectCollisions(self,objects):
        for object in objects:
            if object.sprite != self.sprite:
                if touching(object.sprite,self.sprite):
                    self.collide(object)
                    return True

    def collide(self,object):

        if object in balls:

            e = self.restitution*object.restitution
            theta = math.atan2((object.ypos-self.ypos),(object.xpos-self.xpos))
            cos = math.cos(theta)
            sin = math.sin(theta)
            sbParallel = self.xspeed*cos + self.yspeed*sin
            sbPerpendicular = -self.xspeed*sin + self.yspeed*cos

            obParallel = object.xspeed*cos + object.yspeed*sin
            obPerpendicular = -object.xspeed*sin + object.yspeed*cos

            saParallel = 0.5 * (sbParallel + obParallel - e * (sbParallel - obParallel))
            saPerpendicular = sbPerpendicular

            oaParallel = 0.5 * (sbParallel + obParallel + e * (sbParallel - obParallel))
            oaPerpendicular = obPerpendicular


            #fix overlapping balls
            dx = object.xpos - self.xpos
            dy = object.ypos - self.ypos
            distance = math.sqrt(dx**2 + dy**2)
            min_dist = 2 * RADIUS  

            if distance < min_dist:
                overlap = min_dist - distance
                # Normalize vector between balls
                nx = dx / distance
                ny = dy / distance
                # Push balls apart
                self.xpos -= nx * overlap / 2
                self.ypos -= ny * overlap / 2
                object.xpos += nx * overlap / 2
                object.ypos += ny * overlap / 2

            self.xspeed = saParallel*cos-saPerpendicular*sin
            self.yspeed = saParallel*sin+saPerpendicular*cos

            object.xspeed = oaParallel*cos-oaPerpendicular*sin
            object.yspeed = oaParallel*sin+oaPerpendicular*cos




        else:
            if object in borders:
                if object.png== 'horizontal_border.png':
                    self.yspeed *= -1
                else:
                    self.xspeed *= -1

    def move(self):
        
        self.xacceleration = -self.xspeed*ROLLING_FRICTION
        self.yacceleration = -self.yspeed*ROLLING_FRICTION

        self.xspeed += self.xacceleration
        self.yspeed += self.yacceleration

        totalSpeed = sum((ball.xspeed + ball.yspeed) for ball in balls)
        if totalSpeed < 100:
            v = math.sqrt(self.xspeed**2 + self.yspeed**2)
            if v < 15:
                self.xspeed,self.yspeed = 0,0

        self.xpos += self.xspeed*(1/(int(fps)+1))
        self.ypos += self.yspeed*(1/(int(fps)+1))

        self.draw()

        return (self.xspeed != 0 or self.yspeed != 0)

    def dragBall(self):
        if spriteClicked(self.sprite):
            self.xpos = mouseX()
            self.ypos = mouseY()
            moveSprite(self.sprite,self.xpos,self.ypos,centre=True)

    def setSpeed(self,x,y):
        self.xspeed = int(x)
        self.yspeed = int(y)

class Border(Object):
    def __init__(self,Pxpos,Pypos,Psprite,Prestitution):
        super().__init__(Pxpos,Pypos,Psprite,Prestitution)
        self.png = Psprite
        moveSprite(self.sprite,self.xpos,self.ypos)
    



#MAIN**********************************

screenSize(1600,900)

setBackgroundImage('table.png')

#at the start of the game, all of the balls will be on the table 
#the cue ball is ball 16
for i in range (len(BALL_SPRITES)):
    balls.append(Ball(0,0,BALL_SPRITES[i],BALL_RESTITUTION))


for ball in balls:
    objects.append(ball)
rackBalls()


ballInHandLabel = newLabel('Ball not in hand',20,'arial','black',0,0,'white')
startTurnLabel = newLabel('Start',20,'arial','black',0,50,'white')
fpsLabel = newLabel('0',20,'arial','black',0,25,'white')

showLabel(ballInHandLabel)
showLabel(startTurnLabel)
showLabel(fpsLabel)

#borders
borders = []
borders.append(Border(0,0,BORDER_SPRITES[0],CUSHION_RESTITUTION))
borders.append(Border(2,697,BORDER_SPRITES[0],CUSHION_RESTITUTION))
borders.append(Border(0,0,BORDER_SPRITES[1],CUSHION_RESTITUTION))
borders.append(Border(1447,-5,BORDER_SPRITES[1],CUSHION_RESTITUTION))

for border in borders:
    objects.append(border)

clock = pygame.time.Clock()
pause(1000)

mouseWasDown = False
turnOver = True

while not gameOver:
    fps = clock.tick(targetFps)
    actual_fps = clock.get_fps()
    fpsLabel.update('fps: {}'.format(actual_fps), 'black', 'white')


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        
        elif spriteClicked(ballInHandLabel):
                ballInHand = not ballInHand
                ballInHandLabel.update('ball in hand' if ballInHand else 'ball not in hand', 'black', 'white')

        elif spriteClicked(startTurnLabel):
            turnOver = False
            ballInHand = False
            ballInHandLabel.update('ball not in hand', 'black', 'white')
            balls[15].setSpeed(500, 200)
    
    if ballInHand:
        balls[15].dragBall()


    # Move balls if turn active
    if not turnOver:
        ballMoving = False
        for ball in balls:
            if ball.move():
                ballMoving = True
            ball.detectCollisions(objects)
        if not ballMoving:
            turnOver = True

    updateDisplay()   

    
endWait()
