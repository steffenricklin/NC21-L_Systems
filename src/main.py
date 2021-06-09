# general imports
# local imports
from src.ea import EA
from src.lsystem.LSystem import define_goal
import src.utils as utils

from src.lsystem import LSystem
from src.fitness import calculate_convexity_defects

def run(goal_system, goal, params):
    goal_system.show_image(f"Goal system, iterations={str(goal_system.iterations)}")

    # pass to EA
    ea = EA(goal, params)
    turtles, fitness_turtles = ea.run_evolutions(params["nr_gens"], tournament_size=params["tournament_size"])
    print("finished")

    utils.show_results(turtles, fitness_turtles, print_n=20)

def test():
    pop= LSystem.LSystem('A', {'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'}, 22.5, 5)
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
                  "tournament_size": 5}

    # define the goal parameters

    goal_system, goal = define_goal(axiom='A',
                                    transformations={'B': 'BB', 'A': 'B[+AB-[A]--A][---A]'},
                                    angle=parameters["angle"],
                                    iterations=parameters["iterations"])

    # simulate
    run(goal_system, goal, parameters)
    #test()

# def l_plot_evolve(axiom, transformations, iterations=0, angle=45., p=0.5):
#     lsystem = LSystem(axiom, transformations, angle)
#     turtle_program = lsystem.transform_multiple_evolve(iterations, p)
#     coords = branching_turtle_to_coords(turtle_program, angle)
#     plot_coords(coords, bare_plot=True)  # bare_plot removes the axis labels
#
#
# def l_plot(axiom, transformations, iterations=0, angle=45.):
#     lsystem = LSystem(axiom, transformations, angle)
#     turtle_program = lsystem.transform_multiple(iterations)
#     coords = branching_turtle_to_coords(turtle_program, angle)
#     plot_coords(coords, bare_plot=True)  # bare_plot removes the axis labels
#
#
# def main():
#     # l_plot_evolve('A', {'F': ['F', 'F'], 'A': ['F', '[', '+', 'A', 'F', '-', '[', 'A', ']', '-', '-', 'A', ']', '[', '-', '-', '-', 'A', ']']}, 5, 22.5)
#     l_plot_evolve('A', {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}, 5, 22.5)
#
#     l_plot('A', {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}, 5, 22.5)
