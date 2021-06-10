"""
"""
# general imports
import sys
import copy
import queue
import random
import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt
# local imports
from src.lsystem.crossover import cross_over
from src.lsystem.utils import init_population
plt.style.use('bmh')  # Use some nicer default colors


class EA:
    """Provides functions to run the evolutionary algorithm
    """

    def __init__(self, goal, population_params):
        """Create the EA with the provided parameters and the to be achieved goal system.

        :param goal: LSystem that is to be approximated by the EA
        :param population_params: dictionary of parameters
        """
        # self.goal_system = LSystem('A', {'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'}, 22.5, 5)
        self.goal_system = goal  # L-System object
        self.goal_np = goal.to_numpy()  # L-System representation as numpy array
        self.pop_size = population_params["pop_size"]
        self.angle = population_params["angle"]
        self.nr_iter = population_params["iterations"]
        self.fitness_method = population_params["fitness_func"]
        self.cross_prob = 0.9

        # init population
        self.population = init_population(self.pop_size, None, None, self.angle, self.nr_iter, rand=True)

    def run_evolutions(self, n_gens, prob_mutation=0.75, tournament_size=10):
        """starts of with a the initial population and evolves it over n_gens generations.
        - for n_gens
            - select candidate solutions for reproduction
            - mutate the resulting candidates
            - evaluate new candidates
            - select candidates for the next generation

        :param n_gens: number of generations to simulate
        :param prob_mutation: probability of a system to mutate its transformation rules
        :param tournament_size: how many LSystems should compete with eachother
        """

        # simulate evolution
        fitness_population = None
        hu_season = True
        for _ in trange(n_gens, file=sys.stdout, desc='generations'):
            # make offsprings
            children = []

            pairs = np.random.choice(self.pop_size, (int(self.pop_size / 2), 2), replace=False)
            for pair in pairs:
                parent_a = self.population[pair[0]]
                parent_b = self.population[pair[1]]
                pc = random.random()
                if pc < self.cross_prob:
                    cross_over(parent_a, parent_b, children)
                else:
                    child_a = copy.deepcopy(parent_a)
                    child_b = copy.deepcopy(parent_b)

                    # add children
                    children.append(child_a)
                    children.append(child_b)

            # mutate offsprings
            for _, child in enumerate(children):
                child.mutate_transformations(prob_mutation)
            self.population.extend(children)

            # select new generation
            if random.random() > 0.8:
                hu_season = not hu_season

            self.population, fitness_population = self.run_tournament_selection(self.population,
                                                                                (self.goal_system, self.goal_np),
                                                                                tournament_size,
                                                                                self.pop_size)

            children.clear()  # cleanup
        return self.population, fitness_population

    def run_tournament_selection(self, population, goal, tournament_size, size_pop, hu_season=True):
        """
        Runs tournament selection on the current situation.
        This function computes the fitness of each candidate and then repeatedly
        chooses k candidates out of the population and selects the best one
        until the new population has formed. (selection with replacement)

        :param population: list of LSystems to run the t.-selection with
        :param goal: the to be achieved goal system: tuple(goal_system, goal_numpy)
        :param tournament_size: how many winners to selected in the tournament
        :param size_pop: how large the resulting population should be
        :param hu_season: use hu moments fitness function if True, else use the fitness function in self.fitness_method
        """
        assert tournament_size <= size_pop
        assert tournament_size > 1

        selected = []
        fitness_selected = []
        # compute the fitness for each candidate

        coords_list = []
        fitness_list = []
        for nr, system in enumerate(population):
            coords_list.append(system.to_coords())
            fitness_measure = 'hu' if hu_season else self.fitness_method
            fitness_list.append(system.get_fitness(goal, fitness_measure))
        combined_list = list(zip(population, fitness_list))
        random.shuffle(combined_list)

        q = queue.Queue(len(combined_list))
        for element in combined_list:
            q.put(element)
        while len(selected) < self.pop_size:
            best_system, best_fitness = q.get()
            for _ in range(tournament_size - 1):
                a_system, a_fitness = q.get()
                if a_fitness <= best_fitness:
                    q.put((best_system, best_fitness))
                    best_system = a_system
                    best_fitness = a_fitness
                else:
                    q.put((a_system, a_fitness))

            selected.append(best_system)
            fitness_selected.append(best_fitness)

        return selected, fitness_selected
