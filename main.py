import game
import neat
import pickle


def eval_genomes(genomes, config, num_moves):
    for i, (genome_id, genome) in enumerate(genomes):
        environment = game.Game2048()
        neural_net = neat.nn.FeedForwardNetwork.create(genome, config)
        for e in range(num_moves):
            output = neural_net.activate(environment.get_inputs())
            decision = output.index(max(output))  # [Up, Down, Left, Right]

            if decision == 0:
                environment.move_up()
            elif decision == 1:
                environment.move_down()
            elif decision == 2:
                environment.move_left()
            elif decision == 3:
                environment.move_right()

            environment.update()
            if environment.no_legal_moves():
                break

        genome.fitness = environment.score()


def run_neat(config):
    # Variables
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1')
    population = neat.Population(config)

    # Reporters
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(1))

    winner = population.run(eval_genomes, 50)
    with open('best.pickle', 'wb') as f:
        pickle.dump(winner, f)

# env = game.Game2048()
# while env.alive:
#     env.update()
#     if env.no_legal_moves():
#         print(f'score:{env.score}')
#         env.alive = False
