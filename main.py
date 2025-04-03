import game

env = game.game_2048()

while env.alive:
    env.update()
