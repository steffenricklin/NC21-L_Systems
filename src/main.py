# imports
## general imports
%matplotlib inline
import numpy as np

## local imports
from src.ea import EA
from src.L_system import LSystem
from src.turtle import plot_coords, branching_turtle_to_coords
from src.utils import turn_coords_to_numpy


def run(axiom='A', rules={'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}, iterations=5, angle=22.5):
    #goal parameters
    axiom = 'A'
    transformations = {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'} 
    goal_system = LSystem(axiom, transformations)

    iterations = 5
    goal_system.transform_multiple(iterations)

    coords_g = branching_turtle_to_coords(goal_system.sequence, angle=22.5)
    X,Y = zip(*coords_g)
    goal_nump = turn_coords_to_numpy(X,Y)
    #ensure that it is not RGB anymore 
    goal_img =  np.reshape(goal_nump[:,:,0],(480,640,1))


    # init L-system
    system_zero = LSystem(axiom, rules) # TODO: make a instance of an l-system with the parameters above

    # pass to EA
    ea = EA(system_zero, goal_img)
    turtles = ea.runEvolutions(iterations)
    #best = turtles.getBest(1)
    best = turtles[0].sequence

    # show results
    coords = branching_turtle_to_coords(best, angle)
    plot_coords(coords, bare_plot=True) # bare_plot removes the axis labels

run()


def l_plot_evolve(axiom, transformations, iterations=0, angle=45, p=0.5):
    turtle_program = transform_multiple_evolve(axiom, transformations, iterations, p)
    coords = branching_turtle_to_coords(turtle_program, angle)
    plot_coords(coords, bare_plot=True) # bare_plot removes the axis labels


def l_plot(axiom, transformations, iterations=0, angle=45):
    turtle_program = transform_multiple(axiom, transformations, iterations)
    coords = branching_turtle_to_coords(turtle_program, angle)
    plot_coords(coords, bare_plot=True) # bare_plot removes the axis labels


def main():
    #l_plot_evolve('A', {'F': ['F', 'F'], 'A': ['F', '[', '+', 'A', 'F', '-', '[', 'A', ']', '-', '-', 'A', ']', '[', '-', '-', '-', 'A', ']']}, 5, 22.5)
    l_plot_evolve('A', {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}, 5, 22.5)

    l_plot('A', {'F': 'FF', 'A': 'F[+AF-[A]--A][---A]'}, 5, 22.5)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    run()
