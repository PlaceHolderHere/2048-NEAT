import game

env = game.Game2048()

while env.alive:
    env.update()
