"""
Programmeerimise projekt
"""

import pygame
import sys
from random import shuffle
sys.setrecursionlimit(10000000) # et suurte laburüntide genereerimisel veateadet ei tekiks

delay = 20 # kaua ootame iga "liigutuse" järel
squareSize = 40 # ühe ruudu suurus
screenWidth, screenHeight = (640, 480) # ekraani suurus
width, height = (screenWidth // squareSize, screenHeight // squareSize) # mitu rida-veergu

# Värvid pygame jaoks
black = (0,0,0)
white = (255,255,255)
blue = (30,130,150)
yellow = (255,255,0)
# ilmakaared 
N, S, E, W = (0, -1), (0, 1), (1, 0), (-1, 0)

def setColor(cell, color):
    """ Seab ruudule uue taustavärvi """
    global squareSize, screen, delay
    x, y = cell
    pygame.draw.rect(screen, color, (x * squareSize+2, y * squareSize+2, 
                                    squareSize-2, squareSize-2))
    pygame.time.delay(delay)
    pygame.display.flip()
    
def removeWall(cell, side):
    """ Kustutab vastava seina ruudu vastavast küljest joonistades valge joone paksusega 2 """
    global squareSize, screen
    x, y = cell
    if side == N:
        pygame.draw.line(screen, white, (x*squareSize, y*squareSize),
                                        ((x+1)*squareSize, y*squareSize), 2)
    elif side == S:
        pygame.draw.line(screen, white, (x*squareSize, (y+1)*squareSize),
                                        ((x+1)*squareSize, (y+1)*squareSize), 2)
    elif side == E:
        pygame.draw.line(screen, white, ((x+1)*squareSize, y*squareSize),
                                        ((x+1)*squareSize, (y+1)*squareSize), 2)
    elif side == W:
        pygame.draw.line(screen, white, (x*squareSize, y*squareSize),
                                        (x*squareSize, (y+1)*squareSize), 2)
    pygame.time.delay(delay)
    pygame.display.flip()

def shuffledDirections():
    " Tagastab suvalisse järjestusesse viidud suunad "
    dirs = [N, S, E, W]
    shuffle(dirs)
    return dirs

def neighbor(cell, direction):
    " Tagastab ruudu naabri parameetriks antud suunas "
    x, y = cell
    dx, dy = direction
    return (x + dx, y + dy)

def inBounds(cell):
    " Tagastab True, kui ruut on piirides (ekraanil) "
    global width, height
    x, y = cell
    return x >= 0 and y >= 0 and x < width and y < height
    
def recurse(cell, visited):
    # märgime, et oleme siin olnud
    visited.add(cell) 
    # seame ruudu värvi siniseks
    setColor(cell, blue) 
    for direction in shuffledDirections():
        # valime suvalise seina
        nx, ny = neighbor(cell, direction)
        if inBounds((nx, ny)) and not (nx, ny) in visited:
            # kui pole siin käinud, lammutame seina ning liigume sinna
            removeWall(cell, direction)
            recurse((nx, ny), visited)
    setColor(cell, white)
    
print("Yeee! Yeee! Yeee!")
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
background = pygame.Surface(screen.get_size())
while True:
    background.fill(yellow)
    screen.blit(background, (0,0))
    # joonistame algse ruudustiku
    for row in range(height+1):
        # ekraanile musta värvi joon (ülalt alla) paksusega 2
        pygame.draw.line(screen, black, (0, row * squareSize), 
                                        (screenWidth, row * squareSize), 2)
    for col in range(width+1):
        # ekraanile musta värvi joon (ülalt alla) paksusega 2
        pygame.draw.line(screen, black, (col * squareSize, 0), 
                                        (col * squareSize, screenHeight), 2)


    # kutsume välja rekursiooni (alguses visited hulk tühi)
    recurse((0, 0), set())
    # kontrollime, ega ekraani üritatud kinni panna
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    pygame.time.delay(2000)
