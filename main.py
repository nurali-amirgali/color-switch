import sys
import pygame

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

def jump():
    global ballVelocity
    ballVelocity = jumpForce

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump()

    screen.fill(BG_COLOR)
    pygame.draw.circle(screen, (255,255,255), (WIDTH/2, ballY), 10)
    
    ballY -= ballVelocity * dt
    ballVelocity = max(ballVelocity + gravity * dt, terminalVelocity)

    pygame.display.flip()

pygame.quit()
sys.exit()
