import pygame 
import random
pygame.init()

sw = 800
sh = 800
bg = pygame.image.load('starsbg.png')
window = pygame.display.set_mode((sw,sh))
pygame.display.set_caption("BREAKOUT")

brickHitSound = pygame.mixer.Sound("bullet.wav")
bounceSound = pygame.mixer.Sound("hitGameSound.wav")
bounceSound.set_volume(.3)

clock = pygame.time.Clock()

gameover = False

class Paddle(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self,window):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.w, self.h])

class Ball(object):
    def __init__(self, x, y, w, h, color):
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.color = color
        self.xv = random.choice([2,3,4,-2,-3,-4])
        self.yv = random.randint(3,4)
        self.xx = self.x + self.w
        self.yy = self.y + self.w

    def draw(self,window):
        pygame.draw.rect(window, self.color, [self.x,self.y, self.w, self.h])

    def move(self):
        self.x += self.xv
        self.y += self.yv

class Brick(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.xx = self.x + self.w
        self.yy = self.y + self.h

        self.ranNum = random.randint(0,10)
        if self.ranNum < 3:
            self.pregnant = True
        else:
            self.pregnant = False

    def draw(self,window):
        pygame.draw.rect(window, self.color, [self.x, self.y, self.w, self.h])

bricks = [] # array that stores all the brick objects
def init():#initializes all the blocks
    global bricks
    bricks = []
    for i in range(6): # 6 rows
        for j in range (10): # 10 columns
            bricks.append(Brick(10 + j * 79, 50 + i * 35, 70, 25, (128, 0, 0)))

def redrawGameWindow():
    window.blit(bg,(0,0))
    player.draw(window)
    for ball in balls:
        ball.draw(window)
    for b in bricks:
        b.draw(window)

    font = pygame.font.SysFont('comicsans', 50)
    if gameover:
        if len(bricks)==0:
            resText = font.render("Congrats!", 1, (255, 255, 255))
        else:
            resText = font.render("Thats tough, try again!", 1, (255,255,255))
        window.blit(resText, ((sw//2 - resText.get_width()//2), sh//2 - resText.get_height()//2))
        playAgainText = font.render("Press Space to Play Again", 0.5, (255,255,255))
        window.blit(playAgainText, ((sw//2 - playAgainText.get_width()//2), sh//2 - playAgainText.get_height()//2 + 40))
    pygame.display.update()

ball = Ball(sw/2 - 10,sh - 200, 20, 20, (250,157,0))
balls = [ball]

player = Paddle(sw/2 - 50,sh-100,140,20, (0,197,144))
init() # initialize the array of bricks
run = True
while run:
    clock.tick(100)
    if not gameover:
        for ball in balls:
            ball.move()
        #doesn't allow the paddle to go to far left off the screen
        # [0] represent mouse's x position
        if(pygame.mouse.get_pos()[0] - player.w//2 < 0):
            player.x = 0
        #doesn't allow the paddle to go to far right off the screen
        elif(pygame.mouse.get_pos()[0] + player.w//2 > sw):
            player.x = sw - player.w
        #defines the position of the paddle as per mouse x movement
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w // 2

        for ball in balls:
            #checks if ball is between the paddle
            if(ball.x >= player.x and ball.x <= player.x + player.w) or (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
                #checks if ball's y position matches the y position of paddle - contact
                if(ball.y + ball.h >= player.y) and (ball.y + ball.h <= player.y + player.h):
                    ball.yv *= -1 
                    ball.y = player.y - ball.h - 1
                    bounceSound.play()

            if ball.x + ball.w >= sw:
                bounceSound.play()
                ball.xv *= -1

            if ball.x < 0:
                bounceSound.play()
                ball.xv *= -1

            if ball.y <= 0:
                bounceSound.play()
                ball.yv *= -1

            if ball.y > sh:
                balls.pop(balls.index(ball))

        for brick in bricks:
            for ball in balls:
                if(ball.x >= brick.x and ball.x <= brick.x + brick.w) or (ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w):
                    if(ball.y >= brick.y and ball.y <= brick.y + brick.h) or (ball.y + ball.h >= brick.y and ball.y + ball.h <= brick.y + brick.h):
                        brick.color = (255,113,181)
                        brick.visible = False
                        if brick.pregnant:
                            balls.append(Ball(brick.x, brick.y, 20, 20, (250,157,0)))
                        #bricks.pop(bricks.index(brick))
                        ball.yv *= -1
                        brickHitSound.play()
                        break
        
        for brick in bricks:
            if brick.visible == False:
                bricks.pop(bricks.index(brick))

        if len(balls) == 0: 
            gameover = True
 
    keys = pygame.key.get_pressed()
    if len(bricks) == 0:
        won = True
        gameover = True
    if gameover:
        if keys[pygame.K_SPACE]:
            gameover = False
            won = False
            ball = Ball(sw/2 - 10,sh - 200, 20, 20, (250,157,0))
            if len(balls) == 0:
                balls.append(ball)
            bricks.clear()
            init()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()
pygame.quit()