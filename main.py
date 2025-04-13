import game
import neat
import pickle


def calculate_fitness(score, highest_tile):
    return score + (highest_tile * 10)


def eval_genomes(genomes, configuration):
    num_moves = 1000
    for i, (genome_id, genome) in enumerate(genomes):
        environment = game.Game2048()
        neural_net = neat.nn.FeedForwardNetwork.create(genome, configuration)
        for e in range(num_moves):
            outputs = neural_net.activate(environment.get_inputs())
            sorted_output = sorted(range(len(outputs)), key=lambda x: outputs[x], reverse=True)

            for output in sorted_output:
                if output == 0:
                    if environment.move_up():
                        environment.generate_random_tile()
                        break

                elif output == 1:
                    if environment.move_down():
                        environment.generate_random_tile()
                        break

                elif output == 2:
                    if environment.move_left():
                        environment.generate_random_tile()
                        break

                elif output == 3:
                    if environment.move_right():
                        environment.generate_random_tile()
                        break

            environment.update()
            if environment.no_legal_moves():
                break

        highest_tile = max(max(row) for row in environment.grid)
        highest_tile = highest_tile if highest_tile > 4 else 0
        print(f'{i}. highest_tile: {highest_tile} | score:{environment.score}')
        genome.fitness = calculate_fitness(environment.score, highest_tile)


def run_neat(configuration):
    # Variables
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-52')
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
