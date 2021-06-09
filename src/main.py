# general imports
# local imports
from src.ea import EA
from src.lsystem.LSystem import define_goal, LSystem
import src.utils as utils

from src.fitness import calculate_convexity_defects

def run(goal_system, goal, params):
    goal_system.show_image(f"Goal system, iterations={str(goal_system.iterations)}")

    # pass to EA
    ea = EA(goal, params)
    turtles, fitness_turtles = ea.run_evolutions(params["nr_gens"], prob_mutation=params["p_mutation"], tournament_size=params["tournament_size"])
    print("finished")

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

    # define the goal parameters

    goal_system, goal = define_goal(axiom='A',
                                    transformations={'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'},
                                    angle=parameters["angle"],
                                    iterations=parameters["iterations"])

    # simulate
    run(goal_system, goal, parameters)
    #test()
