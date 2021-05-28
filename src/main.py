# general imports
import numpy as np

# local imports
from src.ea import EA
from src.lsystem.LSystem import LSystem
from src.turtle import plot_coords, branching_turtle_to_coords
from src.utils import turn_coords_to_numpy


def run(axiom, transformations, iterations=5, angle=22.5, pop_size=10, nr_gen=10, tournament_size=3):
    # goal parameters
    goal_axiom = 'A'
    goal_transformations = {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}
    goal_angle = 22.5
    goal_system = LSystem(goal_axiom, goal_transformations, goal_angle, iterations)

    goal_system.transform_multiple(iterations)

    coords_g = branching_turtle_to_coords(goal_system.sequence, angle)
    x, y = zip(*coords_g)
    goal_nump = turn_coords_to_numpy(x, y)
    # ensure that it is not RGB anymore
    goal_img = np.reshape(goal_nump[:, :, 0], (480, 640, 1))

    # init L-system ######Why should we start from just one ?
    # system_zero = LSystem(axiom, transformations, angle)
    params = {"angle": angle, "pop_size": pop_size, "iterations": iterations}

    # pass to EA
    ea = EA(goal_img, params)
    turtles = ea.run_evolutions(nr_gen)
    print("finished")
    # best = turtles.getBest(1)
    best = turtles[0].sequence

    # show results
    coords = branching_turtle_to_coords(best, angle)
    plot_coords(coords, bare_plot=True)  # bare_plot removes the axis labels


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    axiom = 'A'
    transformations = {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}
    iterations = 5
    angle = 22.5
    pop_size = 10
    # a = LSystem(None, None, None, iterations, rand=True)
    # a.show_image()

    run(axiom, transformations, iterations, angle, pop_size=pop_size, nr_gen=3, tournament_size=3)


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
