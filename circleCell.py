import pygame
import os
from math import sin, cos, tan, radians, pi
from random import randint


class Cell:
    def __init__(self, layer, direction, radius, slices, layers, DISPLAY=None):
        self.layer = layer
        self.angle = 360 / slices * direction

        self.radius = layer / layers * radius 
        self.layers = layers

        self.slices = slices
        self.direction = direction
        
        self.x = layer - 1
        self.y = direction - 1
        
        self.DISPLAY = DISPLAY
        self.VISITED_COLOUR = (255,0,255)
        self.BASE_COLOUR = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.visited = False
        self.walls = [True for b in range(4)]
        self.previous = None
    
    def draw(self, width, height, RADIUS):

        x = cos(radians(self.angle)) * self.radius + 0.5 * width
        y = sin(radians(self.angle)) * self.radius + 0.5 * height

        colour = self.VISITED_COLOUR if self.visited else self.BASE_COLOUR

        wallWidth = 2

        
        
        if self.walls[0]:
            
            wall_x1 = round(cos(radians(360 / self.slices * (self.direction + .5))) * self.radius + 0.5 * width, 2)
            wall_y1 = round(sin(radians(360 / self.slices * (self.direction + .5))) * self.radius + 0.5 * height, 2)

            wall_x2 = round(cos(radians(360 / self.slices * (self.direction - .5))) * self.radius + 0.5 * width, 2)
            wall_y2 = round(sin(radians(360 / self.slices * (self.direction - .5))) * self.radius + 0.5 * height, 2)

            pygame.draw.line(self.DISPLAY, colour, (wall_x1, wall_y1), (wall_x2, wall_y2), wallWidth)
        
        if self.walls[1]:

            wall_x1 = round(cos(radians(360 / self.slices * (self.direction + .5))) * self.radius + 0.5 * width, 2)
            wall_y1 = round(sin(radians(360 / self.slices * (self.direction + .5))) * self.radius + 0.5 * height, 2)

            new_r = (self.layer - 1) / self.layers * RADIUS

            wall_x2 = round(cos(radians(360 / self.slices * (self.direction + .5))) * new_r + 0.5 * width, 2)
            wall_y2 = round(sin(radians(360 / self.slices * (self.direction + .5))) * new_r + 0.5 * height, 2)

            pygame.draw.line(self.DISPLAY, colour, (wall_x1, wall_y1), (wall_x2, wall_y2), wallWidth)

        
        if self.walls[2]:

            new_r = (self.layer - 1) / self.layers * RADIUS

            wall_x1 = round(cos(radians(360 / self.slices * (self.direction + .5))) * new_r + 0.5 * width, 2)
            wall_y1 = round(sin(radians(360 / self.slices * (self.direction + .5))) * new_r + 0.5 * height, 2)

            wall_x2 = round(cos(radians(360 / self.slices * (self.direction - .5))) * new_r + 0.5 * width, 2)
            wall_y2 = round(sin(radians(360 / self.slices * (self.direction - .5))) * new_r + 0.5 * height, 2)

            pygame.draw.line(self.DISPLAY, colour, (wall_x1, wall_y1), (wall_x2, wall_y2), wallWidth)

        if self.walls[3]:


            wall_x1 = round(cos(radians(360 / self.slices * (self.direction - .5))) * self.radius + 0.5 * width, 2)
            wall_y1 = round(sin(radians(360 / self.slices * (self.direction - .5))) * self.radius + 0.5 * height, 2)

            new_r = (self.layer - 1) / self.layers * RADIUS

            wall_x2 = round(cos(radians(360 / self.slices * (self.direction - .5))) * new_r + 0.5 * width, 2)
            wall_y2 = round(sin(radians(360 / self.slices * (self.direction - .5))) * new_r + 0.5 * height, 2)

            pygame.draw.line(self.DISPLAY, colour, (wall_x1, wall_y1), (wall_x2, wall_y2), wallWidth)

    
    def checkNeighbours(self, grid, rng):
        neighbours = []

        if self.x+1 in range(len(grid[0])):
            top = grid[self.y][self.x+1]
            if not top.visited or randint(0, 100) < rng:
                neighbours.append(top)

        y = (self.y + 1) % self.slices
        right = grid[y][self.x]
        if not right.visited or randint(0, 100) < rng:
            neighbours.append(right)

        if self.x-1 > 0:
            bottom = grid[self.y][self.x-1]
            if not bottom.visited or randint(0, 100) < rng:
                neighbours.append(bottom)

        y = (self.y - 1) % self.slices
        left = grid[y][self.x]
        if not left.visited or randint(0, 100) < rng:
            neighbours.append(left)
        
        
        self.neighbours = neighbours
    
    def highlight(self, colour, r, w, h):

        wall_x1 = round(cos(radians(360 / self.slices * (self.direction + .5))) * self.radius + 0.5 * w, 2)
        wall_y1 = round(sin(radians(360 / self.slices * (self.direction + .5))) * self.radius + 0.5 * h, 2)

        wall_x2 = round(cos(radians(360 / self.slices * (self.direction - .5))) * self.radius + 0.5 * w, 2)
        wall_y2 = round(sin(radians(360 / self.slices * (self.direction - .5))) * self.radius + 0.5 * h, 2)

        new_r = (self.layer - 1) / self.layers * r

        wall_x3 = round(cos(radians(360 / self.slices * (self.direction + .5))) * new_r + 0.5 * w, 2)
        wall_y3 = round(sin(radians(360 / self.slices * (self.direction + .5))) * new_r + 0.5 * h, 2)

        wall_x4 = round(cos(radians(360 / self.slices * (self.direction - .5))) * new_r + 0.5 * w, 2)
        wall_y4 = round(sin(radians(360 / self.slices * (self.direction - .5))) * new_r + 0.5 * h, 2)

        if self.direction == self.slices:
            colour = (255, 0, 0)

        pygame.draw.polygon(self.DISPLAY, colour, [(wall_x2, wall_y2), (wall_x1, wall_y1), (wall_x3, wall_y3), (wall_x4, wall_y4), ])