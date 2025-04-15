import game
import neat
import pickle


def calculate_fitness(score, highest_tile, penalty):
    return score + (highest_tile * 5) - penalty


counter = 0
average_fitness_history = []


def eval_genomes(genomes, configuration):
    num_moves = 5000
    total_fitness = 0
    generation_highest_tile = 0
    for i, (genome_id, genome) in enumerate(genomes):
        illegal_move_penalty = 0
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
                    else:
                        illegal_move_penalty += 20

                elif output == 1:
                    if environment.move_down():
                        environment.generate_random_tile()
                        break
                    else:
                        illegal_move_penalty += 15

                elif output == 2:
                    if environment.move_left():
                        environment.generate_random_tile()
                        break
                    else:
                        illegal_move_penalty += 5

                elif output == 3:
                    if environment.move_right():
                        environment.generate_random_tile()
                        break
                    else:
                        illegal_move_penalty += 30

            # environment.update()
            if environment.no_legal_moves():
                break

        highest_tile = max(max(row) for row in environment.grid)
        highest_tile = highest_tile if highest_tile > 4 else 0
        genome.fitness = calculate_fitness(environment.score, highest_tile, illegal_move_penalty)

        if highest_tile > generation_highest_tile:
            generation_highest_tile = highest_tile
        total_fitness += genome.fitness
    if counter % 250 == 0:
        print('---------------------------------------------------------------------')
        print(f'Highest Tile in Generation: {generation_highest_tile}')
        print(f'fitness history: {average_fitness_history}')
        print('---------------------------------------------------------------------')
        average_fitness_history.append(total_fitness / len(genomes))

def run_neat(configuration):
    # Variables
    # population = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4916')
    population = neat.Population(configuration)

    # Reporters
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    population.add_reporter(neat.Checkpointer(generation_interval=500))

    winner = population.run(eval_genomes, 5000)
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
