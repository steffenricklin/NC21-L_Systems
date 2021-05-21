"""
"""
# general imports
import matplotlib.pyplot as plt
import random
import numpy as np
import cv2  # to install: apt-get install -y python3-opencv
# local imports
from src.utils import turn_coords_to_numpy
from src.lsystem.LSystem import LSystem
from src.turtle import branching_turtle_to_coords

plt.style.use('bmh')  # Use some nicer default colors


class EA:
    """
    """
    def __init__(self, systems, goal_img):
        self.goal_img = goal_img
        if not isinstance(systems, list) and isinstance(systems, LSystem):
            systems = [systems, ]
        self.systems = systems

    def run_evolutions(self, n_evol_steps, prob_mutation=0.75):
        """starts of with a given L-system / candidate solution.
        - evaluates the quality of each candidate
        - then repeats until termination condition is satisfied:
        - select candidate solutions for reproduction
        - mutate the resulting candidates
        - evaluate new candidates
        - select candidates for the next generation
        """
        # evaluate initial system(s)
        fitnesses = [self.get_fitness(system) for system in self.systems]

        for step in range(n_evol_steps):
            # select candidate solution
            # self.systems = self.selectCandidates()  # TODO

            # mutate candidates
            for i, system in enumerate(self.systems):
                system.evolve_transformations(prob_mutation)
                self.systems[i] = system

            # evaluate the mutated candidates
            fitnesses = [self.get_fitness(system) for system in self.systems]

            # select candidates for next generation
            # self.systems = self.selectCandidates() # TODO
        return self.systems

    def get_fitness(self, system, method='hu'):
        if method == 'hu':
            X, Y = branching_turtle_to_coords(system.sequence)
            return self.calculate_hu_fitness(X, Y, self.goal_img)
        else:
            raise NotImplementedError

    def calculate_hu_fitness(self, X, Y, optimal):
        """
      solution: solution produced by the current rules (in string form)
      """
        nump_sol = turn_coords_to_numpy(X, Y)
        nump_sol = np.reshape(nump_sol[:, :, 0], (480, 640, 1))
        fitness = cv2.matchShapes(nump_sol, self.goal_img, cv2.CONTOURS_MATCH_I1, 0)
        return fitness

    def run_tournament_selection(self, population, optimal, tournament_size, size_pop):
        """
      Runs tournament selection on the current situation.
      This function computes the fitness of each candidate and then repeatedly
      chooses k candidates out of the population and selects the best one
      until the new population has formed. (selection with replacement)
      """

        selected = []

        # compute the fitness for each candidate
        coords_list = [system.to_coords() for system in population]
        fitness_list = [self.calculate_fitness(coordinate, optimal) for coordinate in coords_list]

        # run several tournaments, until there are enough candidates selected to replace the population
        while len(selected) < size_pop:
            # choose some random candidates from the population
            chosen_pop = random.sample(range(len(population)), tournament_size)

            # custom argmin
            f = lambda i: fitness_list[i]
            winner_ind = min(chosen_pop, key=f)

            # add the best solution
            selected.append(population[winner_ind])

        return selected
