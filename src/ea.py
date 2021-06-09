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
from src.lsystem.utils import init_population
plt.style.use('bmh')  # Use some nicer default colors


class EA:
    """
    """

    def __init__(self, goal, population_params):
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

    def run_evolutions(self, n_gens, prob_mutation=0.75, tournament_size=2):
        """starts of with a given L-system / candidate solution.
        - evaluates the quality of each candidate
        - then repeats until termination condition is satisfied:
        - select candidate solutions for reproduction
        - mutate the resulting candidates
        - evaluate new candidates
        - select candidates for the next generation
        """

        # simulate evolution
        fitness_population = None
        hu_season = True
        for _ in trange(n_gens, file=sys.stdout, desc='generations'):
            # for gen in range(n_gens):
            #     print("generation ", gen)
            # ?select random pairs
            # ?cross over
            # Some plants can grow offspring from their own roots: cloning
            # so who needs cross over anyway

            # mutations
            children = []

            pairs = np.random.choice(self.pop_size, (int(self.pop_size / 2), 2), replace=False)

            for pair in pairs:
                parent_a = self.population[pair[0]]
                parent_b = self.population[pair[1]]
                pc = random.random()
                if pc < self.cross_prob:
                    self.cross_over(parent_a, parent_b, children)
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
            if random.random() > 0.8:
                hu_season = not hu_season
            # print(hu_season)
            self.population, fitness_population = self.run_tournament_selection(self.population,
                                                                                (self.goal_system, self.goal_np),
                                                                                tournament_size,
                                                                                self.pop_size)
            # print("end selection")
            children.clear()
        return self.population, fitness_population

    def run_tournament_selection(self, population, goal, tournament_size, size_pop, hu_season=True):
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
        # find mathcing keys
        rules_a = parent_a.get_transformations()
        rules_b = parent_b.get_transformations()
        matches = set(rules_a.keys()) & set(rules_b.keys())
        if matches:
            chosen_key = random.choice(list(matches))

            # swap matching rules
            child_a = copy.deepcopy(parent_a)
            child_b = copy.deepcopy(parent_b)
            child_a.replace_rule(chosen_key, rules_b[chosen_key])
            child_b.replace_rule(chosen_key, rules_a[chosen_key])

            # add children
            children.append(child_a)
            children.append(child_b)
        else:
            chosen_key_a = random.choice(list(rules_a.keys()))
            chosen_key_b = random.choice(list(rules_b.keys()))

            # swap matching rules
            child_a = copy.deepcopy(parent_a)
            child_b = copy.deepcopy(parent_b)
            child_a.replace_rule(chosen_key_b, rules_b[chosen_key_b])
            child_b.replace_rule(chosen_key_a, rules_a[chosen_key_a])

            # add children
            children.append(child_a)
            children.append(child_b)
