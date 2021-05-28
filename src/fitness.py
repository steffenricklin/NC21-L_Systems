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
    X, Y = coordinates
    nump_sol = utils.turn_coords_to_numpy(X, Y)
    nump_sol = np.reshape(nump_sol[:, :, 0], (480, 640, 1))
    fitness = cv2.matchShapes(nump_sol, optimal, cv2.CONTOURS_MATCH_I1, 0)
    return fitness
