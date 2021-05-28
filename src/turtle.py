"""
"""
# general imports
from math import sin, cos
import matplotlib.pyplot as plt
# local imports
from src.constants import LETTER_STRING, DEGREES_TO_RADIANS


def branching_turtle_to_coords(turtle_program, turn_amount=45):
    saved_states = list()
    state = (0, 0, 90)
    yield 0, 0

    #print('turtle', turtle_program)

    for command in turtle_program:
        x, y, angle = state

        if command.lower() in LETTER_STRING:  # Move forward (matches a-j and A-J)
            # try:
            state = (x - cos(angle * DEGREES_TO_RADIANS),
                     y + sin(angle * DEGREES_TO_RADIANS),
                     angle)
            # except OverflowError as err:
            #     print("x: ", type(x), x)
            #     print("D: ", type(DEGREES_TO_RADIANS), DEGREES_TO_RADIANS)
            #     print("a: ", type(angle), angle)
            #     print(state)
            #     print(err)
            #     raise
            # print(state)

            if command.islower():  # Add a break in the line if command matches a-j
                yield float('nan'), float('nan')

            yield state[0], state[1]

        elif command == '+':  # Turn clockwise
            state = (x, y, angle + turn_amount)

        elif command == '-':  # Turn counterclockwise
            state = (x, y, angle - turn_amount)

        elif command == '[':  # Remember current state
            saved_states.append(state)

        elif command == ']':  # Return to previous state
            state = saved_states.pop()
            yield float('nan'), float('nan')
            x, y, _ = state
            yield x, y


def plot_coords(coords, bare_plot=False):
    if bare_plot:
        # Turns off the axis markers.
        plt.axis('off')
    # Ensures equal aspect ratio.
    plt.gca().set_aspect('equal', 'datalim')
    # Converts a list of coordinates into
    # lists of X and Y values, respectively.
    X, Y = zip(*coords)
    # Draws the plot.
    plt.plot(X, Y)
