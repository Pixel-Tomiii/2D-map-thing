import pygame
from enum import IntEnum
import random
import time

TILE_SIZE = 4

colors = [0, (50, 50, 50), (77, 171, 56), (49, 99, 153)]


class Tile(IntEnum):
    STONE = 1
    GRASS = 2
    WATER = 3


class Viewport():
    def __init__(self, world, center, width, height):
        self.world = world
        self.center = center
        self.width = width
        self.height = height

    def translate(self, dx, dy):
        x, y = self.center
        if x + dx < self.width // 2 or x + dx >= len(world[0]) - (self.width // 2):
            return False
        if y + dy < self.height // 2 or y + dy >= len(world) - (self.height // 2):
            return False
        
        self.center = (self.center[0] + dx, self.center[1] + dy)
        return True

    def get_visible(self):
        x = self.center[0]
        y = self.center[1]

        half_width = self.width // 2
        half_height = self.height // 2

        start_x = x - half_width 
        start_y = y - half_width

        if start_x < 0:
            start_x = 0
        elif start_x >= len(self.world[0]) - self.width:
            start_x = len(self.world[0]) - self.width

        if start_y < 0:
            start_y = 0
        elif start_y >= len(self.world) - self.height:
            start_y = len(self.world) - self.height

        view = []
        for y in range(start_y, start_y + self.height):
            view.append(self.world[y][start_x:start_x+self.width])
        return view
                

def load_world(name):
    world_data = open(name + ".map", "r")
    world = []
    for row in world_data:
        row = row.rstrip()
        line = list(map(int, row.split(",")))
        world.append(line)
    return world



# Initalise window.
pygame.init()
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True

width = window.get_width()
height = window.get_height()

# World gen
world = [[random.randint(1, 3) for _ in range(1000)] for __ in range(1000)]
world_view = Viewport(world, (len(world[0]) // 2, len(world) // 2), (width // TILE_SIZE) + 1, (height // TILE_SIZE) + 1)


# Framerate tracking.
last_update = time.time()
half_second = 0.5
font = pygame.font.SysFont("Arial", 20)
last_frames = 0
frames = 0
frame_render = font.render(f"{last_frames * 2}", False, (255, 255, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_event = pygame.event.Event(pygame.QUIT)
                pygame.event.post(quit_event)

            elif event.key == pygame.K_w:
                world_view.translate(0, -1)

            elif event.key == pygame.K_a:
                world_view.translate(-1, 0)

            elif event.key == pygame.K_s:
                world_view.translate(0, 1)

            elif event.key == pygame.K_d:
                world_view.translate(1, 0)

    else:
        now = time.time()
        if now >= last_update + half_second:
            window.fill((0, 0, 0))
            last_update += half_second
            frame_render = font.render(f"{last_frames * 2}", False, (255, 255, 255))
            last_frames = frames
            frames = 0
            
        frames += 1
        world_data = world_view.get_visible()
        world_render = pygame.Surface((world_view.width * TILE_SIZE, world_view.height * TILE_SIZE))
        for y, row in enumerate(world_data):
            for x, value in enumerate(row):
                pygame.draw.rect(world_render, colors[value], pygame.rect.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        window.blit(world_render, ((width // 2) - (world_render.get_width() // 2), (height // 2) - (world_render.get_height() // 2)))
        
        window.blit(frame_render, (0, 0))
        pygame.display.update()

    continue
        

pygame.quit()
