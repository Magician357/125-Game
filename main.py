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
fire_button = pygame.rect.Rect(230,710,100,30)
fire_text = font.render("Fire",True,(0,0,0))
oil_button = pygame.rect.Rect(340,710,100,30)
oil_text = font.render("Oil",True,(0,0,0))

fps = 30

mouse_down = False

draw_type=liquid

while running:
    mouse_pos = pygame.mouse.get_pos()
    i_x,i_y=universe.get_index(mouse_pos)
    
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down=True
            if powder_button.collidepoint(mouse_pos):
                draw_type=powder
            elif water_button.collidepoint(mouse_pos):
                draw_type=liquid
            elif fire_button.collidepoint(mouse_pos):
                draw_type=fire
            elif oil_button.collidepoint(mouse_pos):
                draw_type=oil
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=False
    
    if mouse_down:
        if i_x != -1 and universe.grid[i_y][i_x].density == -1:
            universe.set_cell(i_x,i_y,draw_type(i_x,i_y))


    # clear frame
    screen.fill("white")
    
    universe.draw(screen)
    
    pygame.draw.rect(screen,(203,189,147),powder_button)
    screen.blit(powder_text,(15,715))
    pygame.draw.rect(screen,(13,87,166),water_button)
    screen.blit(water_text,(125,715))
    pygame.draw.rect(screen,(227,100,25),fire_button)
    screen.blit(fire_text,(235,715))
    pygame.draw.rect(screen,(64, 31, 0),oil_button)
    screen.blit(oil_text,(345,715))
    
    universe.tick()


    pygame.display.flip()
    pygame.display.set_caption(f"fps: {clock.get_fps():.2f}     cell info: ({i_x},{i_y}), {universe.grid[i_y][i_x].name}, {universe.grid[i_y][i_x].temp:.2f} degrees")

    clock.tick(fps)