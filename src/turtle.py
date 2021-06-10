"""
"""
# general imports
from math import sin, cos
import matplotlib.pyplot as plt
# local imports
from src.constants import LETTER_STRING, DEGREES_TO_RADIANS


def branching_turtle_to_coords(sequence, turn_amount=45):
    """Transforms a sequence from an LSystem into x,y coordinates.

    :param sequence: sequence of characters from an LSystem representation
    :param turn_amount: the angle at which the 'turtle' turns
    """
    saved_states = list()
    state = (0, 0, 90)
    yield 0, 0

    for command in sequence:
        x, y, angle = state

        if command.lower() in LETTER_STRING:  # Move forward (matches a-j and A-J)
            state = (x - cos(angle * DEGREES_TO_RADIANS),
                     y + sin(angle * DEGREES_TO_RADIANS),
                     angle)

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


def plot_coords(coords, title, bare_plot=False):
    """Plots the given coordinates

    :param coords: coordinates x,y
    :param title: title for the plot
    :param bare_plot: True turns the axis markers off
    """
    if bare_plot:
        # Turns off the axis markers.
        plt.axis('off')
    # Ensures equal aspect ratio.
    plt.gca().set_aspect('equal', 'datalim')
    # Converts a list of coordinates into
    # lists of X and Y values, respectively.
    x, y = zip(*coords)
    # Draws the plot.
    plt.plot(x, y)
    plt.title(title)
    plt.show()
