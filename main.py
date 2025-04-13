import game
import neat
import pickle


def calculate_fitness(score, illegal_moves, highest_tile):
    return score + (highest_tile * 10) + (illegal_moves * 20)


def eval_genomes(genomes, configuration):
    num_moves = 100
    for i, (genome_id, genome) in enumerate(genomes):
        num_illegal_moves = 0
        environment = game.Game2048()
        neural_net = neat.nn.FeedForwardNetwork.create(genome, configuration)
        for e in range(num_moves):
            output = neural_net.activate(environment.get_inputs())
            decision = output.index(max(output))  # [Up, Down, Left, Right]

            if decision == 0:
                if environment.move_up():
                    environment.generate_random_tile()
                else:
                    num_illegal_moves += 1
            elif decision == 1:
                if environment.move_down():
                    environment.generate_random_tile()
                else:
                    num_illegal_moves += 1
            elif decision == 2:
                if environment.move_left():
                    environment.generate_random_tile()
                else:
                    num_illegal_moves += 1
            elif decision == 3:
                if environment.move_right():
                    environment.generate_random_tile()
                else:
                    num_illegal_moves += 1

            environment.update()
            if environment.no_legal_moves():
                break

        highest_tile = [max(max(row) for row in environment.grid)]
        genome.fitness = calculate_fitness(environment.score, highest_tile, num_illegal_moves)


def run_neat(configuration):
    # Variables
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-29')
    population = neat.Population(configuration)

    # Reporters
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(1))

    winner = population.run(eval_genomes, 50)
    with open('best.pickle', 'wb') as f:
        pickle.dump(winner, f)


if __name__ == '__main__':
    config_path = "config.txt"
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    run_neat(config)
