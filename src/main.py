# general imports
# local imports
from src.ea import EA
from src.lsystem.LSystem import LSystem
import src.utils as utils


def run(goal_system, params):
    """
    runs the evolutionary algorithm (ea) on a given goal_system with given parameters
    """
    goal_system.show_image(f"Goal system, iterations={str(goal_system.iterations)}")

    # pass to EA and run the simulation
    ea = EA(goal_system, params)
    results_systems, results_fitness = ea.run_evolutions(n_gens=params["nr_gens"],
                                                         prob_mutation=params["p_mutation"],
                                                         tournament_size=params["tournament_size"])

    # plot print_n systems from the resulting population
    utils.show_results(results_systems, results_fitness, print_n=params["tournament_size"])


def test():
    from src.fitness import calculate_convexity_defects
    system = LSystem('A', {'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'}, 22.5, 5)
    coordinates = system.to_coords()
    calculate_convexity_defects(coordinates)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    # define the ea - parameters
    parameters = {"angle": 22.5,
                  "pop_size": 30,
                  "iterations": 5,
                  "nr_gens": 500,
                  "tournament_size": 5,
                  "p_mutation": 0.75,
                  "fitness_func": ['convex']
                  }

    # define the goal, returns a goal L-System and it's numpy representation
    goal = LSystem(axiom='A',
                   rules={'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'},
                   angle=parameters["angle"],
                   iterations=parameters["iterations"])

    # simulate
    run(goal, parameters)
    # test()
    print("done.")
