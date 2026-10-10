import sys
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
BG_COLOR = (0,0,0) #(40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=True)
pygame.display.set_caption("color switch")
clock = pygame.time.Clock()

terminalVelocity = -1500
ballVelocity = 0
jumpForce = 250
gravity = -600
ballY = HEIGHT/2

class ring:
    def __init__(self, x, y, screen, radius=50, width=18, rotation=0, resolution=200, colors=[(140, 19, 251), (255, 0, 128), (53, 226, 242), (246, 223, 14)]):
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

def jump():
    global ballVelocity
    ballVelocity = jumpForce

smallRing = ring(WIDTH/2, HEIGHT/2, screen)
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

    screen.fill(BG_COLOR)
    
    smallRing.render()
    pygame.draw.circle(screen, (255,255,255), (WIDTH/2, ballY), 10)

    pygame.display.flip()

pygame.quit()
sys.exit()
