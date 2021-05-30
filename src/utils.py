# general imports
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')  # Use some nicer default colors
# local imports
import src.turtle as turtle


def turn_coords_to_numpy(X, Y):
    """
    X: list of x-coordinates
    Y: list of y-coordinates
    Turns the X and Y coordinates as extracted from zip(*branching_turtle_to_coordinates())
    into a numpy array representing the figure.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.tight_layout(pad=0)

    # To remove the huge white borders
    ax.margins(0)
    ax.plot(X, Y, color="black")
    ax.axis('off')

    fig.canvas.draw()       # draw the canvas, cache the renderer
    plt.close()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    return image


def show_results(l_systems, fitness_turtles, params):
    for i, system in enumerate(l_systems):
        seq = system.transform_multiple(params["iterations"])
        xy = turtle.branching_turtle_to_coords(seq, system.angle)
        turtle.plot_coords(xy, bare_plot=True)
        print(f"turtle {i}:")
        print("\t- axiom:   ", system.axiom)
        print("\t- t.-rules:", system.transformations)
        print("\t- fitness: ", fitness_turtles[i])
    best_turtle = l_systems[min(range(len(l_systems)), key=lambda x: fitness_turtles[x])]
    print(f"Best system is system #{best_turtle}")
