"""
contains auxiliary methods related to L-Systems
"""
from src.lsystem.LSystem import LSystem


def init_population(pop_size, axiom, rules, angle, iterations, rand):
    """Initializes a list (population) of LSystem objects with the given parameters

    :param pop_size: population size. How many LSystems to create
    :param axiom: starting axiom of the LSystems. May be None if rand==True
    :param rules: dictionary of transformation rules. May be None if rand==True
    :param angle: angle that is used for turning when drawing the LSystem
    :param iterations: depths of the LSystems
    :param rand: whether to create fixed or random LSystems. Set to True to create random Lsystems
    :return: new LSystem population
    """
    pop = []
    for mu in range(pop_size):
        pop.append(LSystem(axiom, rules, angle, iterations, rand))
    return pop
