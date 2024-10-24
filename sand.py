# This file is not meant to be run.
# This file has all of the code to run the game.
import pygame
from copy import deepcopy,copy
from random import randint

def rand_dir():
    return (-1,1)[randint(0,1)]

class empty:
    # Air
    def __init__(self,x,y):
        self.color=(0,0,0)    # The color to display
        self.density = -1     # The density of the cell
        self.x, self.y = x,y  # Save position
        self.clock = 0        # Current cycle. Used to ensure the pixel is checked only once per frame.
        self.name  = "air"
        self.temp=21
        self.burning=False
        self.burn_ticks = 0
        self.burn_max = 10
        self.heat_transfer=0
    def tick(self):
        if self.y > 0 \
            and universe.grid[self.y-1][self.x].density == -1\
                and universe.grid[self.y-1][self.x].temp < self.temp:
                    self.swap(0,-1)
    def tick_temp(self):
        #cool
        self.temp += 0.01 * -1 if self.temp > 21 else 1
        # pass
    def swap(self,dx,dy):
        global universe
        
        self.clock = universe.cycle
        temp=deepcopy(universe.grid[self.y+dy][self.x+dx]) # store before swapping
        temp.y,temp.x=self.y,self.x
        copy = deepcopy(self)
        copy.y+=dy
        copy.x+=dx
        universe.grid[self.y+dy][self.x+dx] = copy
        universe.grid[self.y][self.x] = temp
        
        universe.active.add((self.x+dx,self.y+dy))
        
    def burn_neighbors(self):
        global universe
        
        if self.x > 0:
            universe.grid[self.y][self.x-1].burning=True
        if self.x < universe.height-1:
            universe.grid[self.y][self.x+1].burning=True
        
        if self.y > 0:
            universe.grid[self.y-1][self.x].burning=True
        if self.y < universe.height-1:
            universe.grid[self.y+1][self.x].burning=True

class universe_class:
    def __init__(self,width,height,pixel_width,pixel_height):
        self.grid = [[empty(x,y) for x in range(width)] for y in range(height)]
        self.cycle=0
        self.width,self.height = width,height
        
        cell_width, cell_height = pixel_width//width,pixel_height//height
        
        self.rects = [[pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height) for x in range(width)] for y in range(height)]
        
        self.active=set()
        
    def tick(self):
        # for y in range(self.height):
        #     for x in range(self.width):
        for x,y in copy(self.active):
            if self.grid[y][x].clock < self.cycle:
                
                if self.grid[y][x].density == -1 and abs(self.grid[y][x].temp-21) < 1.5:
                    self.active.remove((x,y))
                    continue
                
                self.grid[y][x].tick()
                self.grid[y][x].tick_temp()
                # dx, dy, check value, max value
                for dx,dy,cv,mv in zip((-1,1,0,0),(0,0,-1,1),(x,x,y,y),(0,self.width-1,0,self.height-1)):
                    if cv != mv:
                        # if self.grid[y+dy][x+dx].density == -1:
                        #     self.grid[y+dy][x+dx].temp+= 0.01*(21-self.grid[y+dy][x+dx].temp)
                        t1,t2 = self.grid[y+dy][x+dx].temp,self.grid[y][x].temp
                        t1,t2 = self.balance_heat(t1,t2,0.01 if self.grid[y+dy][x+dx].density == -1 else 0.4)
                        self.grid[y+dy][x+dx].temp,self.grid[y][x].temp = t1,t2
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

    def set_cell(self,x,y,value):
        self.grid[y][x] = value
        self.active.add((x,y))

    def balance_heat(self,temp1,temp2,diffusion_rate=0.15):
        temp_diff = temp2-temp1
        temp_diff*=diffusion_rate
        return temp1+temp_diff,temp2-temp_diff

# The variable used by every cell
universe = universe_class(70,70,700,700)

class powder(empty):
    def __init__(self,x,y,density=10,color=(203,189,147)):
        # For what these values are, see empty class
        self.color=color
        self.density=density
        self.x, self.y = x,y
        self.clock = 0
        self.name = "powder"
        self.temp=21
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
        self.temp=21
        self.burning=False
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
    def tick_temp(self):
        if self.temp >= 100:
            universe.grid[self.y][self.x] = gas(self.x,self.y)
            universe.grid[self.y][self.x].temp=max(self.temp,150)
        else:
            if self.burning:
                self.burning=False
                self.temp += 0.1 * (110 - self.temp)
            else:
                self.temp += 0.05 * (21 - self.temp)

class fire(empty):
    def __init__(self,x,y):
        # For what these values are, see empty class
        self.density=0
        self.x, self.y = x,y
        self.clock = 0
        self.name = "liquid"
        self.temp=500
        self.ticks    = 0              # How many ticks it has been alive
        self.lifespan = randint(5,35)  # How long it should last
    def tick(self):
        self.burn_neighbors()
        
        self.ticks+=1
        if self.ticks >= self.lifespan:
            universe.grid[self.y][self.x]=empty(self.x,self.y)
        
        dx=rand_dir()
        dy=-1 if self.y > 0 else 0
        
        if self.x == (0,universe.width-1,0)[dx]:
            dx=0
        
        universe.grid[self.y+dy][self.x+dx].temp += 0.2 * (self.temp-universe.grid[self.y+dy][self.x+dx].temp)
        
        if universe.grid[self.y+dy][self.x+dx].density == -1:
            self.swap(dx,dy)
        elif universe.grid[self.y+dy][self.x].density == -1:
            self.swap(0,dy)
        elif universe.grid[self.y][self.x+dx].density == -1:
            self.swap(dx,0)
    def tick_temp(self):
        self.temp += 0.1 * (1000-self.temp)
    
    # random color every time
    @property
    def color(self):
        return (randint(200, 255), randint(50, 150), randint(0, 50))

class gas(empty):
    def __init__(self,x,y,density=1,color=(232//2, 243//2, 255//2)):
        # For what these values are, see empty class
        self.color=color
        self.density=density
        self.x, self.y = x,y
        self.clock = 0
        self.name = "liquid"
        self.temp=150
        self.burning=False
        
    def tick(self):
        dx,dy = rand_dir(),(-1,-1,1)[randint(0,2)]
        if self.x == (0,universe.width-1,0)[dx]:
            dx=0
        if self.y == (0,universe.height-1,0)[dy]:
            dy=0
        self.swap(dx,dy)
    def tick_temp(self):
        if self.temp < 80:
            universe.grid[self.y][self.x] = liquid(self.x,self.y)
            universe.grid[self.y][self.x].temp=self.temp
        if self.burning:
            self.burning=False
            self.temp += 0.1 * (500-self.temp)

# Subclasses
class oil(liquid):
    def __init__(self, x, y, density=4, color=(64, 31, 0)):
        super().__init__(x, y, density, color)
        self.burn_max = randint(50,100)
        self.burn_ticks=0
        self.burning=False
        self.name="oil"
    def tick(self):
        if self.burning:
            self.burn_ticks+=1
            if self.y > 0 and universe.grid[self.y-1][self.x].density == -1 and randint(1,5) == 2:
                universe.set_cell(self.x,self.y-1,fire(self.x,self.y-1))
            if self.burn_ticks >= self.burn_max:
                universe.grid[self.y][self.x]=fire(self.x,self.y)
                return
            self.burn_neighbors()

        super().tick()
    def tick_temp(self):
        if self.burning:
            self.temp+= 0.5 * (500-self.temp)