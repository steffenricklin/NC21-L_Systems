"""
"""
# general imports
import sys

import matplotlib.pyplot as plt
import random
import copy
import queue
from tqdm import trange
# local imports
from src.lsystem.LSystem import LSystem
from src.fitness import calculate_hu_fitness
import numpy as np

plt.style.use('bmh')  # Use some nicer default colors


class EA:
    """
    """

    def __init__(self, goal_img, population_params):
        self.goal_img = goal_img
        self.population = []
        self.pop_size = population_params["pop_size"]
        self.angle = population_params["angle"]
        self.nr_iter = population_params["iterations"]
        self.cross_prob = 0.9

    def run_evolutions(self, n_gens, prob_mutation=0.75, tournament_size=2):
        """starts of with a given L-system / candidate solution.
        - evaluates the quality of each candidate
        - then repeats until termination condition is satisfied:
        - select candidate solutions for reproduction
        - mutate the resulting candidates
        - evaluate new candidates
        - select candidates for the next generation
        """
        for mu in range(self.pop_size):
            self.population.append(LSystem(None, None, 45, iterations=self.nr_iter, rand=True))

        # simulate evolution
        fitness_population = None
        for _ in trange(n_gens, file=sys.stdout, desc='generations'):
            # for gen in range(n_gens):
            #     print("generation ", gen)
            # ?select random pairs
            # ?cross over
            # Some plants can grow offspring from their own roots: cloning
            # so who needs cross over anyway

            # mutations
            children = []

            pairs = np.random.choice(self.pop_size,(int(self.pop_size/2), 2), replace=False)

            for pair in pairs:
                parent_a = self.population[pair[0]]
                parent_b = self.population[pair[1]]
                pc = random.random()
                if pc < self.cross_prob:
                    self.cross_over(parent_a,parent_b, children)
                else:
                    child_a = copy.deepcopy(parent_a)
                    child_b = copy.deepcopy(parent_b)

                    # add children
                    children.append(child_a)
                    children.append(child_b)

            for _, child in enumerate(children):
                child.mutate_transformations(prob_mutation)
            self.population.extend(children)

            # select new generation

            self.population, fitness_population = self.run_tournament_selection(self.population,
                                                                                self.goal_img,
                                                                                tournament_size,
                                                                                self.pop_size)
            print("end selection")
            children.clear()
        return self.population, fitness_population

    def run_tournament_selection(self, population, optimal, tournament_size, size_pop):
        assert tournament_size <= size_pop
        assert tournament_size > 1
        """
      Runs tournament selection on the current situation.
      This function computes the fitness of each candidate and then repeatedly
      chooses k candidates out of the population and selects the best one
      until the new population has formed. (selection with replacement)
      """

        selected = []
        fitness_selected = []
        # compute the fitness for each candidate
        # print("start tournament selection")
        coords_list = []
        for nr, system in enumerate(population):
            coords_list.append(system.to_coords())
        fitness_list = [calculate_hu_fitness(coordinate, optimal) for coordinate in coords_list]
        combined_list = list(zip(population, fitness_list))
        random.shuffle(combined_list)

        q = queue.Queue(self.pop_size * 2)
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

        '''
        # run several tournaments, until there are enough candidates selected to replace the population
        while len(selected) < size_pop:
        #    # choose some random candidates from the population
            chosen_pop = random.sample(range(len(population)), tournament_size)

            # custom argmin
            f = lambda i: fitness_list[i]
            winner_ind = min(chosen_pop, key=f)

            # add the best solution
            selected.append(population[winner_ind])
            fitness_selected.append(fitness_list[winner_ind])
        '''

        return selected, fitness_selected
    def cross_over(self, parent_a, parent_b, children):
        #find mathcing keys
        rules_a = parent_a.get_transformations()
        rules_b = parent_b.get_transformations()
        matches = set(rules_a.keys()) & set(rules_b.keys())
        if matches:
            chosen_key = random.choice(list(matches))

            #swap matching rules
            child_a = copy.deepcopy(parent_a)
            child_b = copy.deepcopy(parent_b)
            child_a.replace_rule(chosen_key, rules_b[chosen_key])
            child_b.replace_rule(chosen_key, rules_a[chosen_key])

            #add children
            children.append(child_a)
            children.append(child_b)
        else:
            child_a = copy.deepcopy(parent_a)
            child_b = copy.deepcopy(parent_b)

            # add children
            children.append(child_a)
            children.append(child_b)