# This file is not meant to be run.
# This file has all of the code to run the game.
import pygame
from copy import deepcopy
from random import randint

def rand_dir():
    return (-1,1)[randint(0,1)]

class empty:
    # Air
    def __init__(self,x,y):
        self.color=(0,0,0)    # The color to display
        self.density = -1     # The density of the cell
        self.burn_time=-1     # The time when it started to burn. -1 if not burning.
        self.x, self.y = x,y  # Save position
        self.clock = 0        # Current cycle. Used to ensure the pixel is checked only once per frame.
        self.name  = "air"
    def tick(self):
        # Placeholder for movement
        pass
    def swap(self,dx,dy):
        global universe
        
        self.clock = universe.cycle
        temp=deepcopy(universe[self.y+dy][self.x+dx]) # store before swapping
        temp.y,temp.x=self.y,self.x
        copy = deepcopy(self)
        copy.y+=dy
        copy.x+=dx
        universe.grid[self.y+dy][self.x+dx] = copy
        universe.grid[self.y][self.x] = temp

class universe_class:
    def __init__(self,width,height,pixel_width,pixel_height):
        self.grid = [[empty(x,y) for x in range(width)] for y in range(height)]
        self.cycle=0
        self.width,self.height = width,height
        
        cell_width, cell_height = pixel_width//width,pixel_height//height
        
        self.rects = [[pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height) for x in range(width)] for y in range(height)]
        
    def tick(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].clock < self.cycle:
                    self.grid[y][x].tick()
        self.cycle+=1
    
    def draw(self,screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen,self.grid[y][x].color,self.rects[y][x])
    
    def get_index(self,pos):
        # takes in position on screen and returns what cell
        for y in range(self.height):
            for x in range(self.width):
                if self.rects[y][x].collidepoint(pos):
                    return x,y
        return -1,-1
    
    def __getitem__(self,y):
        return self.grid[y]

# The variable used by every cell
universe = universe_class(50,50,700,700)

class powder(empty):
    def __init__(self,x,y,density=10,color=(203,189,147)):
        # For what these values are, see empty class
        self.color=color
        self.density=density
        self.x, self.y = x,y
        self.clock = 0
        self.name = "powder"
    def tick(self):
        global universe
        
        # Check if on bottom
        if self.y >= universe.height-1:
            self.y = universe.height # just to make sure
            return

        # Check below
        if universe.grid[self.y+1][self.x].density < self.density:
            self.swap(0,1)
            return
        
        dir = rand_dir()
        # This is a little complicated
        # But it just checks if the direction chosen goes out of bounds
        if self.x == (0,universe.width-1,0)[dir]:
            return
        # Check diagonal
        if universe.grid[self.y+1][self.x+dir].density < self.density:
            self.swap(dir,1)
            return

class liquid(empty):
    def __init__(self,x,y,density=5,color=(13,87,166)):
        # For what these values are, see empty class
        self.color=color
        self.density=density
        self.x, self.y = x,y
        self.clock = 0
        self.name = "liquid"
    def tick(self):
        dir = rand_dir()
        
        if self.y < universe.height-1 and universe.grid[self.y+1][self.x].density < self.density:
            self.swap(0,1)
            return
        else:
            # Move to side
            if not self.x == (0,universe.width-1,0)[dir] and universe.grid[self.y][self.x+dir].density < self.density:
                # if not self.x == (0,universe.width-2,0)[dir] and universe.grid[self.y][self.x+dir*2].density < self.density: 
                    # self.swap(dir*2,0)
                # else:
                self.swap(dir,0)
            return