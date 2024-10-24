import pygame
from sand import *
# NOTE: You must install this file (using pip)
from bresenham import bresenham
# All this is used for is to draw lines

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
freeze_button = pygame.rect.Rect(450,710,100,30)
freeze_text = font.render("Freeze",True,(0,0,0))
wood_button = pygame.rect.Rect(560,710,100,30)
wood_text = font.render("Wood",True,(0,0,0))    

fps = 30

mouse_down = False

draw_type=wood

draw_size=0

simulating = True

i_x,i_y=0,0
p_x,p_y=0,0

while running:
    mouse_pos = pygame.mouse.get_pos()
    p_x,p_y=i_x,i_y
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
            elif freeze_button.collidepoint(mouse_pos):
                draw_type=freeze
            elif wood_button.collidepoint(mouse_pos):
                draw_type=wood
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=False
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_EQUALS]:
                draw_size+=1
            elif pressed[pygame.K_MINUS]:
                draw_size = min(0,draw_size)
            if pressed[pygame.K_SPACE]:
                simulating=not simulating
    
    if mouse_down:
        if i_x != -1 and universe.grid[i_y][i_x].density == -1:
            # universe.set_cell(i_x,i_y,draw_type(i_x,i_y))
            for c_x,c_y in bresenham(p_x if p_x != -1 else i_x,p_y if p_y != -1 else i_y,i_x,i_y):
                universe.set_box(c_x,c_y,draw_size,draw_type,False)


    # clear frame
    screen.fill("white")
    
    pygame.draw.rect(screen,(203,189,147),powder_button)
    screen.blit(powder_text,(15,715))
    pygame.draw.rect(screen,(13,87,166),water_button)
    screen.blit(water_text,(125,715))
    pygame.draw.rect(screen,(227,100,25),fire_button)
    screen.blit(fire_text,(235,715))
    pygame.draw.rect(screen,(64, 31, 0),oil_button)
    screen.blit(oil_text,(345,715))
    pygame.draw.rect(screen,(25, 100, 227),freeze_button)
    screen.blit(freeze_text,(455,715))
    pygame.draw.rect(screen,(71, 61, 31),wood_button)
    screen.blit(wood_text,(565,715))
    
    if simulating:
        universe.tick()
    universe.draw(screen)
    
    pygame.draw.rect(screen,(50,50,50),universe.rects[i_y][i_x])


    pygame.display.flip()
    pygame.display.set_caption(f"fps: {clock.get_fps():.2f}     cell info: ({i_x},{i_y}), {universe.grid[i_y][i_x].name}, {universe.grid[i_y][i_x].temp:.2f} degrees, {'Active' if (i_x,i_y) in universe.active else 'Inactive'}")

    clock.tick(fps)