import pygame
import random


class Game2048:
    def __init__(self):
        self.SCREEN_HEIGHT = 650
        self.SCREEN_WIDTH = 600
        self.GRID_SIZE = 4
        self.LINE_WIDTH = 4
        self.CELL_SIZE = self.SCREEN_WIDTH // self.GRID_SIZE
        self.score = 0
        self.grid = [[0 for e in range(self.GRID_SIZE)] for i in range(self.GRID_SIZE)]
        self.generate_random_tile()
        self.generate_random_tile()
        # self.grid = [[2, 0, 0, 0],
        #              [4, 0, 0, 0],
        #              [4, 0, 0, 0],
        #              [2, 0, 0, 0]]  #
        self.alive = True

        # Pygame Init
        pygame.init()
        self.win = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.alive = False
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.generate_random_tile()

                elif event.key == pygame.K_w:
                    if self.move_up():
                        self.generate_random_tile()
                        print(self.score)

                elif event.key == pygame.K_s:
                    if self.move_down():
                        self.generate_random_tile()
                        print(self.score)

                elif event.key == pygame.K_a:
                    if self.move_left():
                        self.generate_random_tile()
                        print(self.score)

                elif event.key == pygame.K_d:
                    if self.move_right():
                        self.generate_random_tile()
                        print(self.score)

        self.win.fill((255, 255, 255))
        self.draw_grid()
        pygame.display.update()

    def get_empty_tiles(self):
        empty_cells = []
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                if col == 0:
                    empty_cells.append((row_index, col_index))

        return empty_cells

    def generate_random_tile(self):  # broken
        empty_cells = self.get_empty_tiles()
        if len(empty_cells) != 0:
            rand_cell = random.randint(0, len(empty_cells) - 1)
            rand_cell_value = random.randint(1, 10)
            if rand_cell_value < 9:
                self.grid[empty_cells[rand_cell][0]][empty_cells[rand_cell][1]] = 2

            else:
                self.grid[empty_cells[rand_cell][0]][empty_cells[rand_cell][1]] = 4

    def draw_grid(self):
        pygame.draw.rect(self.win, (0, 0, 0),
                         (self.SCREEN_WIDTH - self.LINE_WIDTH, 50, self.LINE_WIDTH, self.SCREEN_HEIGHT - 50))
        pygame.draw.rect(self.win, (0, 0, 0),
                         (0, self.SCREEN_HEIGHT - self.LINE_WIDTH, self.SCREEN_WIDTH, self.LINE_WIDTH))
        for row_index, row in enumerate(self.grid):
            pygame.draw.rect(self.win, (0, 0, 0),
                             (row_index * self.CELL_SIZE, 50, self.LINE_WIDTH, self.SCREEN_HEIGHT - 50))
            pygame.draw.rect(self.win, (0, 0, 0),
                             (0, row_index * self.CELL_SIZE + 50, self.SCREEN_WIDTH, self.LINE_WIDTH))
            for col_index, col in enumerate(row):
                if col != 0:
                    cell_x = (col_index * self.CELL_SIZE) + self.LINE_WIDTH * 1.5
                    cell_y = (row_index * self.CELL_SIZE) + self.LINE_WIDTH * 1.5 + 50
                    pygame.draw.rect(self.win, (255, 255, 125), (
                        cell_x, cell_y, self.CELL_SIZE - (self.LINE_WIDTH * 2), self.CELL_SIZE - (self.LINE_WIDTH * 2)))
                    self.display_text(
                        cell_x + (self.CELL_SIZE // 2), cell_y + (self.CELL_SIZE // 2), col, (0, 0, 0))

    def display_text(self, x, y, msg, color):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 35)
        text = font.render(f'{msg}', False, color)
        text_rect = text.get_rect(center=(x, y))

        self.win.blit(text, text_rect)

    # Testing Function
    def print_grid(self):
        for row in self.grid:
            print(row)
        print('----------------------------------')

    def move_up(self):
        changed = False
        for col_index in range(self.GRID_SIZE):  # Performs Algorithm over every column
            cell_is_merged = [False for x in range(self.GRID_SIZE)]
            for row_index in range(self.GRID_SIZE - 1):  # Skip topmost row
                row_index += 1
                if self.grid[row_index][col_index] != 0:
                    counter = 0
                    for i in range(row_index):  # iterates over every row above row_index
                        row_index_2 = row_index - 1 - i
                        if self.grid[row_index_2][col_index] == 0:
                            counter += 1

                        elif self.grid[row_index][col_index] != self.grid[row_index_2][col_index]:
                            break

                        elif self.grid[row_index][col_index] == self.grid[row_index_2][col_index] and not \
                                cell_is_merged[row_index_2]:
                            counter += 1
                            cell_is_merged[row_index_2] = True
                            self.grid[row_index][col_index] += self.grid[row_index][col_index]
                            self.score += self.grid[row_index][col_index]
                            break

                    if counter != 0:
                        self.grid[row_index - counter][col_index] = self.grid[row_index][col_index]
                        self.grid[row_index][col_index] = 0
                        changed = True
        return changed

    def move_down(self):
        changed = False
        for col_index in range(self.GRID_SIZE):  # Performs Algorithm over every column
            cell_is_merged = [False for x in range(self.GRID_SIZE)]
            for index in range(self.GRID_SIZE - 1):  # Skip bottom row
                row_index = self.GRID_SIZE - 2 - index
                if self.grid[row_index][col_index] != 0:
                    counter = 0
                    for i in range(index + 1):  # iterates over every row above row_index
                        row_index_2 = row_index + 1 + i
                        if self.grid[row_index_2][col_index] == 0:
                            counter += 1

                        elif self.grid[row_index][col_index] != self.grid[row_index_2][col_index]:
                            break

                        elif self.grid[row_index][col_index] == self.grid[row_index_2][col_index] and not \
                                cell_is_merged[row_index_2]:
                            counter += 1
                            cell_is_merged[row_index_2] = True
                            self.grid[row_index][col_index] += self.grid[row_index][col_index]
                            self.score += self.grid[row_index][col_index]
                            break

                    if counter != 0:
                        self.grid[row_index + counter][col_index] = self.grid[row_index][col_index]
                        self.grid[row_index][col_index] = 0
                        changed = True
        return changed

    def move_right(self):
        changed = False
        for row in self.grid:
            cell_is_merged = [False for x in range(self.GRID_SIZE)]
            for index, col in enumerate(row[:self.GRID_SIZE - 1]):  # iterates over every column except for rightmost
                col_index = self.GRID_SIZE - index - 2
                if row[col_index] != 0:
                    counter = 0
                    for i in range(index + 1):  # iterates over every column to the right of col_index
                        col_index_2 = col_index + 1 + i
                        if row[col_index_2] == 0:
                            counter += 1

                        elif row[col_index] != row[col_index_2]:
                            break

                        elif row[col_index] == row[col_index_2] and not cell_is_merged[col_index_2]:
                            counter += 1
                            cell_is_merged[col_index_2] = True
                            row[col_index] += row[col_index]
                            self.score += row[col_index]
                            break

                    if counter != 0:
                        row[col_index + counter] = row[col_index]
                        row[col_index] = 0
                        changed = True
        return changed

    def move_left(self):
        changed = False
        for row in self.grid:
            cell_is_merged = [False for x in range(len(row[1:]))]
            for index, col in enumerate(row[1:]):  # iterates over every column except for leftmost
                if col != 0:
                    col_index = index + 1
                    counter = 0
                    for i in range(col_index):  # iterates over every column to the left of col_index
                        col_index_2 = index - i
                        if row[col_index_2] == 0:
                            counter += 1

                        elif row[col_index] != row[col_index_2]:
                            break

                        elif row[col_index_2] == row[col_index] and not cell_is_merged[col_index_2]:
                            counter += 1
                            cell_is_merged[col_index_2] = True
                            row[col_index] += row[col_index]
                            self.score += row[col_index]
                            break

                    if counter != 0:
                        row[col_index - counter] = row[col_index]
                        row[col_index] = 0
                        changed = True
        return changed

    def no_legal_moves(self):
        # Move_Left
        for row in self.grid:
            for index, col in enumerate(row[1:]):  # iterates over every column except for leftmost
                if col != 0:
                    col_index = index + 1
                    for i in range(col_index):  # iterates over every column to the left of col_index
                        col_index_2 = index - i
                        if row[col_index_2] == 0:
                            return False

                        elif row[col_index] != row[col_index_2]:
                            break

                        elif row[col_index_2] == row[col_index]:
                            return False

        # Move Right
        for row in self.grid:
            for index, col in enumerate(row[:self.GRID_SIZE - 1]):  # iterates over every column except for rightmost
                col_index = self.GRID_SIZE - index - 2
                if row[col_index] != 0:
                    for i in range(index + 1):  # iterates over every column to the right of col_index
                        col_index_2 = col_index + 1 + i
                        if row[col_index_2] == 0:
                            return False

                        elif row[col_index] != row[col_index_2]:
                            break

                        elif row[col_index] == row[col_index_2]:
                            return False

        # Move Up
        for col_index in range(self.GRID_SIZE):  # Performs Algorithm over every column
            for row_index in range(self.GRID_SIZE - 1):  # Skip topmost row
                row_index += 1
                if self.grid[row_index][col_index] != 0:
                    for i in range(row_index):  # iterates over every row above row_index
                        row_index_2 = row_index - 1 - i
                        if self.grid[row_index_2][col_index] == 0:
                            return False

                        elif self.grid[row_index][col_index] != self.grid[row_index_2][col_index]:
                            break

                        elif self.grid[row_index][col_index] == self.grid[row_index_2][col_index]:
                            return False

        # Move Down
        for col_index in range(self.GRID_SIZE):  # Performs Algorithm over every column
            for index in range(self.GRID_SIZE - 1):  # Skip bottom row
                row_index = self.GRID_SIZE - 2 - index
                if self.grid[row_index][col_index] != 0:
                    for i in range(index + 1):  # iterates over every row above row_index
                        row_index_2 = row_index + 1 + i
                        if self.grid[row_index_2][col_index] == 0:
                            return False

                        elif self.grid[row_index][col_index] != self.grid[row_index_2][col_index]:
                            break

                        elif self.grid[row_index][col_index] == self.grid[row_index_2][col_index]:
                            return False

        return True
