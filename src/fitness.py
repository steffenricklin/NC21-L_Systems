"""
Contains possibly multiple fitness functions
"""
# general imports
import numpy as np
import cv2  # python3 opencv
# local imports
import src.utils as utils


def calculate_hu_fitness(coordinates, optimal):
    """
  solution: solution produced by the current rules (in string form)
  """
    x, y = coordinates
    numpy_sol = utils.turn_coords_to_numpy(x, y)
    numpy_sol = np.reshape(numpy_sol[:, :, 0], (480, 640, 1))
    fitness = cv2.matchShapes(numpy_sol, optimal, cv2.CONTOURS_MATCH_I2, 0)
    return fitness

def calculate_convexity_defects(coordinates):
    '''
    return: convexivity defects of the current structure
    '''
    #TO DO