# general imports
import numpy as np

# local imports
from src.ea import EA
from src.lsystem.LSystem import LSystem
from src.turtle import plot_coords, branching_turtle_to_coords
import src.utils as utils


def run(goal, params):
    # pass to EA
    ea = EA(goal, params)
    turtles, fitness_turtles = ea.run_evolutions(params["nr_gens"], tournament_size=params["tournament_size"])
    print("finished")

    utils.show_results(turtles, fitness_turtles, params)


def get_goal(axiom, transformations, angle, iterations):
    goal_system = LSystem(axiom, transformations, angle, iterations)
    goal_sequence = goal_system.transform_multiple(iterations)

    coords_g = branching_turtle_to_coords(goal_sequence, angle)
    x, y = zip(*coords_g)
    goal_numpy = utils.turn_coords_to_numpy(x, y)
    # ensure that it is not RGB anymore
    goal = np.reshape(goal_numpy[:, :, 0], (480, 640, 1))
    return goal


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    # define the ea - parameters
    parameters = {"angle": 22.5,
                  "pop_size": 10,
                  "iterations": 5,
                  "nr_gens": 3,
                  "tournament_size": 3}

    # define the goal parameters
    goal_img = get_goal(axiom='A',
                        transformations={'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'},
                        angle=parameters["angle"],
                        iterations=parameters["iterations"])

    # simulate
    run(goal_img, parameters)

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
