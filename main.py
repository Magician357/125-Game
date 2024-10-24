import pygame
from sand import *

# pygame setup
pygame.init()
width,height = 700,800
screen = pygame.display.set_mode((700, 800))
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont('Arial', 18)

powder_button = pygame.rect.Rect(10,710,100,30)
powder_text= font.render("Powder",True,(0,0,0))
water_button = pygame.rect.Rect(120,710,100,30)
water_text = font.render("Liquid",True,(0,0,0))

fps = 30

mouse_down = False

draw_type=powder

while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down=True
            
            pos = pygame.mouse.get_pos()
            if powder_button.collidepoint(pos):
                draw_type=powder
            elif water_button.collidepoint(pos):
                draw_type=liquid
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=False
    
    if mouse_down:
        mouse_pos = pygame.mouse.get_pos()
        i_x,i_y=universe.get_index(mouse_pos)
        if i_x != -1:
            universe.grid[i_y][i_x] = draw_type(i_x,i_y)


    # clear frame
    screen.fill("white")
    
    universe.draw(screen)
    
    pygame.draw.rect(screen,(203,189,147),powder_button)
    screen.blit(powder_text,(15,715))
    pygame.draw.rect(screen,(13,87,166),water_button)
    screen.blit(water_text,(125,715))
    
    universe.tick()


    pygame.display.flip()
    pygame.display.set_caption(f"fps: {clock.get_fps():.2f}")

    clock.tick(fps)