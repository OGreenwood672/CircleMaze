import pygame

from random import choice
from math import pi

import json

from circleCell import Cell

def createCircle(display, CircleObject):
    circle = []
    for angle in range(CircleObject["slices"]):
        sector = []
        for layer in range(CircleObject["layers"]):
            sector.append(Cell(layer + 1, angle + 1, CircleObject["radius"], CircleObject["slices"], CircleObject["layers"], display))
        circle.append(sector)
    return circle

def draw(display, circle, r, w, h):
    display.fill((0, 0, 0))
    pygame.draw.circle(display,(255, 255, 255), (w // 2, h // 2), r)
    for sector in circle:
        for cell in sector:
            cell.draw(w, h, r)

def serialize(circle, CircleObject):

    obj = []

    obj.append({"attr": json.dumps(CircleObject)})

    for sector in circle:
        sectors = []
        for cell in sector:
            sectors.append({
                "x": cell.x,
                "y": cell.y,
                "walls": json.dumps(cell.walls)
            })
        obj.append(json.dumps(sectors))

    return obj

def removeWalls(cell, cell2, slices):

    if cell.x - cell2.x == 1:
        cell.walls[2] = False
        cell2.walls[0] = False

    elif cell.x - cell2.x == -1:
        cell.walls[0] = False
        cell2.walls[2] = False

    elif cell.y - cell2.y == 1:
        cell.walls[3] = False
        cell2.walls[1] = False

    elif cell.y - cell2.y == -1:
        cell.walls[1] = False
        cell2.walls[3] = False
    
    elif cell.y - cell2.y == -(slices-1):
        cell.walls[3] = False
        cell2.walls[1] = False
        
    elif cell.y - cell2.y == (slices-1):
        cell.walls[1] = False
        cell2.walls[3] = False


 # DEPTH-FIRST SEARCH using a Recursive backtracker
def main(visual=True, resp=False, rng=2): # rng( 0-12 (%))


    CircleObject = {
        "width": 800,
        "height": 800,
        "radius": 350,
        "slices": 40,
        "layers": 30,
    }

    if visual:
        pygame.init()
        display = pygame.display.set_mode((CircleObject["width"], CircleObject["height"]))
        pygame.display.set_caption('Maze Generator [circle]')
    else:
        display = None


    circle = createCircle(display, CircleObject)

    circle[0][0].visited = True
    stack = [circle[0][0]]


    while stack:
        
        current = stack.pop()
        current.checkNeighbours(circle, rng)


        if visual:

            draw(
                display,
                circle,
                CircleObject["radius"],
                CircleObject["width"],
                CircleObject["height"]
                )
            
            current.highlight((255, 0, 0), CircleObject["radius"], CircleObject["width"], CircleObject["height"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()


        if current.neighbours:
            stack.append(current)
            neighbour = choice(current.neighbours)
            removeWalls(current, neighbour, CircleObject["slices"])
            neighbour.visited = True
            stack.append(neighbour)
        
    while visual:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        draw(
            display,
            circle,
            CircleObject["radius"],
            CircleObject["width"],
            CircleObject["height"]
            )

        pygame.display.update()
    
    if resp:
        return serialize(circle, CircleObject)


if __name__ == '__main__':
    main()