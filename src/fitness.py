"""
Contains possibly multiple fitness functions
"""
# general imports
import numpy as np
import cv2  # python3 opencv
# local imports
import src.utils as utils


def calculate_hu_fitness(coordinates, optimal):
    """Calculates the fitness using hu moments.
    solution: solution produced by the current rules (in string form)

    :param coordinates: coordinates (x,y) of a LSystem
    :param optimal: goal system as numpy array
    :return: float fitness value
    """
    x, y = coordinates
    numpy_sol = utils.turn_coords_to_numpy(x, y)
    numpy_sol = np.reshape(numpy_sol[:, :, 0], (480, 640, 1))
    fitness = cv2.matchShapes(numpy_sol, optimal, cv2.CONTOURS_MATCH_I2, 0)
    return fitness


def convex_hull_defect_fitness(coordinates, optimal):
    """Computes a fitness value based on convex hull defects

    :param coordinates: coordinates (x,y) of a LSystem
    :param optimal: goal system/as_numpy (not needed?)
    """
    # optimal_coord = optimal.to_coords()
    current_chd_distances = calculate_convexity_defects(coordinates)
    # optimal_chd_distances = calculate_convexity_defects(optimal_coord)
    len_opt = 12  # len(optimal_chd_distances) 12
    average_opt = 27858.0  # sum(optimal_chd_distances[:,0,3])/len_opt 27858.0
    average_current = sum(current_chd_distances[:, 0, 3]) / len(current_chd_distances)
    difference_nr = abs(len(current_chd_distances) - len_opt)
    difference_average = abs(average_current - average_opt) / 10000

    return difference_nr + difference_average


def calculate_convexity_defects(coordinates):
    """Computes the convexity defects of the given coordinates of a LSystem

    :param coordinates: coordinates (x,y) of a LSystem
    return: convexity defects of the current structure
    """
    x, y = coordinates
    numpy_sol = utils.turn_coords_to_numpy(x, y)
    gray = cv2.cvtColor(numpy_sol, cv2.COLOR_BGR2GRAY)

    conts, hierarchy = cv2.findContours(gray.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(conts, key=lambda l: cv2.contourArea(l), reverse=True)
    hull = cv2.convexHull(contours[1], returnPoints=False)

    defects = cv2.convexityDefects(contours[1], hull)
    return defects


def calculate_rms(x1, x2):
    mse = np.sqrt(np.mean(np.sum(np.square(x1 - x2), axis=-1)))
    return float(mse)
