import sys
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 350, 600
FPS = 60
BG_COLOR = (0,0,0) #(40, 40, 40)

PURPLE = 0
PINK = 1
CYAN = 2
YELLOW = 3
WHITE = 4

colors=[(140, 19, 251), (255, 0, 128), (53, 226, 242), (246, 223, 14)]
ballColors=[(140, 19, 251), (255, 0, 128), (53, 226, 242), (246, 223, 14), (255,255,255)]

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=True)
pygame.display.set_caption("color switch")
clock = pygame.time.Clock()

terminalVelocity = -1500
ballVelocity = 0
jumpForce = 250
gravity = -600
ballRadius = 10
ballColor = 0
ballY = HEIGHT/2

class ring:
    def __init__(self, x, y, screen, radius=50, width=18, rotation=0, resolution=200):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.screen = screen
        self.rotation = rotation
        self.colors = colors
        self.resolution = resolution
        
    def render(self):
        segmentSize = 360/len(self.colors)
        for i, color in enumerate(self.colors):
            startDir = self.rotation + i * segmentSize
            points = [(self.x, self.y)]
            for step in range(self.resolution + 1):
                dir = startDir + step * (segmentSize/self.resolution)
                dirRadians = math.radians(dir)
                x = self.x + (self.radius + self.width) * math.cos(dirRadians)
                y = self.y + (self.radius + self.width) * math.sin(dirRadians)
                
                points.append((x,y))
            pygame.draw.polygon(self.screen, color, points)
        pygame.draw.circle(self.screen, (0,0,0), (self.x, self.y), self.radius)
        
    def collisionCheck(self, ballX, ballY, ballRadius):
        distance = math.dist((ballX, ballY), (self.x, self.y))
        if distance > (self.radius - ballRadius) and distance < (self.radius + self.width + ballRadius):
            dx = ballX - self.x
            dy = ballY - self.y
            
            radians = math.atan2(dy, dx)
            degrees = math.degrees(radians)
            
            if degrees < 0:
                degrees += 360
            
            segmentSize = 360/len(self.colors)
            for i in range(len(self.colors)):
                startDir = self.rotation + i * segmentSize
                endDir = startDir + segmentSize
                
                if (degrees - startDir) % 360 <= (endDir - startDir) % 360:
                    return True, i
        return False, -1

class movingWall:
    def __init__(self, y, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.y = y
        self.x = 0
        self.pivotX = self.width/2
        self.colors = colors
        self.offset = 0
        self.height = 18
        self.rotation = 45
    
    def render(self):
        self.width = math.sin(math.radians(90)) * (screen.get_width()/math.sin(math.radians(self.rotation))) + self.height
        wallSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        miniWidth = self.width/4
        for i, color in enumerate(self.colors):
            posX = (i * miniWidth + self.offset) % self.width
            pygame.draw.rect(wallSurface, color, (posX, 0, miniWidth+1, self.height))
            if (posX + (miniWidth+1)) > self.width:
                extraWidth = (posX + (miniWidth+1)) - self.width
                pygame.draw.rect(wallSurface, color, (0, 0, extraWidth, self.height))
        
        rotatedSurface = pygame.transform.rotate(wallSurface, self.rotation)
        rotatedRect = rotatedSurface.get_rect(center=(self.pivotX, self.y + (self.height/2)))
        
        self.screen.blit(rotatedSurface, rotatedRect)
    
    def collisionCheck(self, ballX, ballY, ballRadius):        
        if (ballY + ballRadius) > self.y and (ballY - ballRadius) < (self.y + self.height):
            miniWidth = self.width/4
            for i in range(len(self.colors)):
                startX = (i * miniWidth + self.offset) % self.width
                endX = startX + miniWidth
                if (ballX + ballRadius) < endX and (ballX - ballRadius) > startX:
                    return True, i
        return False, -1
            

def jump():
    global ballVelocity
    ballVelocity = jumpForce

smallRing = ring(WIDTH*0.6, HEIGHT*0.7, screen)
smallWall = movingWall(HEIGHT*0.4, screen)
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump()
                
    ballY -= ballVelocity * dt
    ballVelocity = max(ballVelocity + gravity * dt, terminalVelocity)
    smallRing.rotation += 130 * dt
    smallWall.offset += 50 * dt
    
    collision, colorIndex = smallRing.collisionCheck(WIDTH/2, ballY, ballRadius)
    #if collision:
       # if colorIndex != ballColor:
            #running = False
            
    collision, colorIndex = smallWall.collisionCheck(WIDTH/2, ballY, ballRadius)
    if collision:
        if colorIndex != ballColor:
            running = False

    screen.fill(BG_COLOR)
    
    smallRing.render()
    smallWall.render()
    pygame.draw.circle(screen, ballColors[ballColor], (WIDTH/2, ballY), ballRadius)

    pygame.display.flip()

pygame.quit()
sys.exit()
