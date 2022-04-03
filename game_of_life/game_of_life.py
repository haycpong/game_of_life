"""Class GameofLife
This file contains the game logic.
Function
    __init__()
    run()
    draw_grid()
    update_grid()
    update_cell()
"""

import pygame
import numpy as np

class GameofLife:
    """Game Rules:
    1. If a living cell has 0 or 1 neighbour, then it will die.
    2. If a living cell has 4, 5, 6, 7 or 8 neighbours, then it will die.
    3. If a dead cell has 3 neightbours, reproduction will happen.
    """
    def __init__(self, surface, width=640 , height=480, scale=20, offset=1, active_color=(255, 255, 255), inactive_color=(10, 10, 10)):
        """Define window width and height, scale, offset, active_color"""
        self.surface = surface
        self.width = width
        self.height = height
        self.scale = scale
        self.offset = offset
        self.active_color = active_color
        self.inactive_color = inactive_color

        self.columns = int(height / scale)
        self.rows = int(width / scale)

        self.regenerate() 
        print ("screen(%d,%d),scale(%d), grid(%d,%d)" % (self.width, self.height, scale, self.rows, self.columns))

    def run(self):
        """"Update and redraw the current grid state"""
        self.draw_grid()
        self.update_grid()

    def draw_grid(self):
        """Drawing the grid"""
        for row in range(self.rows):
            for col in range(self.columns):
                if self.grid[row, col]:
                    pygame.draw.rect(self.surface, self.active_color, [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])
                else:
                    pygame.draw.rect(self.surface, self.inactive_color, [row * self.scale, col * self.scale, self.scale - self.offset, self.scale - self.offset])

    def update_grid(self):
        """Updating the grid"""
        updated_grid = self.grid.copy()
        for row in range(updated_grid.shape[0]):
            for col in range(updated_grid.shape[1]):
                updated_grid[row, col] = self.update_cell(row, col)

        self.grid = updated_grid


    def update_cell(self, x, y):
        """Update single cells"""
        current_state = self.grid[x, y]
        alive_neighbors = 0

        # Get to how many alive neighbors
        for i in range(-1, 2):
            if ((x + i) < 0 or ((x + i) >= self.grid.shape[0])):
                continue
            for j in range(-1, 2):
                if ((y + j) < 0 or (y + j) >= self.grid.shape[1]):
                    continue
                if i == 0 and j == 0:
                        continue
                elif self.grid[x + i, y + j]:
                    alive_neighbors += 1
        # Updating the cell's state
        if current_state and alive_neighbors < 2: #underpopulation
            return False
        elif current_state and (alive_neighbors == 2 or alive_neighbors == 3): 
            return True
        elif current_state and alive_neighbors > 3: #overpopulation
            return False
        elif ~current_state and alive_neighbors == 3: #reproduction
            return True
        else:
            return current_state

    def get_grid_pos(self, x, y):
        """transform mouse(x,y) to grid(x,y)"""
        idx_x = int(x / self.scale)
        idx_y = int(y / self.scale)

        if idx_x >= self.rows: #exceeds x boundary in grid[x,y]
            grid_x = idx_x - 1
        else:
            grid_x = idx_x

        if idx_y >= self.columns: #exceeds y boundary in grid[x,y]
            grid_y = idx_y - 1
        else:
            grid_y = idx_y

        return (grid_x, grid_y)


    def alternate_grid_state(self, x, y):
        self.grid[x, y] = ~self.grid[x, y]

    def set_grid_live(self, x, y):
        self.grid[x,y] = True

    def get_grid_state(self, x, y):
        return self.grid[x,y]

    def regenerate(self):
        """randomly generate population"""
        self.grid = np.random.randint(0, 2, size=(self.rows, self.columns), dtype=bool)

    def clear(self):
        """clear all"""
        self.grid = np.random.randint(0, 1, size=(self.rows, self.columns), dtype=bool)