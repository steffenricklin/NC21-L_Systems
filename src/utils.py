# general imports
import random
from math import isnan
from math import pi, sin, cos
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')  # Use some nicer default colors
import cv2  # to install: apt-get install -y python3-opencv
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# local imports
import src.constants
# from src.L_system import LSystem


def turn_coords_to_numpy(X, Y):
    '''
    X: list of x-coordinates
    Y: list of y-coordinates
    Turns the X and Y coordinates as extracted from zip(*branching_turtle_to_coordinates())
    into a numpy array representing the figure.
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.tight_layout(pad=0)

    # To remove the huge white borders
    ax.margins(0)
    ax.plot(X,Y, color="black")
    ax.axis('off')

    fig.canvas.draw()       # draw the canvas, cache the renderer
    plt.close()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    return image


