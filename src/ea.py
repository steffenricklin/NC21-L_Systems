"""
"""
# general imports
import matplotlib.pyplot as plt
import random
# local imports
from src.lsystem.LSystem import LSystem
from src.fitness import calculate_hu_fitness

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

    def run_evolutions(self, n_evol_steps, prob_mutation=0.75, tournament_size=3):
        """starts of with a given L-system / candidate solution.
        - evaluates the quality of each candidate
        - then repeats until termination condition is satisfied:
        - select candidate solutions for reproduction
        - mutate the resulting candidates
        - evaluate new candidates
        - select candidates for the next generation
        """
        best_fit = []
        for mu in range(self.pop_size):
            self.population.append(LSystem(None, None, 45, self.nr_iter, rand=True))

        # simulate evolution
        for gen in range(n_evol_steps):
            print("generation ", gen)
            # ?select random pairs
            # ?cross over
            # Some plants can grow offspring from their own roots: cloning
            # so who needs cross over anyway

            # mutations
            children = self.population.copy()

            for nr, child in enumerate(children):
                child.mutate_transformations(prob_mutation)

            self.population.extend(children)

            # select new generaton

            self.population = self.run_tournament_selection(self.population, self.goal_img, tournament_size,
                                                            self.pop_size)
            children.clear()
        return self.population

    def run_tournament_selection(self, population, optimal, tournament_size, size_pop):
        """
      Runs tournament selection on the current situation.
      This function computes the fitness of each candidate and then repeatedly
      chooses k candidates out of the population and selects the best one
      until the new population has formed. (selection with replacement)
      """

        selected = []

        # compute the fitness for each candidate
        print("start tournament selection")
        coords_list = [system.to_coords() for system in population]
        print(" - calculate hu fitness")
        fitness_list = [calculate_hu_fitness(coordinate, optimal) for coordinate in coords_list]
        print(" - fit for free", fitness_list[0])
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
