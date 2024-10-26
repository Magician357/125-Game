# *=============================================================================
#  |   Assignment:  Program 1.2.5:  Shall We Play a Game
#  |       Author:  Zachary Martinez
#  |
#  |  Course Name:  Computer Science Principles
#  |   Instructor:  Mr. Virak
#  |     Due Date:  10/25/2024 at 11:59 PM
#  |
#  |  Description:  Simulate a falling sand environment with a variety
#  |                of elements that behave in different ways. Powder 
#  |                (1 element) tries to fall down, or slide          
#  |                diagonally. Liquid (2 elements) try to fall down, 
#  |                and then slide from side to side. Gas (1 element) 
#  |                moves in any direction randomly, with a bias      
#  |                toward moving upward. Solid (2 elements) does not 
#  |                move. Fire moves diagonally upward, and freeze    
#  |                simply turns into an empty cell at -50 degrees.   
#  |                There is also a simply temperature simulation,    
#  |                where neighboring cells transfer heat. Things on  
#  |                fire heat up, while most other elements attempt to 
#  |                cool to room temperature (22 degrees).
#  |
#  |     Language:  Python 3
#  | Ex. Packages:  bresenham    - https://pypi.org/project/bresenham/
#  |                copy, random - part of python
#  |                pygame       - https://pygame.org
#  |                
#  | Deficiencies:  Simulation parameters and temperature functions could
#  |                be changed to be more reflective of real life. The 
#  |                simulation may slow down if large amounts of cells 
#  |                are activated (eg air temp very high/low, lots of 
#  |                things on fire)
#  *===========================================================================*

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

powder_button = pygame.rect.Rect(10,720,100,30)
powder_text= font.render("Powder",True,(0,0,0))
water_button = pygame.rect.Rect(120,720,100,30)
water_text = font.render("Liquid",True,(0,0,0))
fire_button = pygame.rect.Rect(230,720,100,30)
fire_text = font.render("Fire",True,(0,0,0))
oil_button = pygame.rect.Rect(340,720,100,30)
oil_text = font.render("Oil",True,(0,0,0))
freeze_button = pygame.rect.Rect(450,720,100,30)
freeze_text = font.render("Freeze",True,(0,0,0))
wood_button = pygame.rect.Rect(560,720,100,30)
wood_text = font.render("Wood",True,(0,0,0))

empty_button = pygame.rect.Rect(10,680,100,30)
empty_text = font.render("Empty",True,(255,255,255))

select_marker = pygame.rect.Rect(8,678,104,34)

selected_rect = empty_button

help_text = font.render("Click one of the buttons to select an element",True,(0,0,0))
help_text_2 = font.render("Press space to pause. Press +/- to change cursor size. While paused, press R to restart.",True,(0,0,0))

paused_text = font.render("Paused",True,(255,255,255))

fps = 30

mouse_down = False

draw_type=empty
override = False

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
                selected_rect = powder_button
                override=False
            elif water_button.collidepoint(mouse_pos):
                draw_type=liquid
                selected_rect = water_button
                override=False
            elif fire_button.collidepoint(mouse_pos):
                draw_type=fire
                selected_rect = fire_button
                override=False
            elif oil_button.collidepoint(mouse_pos):
                draw_type=oil
                selected_rect = oil_button
                override=False
            elif freeze_button.collidepoint(mouse_pos):
                draw_type=freeze
                selected_rect = freeze_button
                override=False
            elif wood_button.collidepoint(mouse_pos):
                draw_type=wood
                selected_rect = wood_button
                override=False
            elif empty_button.collidepoint(mouse_pos):
                draw_type=empty
                selected_rect = empty_button
                override=True
            select_marker.x,select_marker.y = selected_rect.x-2,selected_rect.y-2
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down=False
        elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_EQUALS]:
                draw_size+=1
            elif pressed[pygame.K_MINUS]:
                draw_size = max(0,draw_size-1)
            if pressed[pygame.K_SPACE]:
                simulating=not simulating
            elif pressed[pygame.K_r] and not simulating:
                universe.reset()
                simulating=True
    
    if mouse_down:
        if i_x != -1:
        # and universe.grid[i_y][i_x].density == -1:
            # universe.set_cell(i_x,i_y,draw_type(i_x,i_y))
            for c_x,c_y in bresenham(p_x if p_x != -1 else i_x,p_y if p_y != -1 else i_y,i_x,i_y):
                universe.set_box(c_x,c_y,draw_size,draw_type,override)


    # clear frame
    screen.fill("white")
    
    pygame.draw.rect(screen,(10,10,10),select_marker)
    
    pygame.draw.rect(screen,(203,189,147),powder_button)
    screen.blit(powder_text,(15,725))
    pygame.draw.rect(screen,(13,87,166),water_button)
    screen.blit(water_text,(125,725))
    pygame.draw.rect(screen,(227,100,25),fire_button)
    screen.blit(fire_text,(235,725))
    pygame.draw.rect(screen,(64, 31, 0),oil_button)
    screen.blit(oil_text,(345,725))
    pygame.draw.rect(screen,(25, 100, 227),freeze_button)
    screen.blit(freeze_text,(455,725))
    pygame.draw.rect(screen,(71, 61, 31),wood_button)
    screen.blit(wood_text,(565,725))
    
    pygame.draw.rect(screen,(0, 0, 0),empty_button)
    screen.blit(empty_text,(15,685))
    
    screen.blit(help_text,(120,685))
    screen.blit(help_text_2,(15,765))
    
    universe.draw(screen)
    if simulating:
        universe.tick()
    else:
        screen.blit(paused_text,(350,350))
    
    if i_x != -1:
        temp_surface=pygame.surface.Surface((700,700),pygame.SRCALPHA)
        for dx in range(-draw_size,draw_size+1):
            for dy in range(-draw_size,draw_size+1):
                if i_x+dx >= universe.width or i_x+dx < 0 or i_y+dy >= universe.height or i_y+dy < 0:
                    continue
                pygame.draw.rect(temp_surface,(50,50,50,100),universe.rects[i_y+dy][i_x+dx])
        screen.blit(temp_surface,(0,0))


    pygame.display.flip()
    
    pygame.display.set_caption(f"fps: {clock.get_fps():.2f}"+"    "
        +f"cell info: ({i_x},{i_y}), "+
            f"ID {universe.grid[i_y][i_x].name}{universe.grid[i_y][i_x].id}, "+ 
                f"{universe.grid[i_y][i_x].temp:.2f} degrees, " +
                    f"{'Active' if (i_x,i_y) in universe.active else 'Inactive'}, "+ 
                        f"Burning: {universe.grid[i_y][i_x].burning}")

    clock.tick(fps)