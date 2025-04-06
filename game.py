import pygame
import random
import copy

class game_2048:
    def __init__(self):
        self.SCREEN_HEIGHT = 650
        self.SCREEN_WIDTH = 600
        self.GRID_SIZE = 4
        self.LINE_WIDTH = 4
        self.CELL_SIZE = self.SCREEN_WIDTH // self.GRID_SIZE
        self.score = 0
        self.grid = [[2, 0, 0, 0],
                     [4, 0, 0, 0],
                     [4, 0, 0, 0],
                     [2, 0, 0, 0]]
            # [[0 for e in range(self.GRID_SIZE)] for i in range(self.GRID_SIZE)]
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
                    # row, col = self.generate_random_tile()
                    # self.grid[row][col] = 2
                    pass

                elif event.key == pygame.K_w:
                    self.move_up()

                elif event.key == pygame.K_s:
                    self.move_down()

                elif event.key == pygame.K_a:
                    self.move_left()

                elif event.key == pygame.K_d:
                    self.move_right()

        self.win.fill((255, 255, 255))
        self.draw_grid()
        pygame.display.update()

    def generate_random_tile(self):  # broken
        pass
        # shuffled_rows = copy.deepcopy(self.grid)
        # random.shuffle(shuffled_rows)
        #
        # col_indices = list(range(len(shuffled_rows[0])))
        # random.shuffle(col_indices)
        # shuffled_tiles = [[row[i] for i in col_indices] for row in shuffled_rows]
        #
        # for row_index, row in enumerate(shuffled_tiles):
        #     for col_index, col in enumerate(row):
        #         if col == 0:
        #             return row_index, col_index

    def draw_grid(self):
        pygame.draw.rect(self.win, (0, 0, 0), (self.SCREEN_WIDTH - self.LINE_WIDTH, 50, self.LINE_WIDTH, self.SCREEN_HEIGHT - 50))
        pygame.draw.rect(self.win, (0, 0, 0), (0, self.SCREEN_HEIGHT - self.LINE_WIDTH, self.SCREEN_WIDTH, self.LINE_WIDTH))
        for row_index, row in enumerate(self.grid):
            pygame.draw.rect(self.win, (0, 0, 0), (row_index * self.CELL_SIZE, 50, self.LINE_WIDTH, self.SCREEN_HEIGHT - 50))
            pygame.draw.rect(self.win, (0, 0, 0), (0, row_index * self.CELL_SIZE + 50, self.SCREEN_WIDTH, self.LINE_WIDTH))
            for col_index, col in enumerate(row):
                if col != 0:
                    cell_x = (col_index * self.CELL_SIZE) + self.LINE_WIDTH * 1.5
                    cell_y = (row_index * self.CELL_SIZE) + self.LINE_WIDTH * 1.5 + 50
                    pygame.draw.rect(self.win, (255, 255, 125), (cell_x, cell_y,
                                                                 self.CELL_SIZE - (self.LINE_WIDTH * 2), self.CELL_SIZE - (self.LINE_WIDTH * 2)))
                    self.display_text(cell_x + (self.CELL_SIZE // 2), cell_y + (self.CELL_SIZE // 2), col, (0, 0, 0))

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
        for col_index in range(self.GRID_SIZE): # Performs Algorithm over every column
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

                        elif self.grid[row_index][col_index] == self.grid[row_index_2][col_index] and not cell_is_merged[row_index_2]:
                            counter += 1
                            cell_is_merged[row_index_2] = True
                            self.grid[row_index][col_index] += self.grid[row_index][col_index]
                            break

                    if counter != 0:
                        self.grid[row_index - counter][col_index] = self.grid[row_index][col_index]
                        self.grid[row_index][col_index] = 0

    def move_down(self):
        pass

    def move_right(self):
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
                            break

                    if counter != 0:
                        row[col_index + counter] = row[col_index]
                        row[col_index] = 0

    def move_left(self):
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
                            break

                    if counter != 0:
                        row[col_index - counter] = row[col_index]
                        row[col_index] = 0

    def check_if_legal(self):
        pass

    def no_legal_moves(self):
        pass