# general imports
# local imports
from src.ea import EA
from src.lsystem.LSystem import LSystem
from src.fitness import calculate_convexity_defects
import src.utils as utils


def run(goal_system, params):

    goal_system.show_image(f"Goal system, iterations={str(goal_system.iterations)}")

    # pass to EA
    ea = EA(goal_system, params)
    turtles, fitness_turtles = ea.run_evolutions(n_gens=params["nr_gens"],
                                                 prob_mutation=params["p_mutation"],
                                                 tournament_size=params["tournament_size"])
    print("done.")

    utils.show_results(turtles, fitness_turtles, print_n=params["tournament_size"])


def test():
    pop = LSystem('A', {'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'}, 22.5, 5)
    coordinates = pop.to_coords()
    calculate_convexity_defects(coordinates)
    print("finished")


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
    goal = define_goal(axiom='A',
                       transformations={'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'},
                       angle=parameters["angle"],
                       iterations=parameters["iterations"])

    # simulate
    run(goal, parameters)
    # test()
