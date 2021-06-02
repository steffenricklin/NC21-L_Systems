"""
"""
# general imports
import matplotlib.pyplot as plt
import random
import copy
import queue
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
            self.population.append(LSystem(None, None, 45, self.nr_iter, rand=True))

        # simulate evolution
        fitness_population = None
        for gen in range(n_gens):
            print("generation ", gen)
            # ?select random pairs
            # ?cross over
            # Some plants can grow offspring from their own roots: cloning
            # so who needs cross over anyway

            # mutations
            children = copy.deepcopy(self.population)

            for nr, child in enumerate(children):
                child.mutate_transformations(prob_mutation)
            self.population.extend(children)

            # select new generation

            self.population, fitness_population = self.run_tournament_selection(self.population,
                                                                                self.goal_img,
                                                                                tournament_size,
                                                                                self.pop_size)
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

        q = queue.Queue(self.pop_size*2)
        for element in combined_list:
            q.put(element)
        while len(selected)< self.pop_size:
            best_system, best_fitness = q.get()
            for _ in range(tournament_size-1):
                a_system, a_fitness = q.get()
                if a_fitness <= best_fitness:
                    q.put((best_system, best_fitness))
                    best_system = a_system
                    best_fitness = a_fitness
                else:
                    q.put((a_system, a_fitness))

            selected.append(best_system)

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
