# general imports
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
plt.style.use('bmh')  # Use some nicer default colors
# local imports


def turn_coords_to_numpy(x, y):
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
    ax.plot(x, y, color="black")
    ax.axis('off')

    fig.canvas.draw()       # draw the canvas, cache the renderer
    plt.close()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    
    return image


def show_results(l_systems, fitness_turtles, print_n):
    arg_systems = np.argsort(fitness_turtles)
    l_systems = list(np.asarray(l_systems)[arg_systems])
    fitness_turtles = list(np.asarray(fitness_turtles)[arg_systems])

    rng = len(l_systems) if len(l_systems) < print_n else print_n
    for i in range(rng):
        system = l_systems[i]
        fitness = fitness_turtles[i]
        system.show_image(f"system {str(i)}, iterations={str(system.iterations)},\nfitness={str(round(fitness, 5))}")
        print(f"turtle {i}:")
        print("\t- axiom:   ", system.axiom)
        print("\t- t.-rules:", system.transformations)
        print("\t- fitness: ", fitness_turtles[i])


def fig2data(fig):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    source: https://web-backend.icare.univ-lille.fr/tutorials/convert_a_matplotlib_figure
    """
    # draw the renderer
    fig.canvas.draw()

    # Get the RGBA buffer from the figure
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    buf = np.roll(buf, 3, axis=2)
    return buf


def fig2img(fig):
    """
    @brief Convert a Matplotlib figure to a PIL Image in RGBA format and return it
    @param fig a matplotlib figure
    @return a Python Imaging Library ( PIL ) image
    source: https://web-backend.icare.univ-lille.fr/tutorials/convert_a_matplotlib_figure
    """
    # put the figure pixmap into a numpy array
    buf = fig2data(fig)
    w, h, d = buf.shape
    return Image.frombytes("RGBA", (w, h), buf.tostring()).convert("L")
