import game

env = game.Game2048()

while env.alive:
    env.update()
    if env.no_legal_moves():
        print(f'score:{env.score}')
        env.print_grid()
        env.alive = False
