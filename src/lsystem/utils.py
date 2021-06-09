"""
contains auxiliary methods related to L-Systems
"""
from src.lsystem.LSystem import LSystem


def init_population(pop_size, axiom, rules, angle, iterations, rand):
    pop = []
    for mu in range(pop_size):
        pop.append(LSystem(axiom, rules, angle, iterations, rand))
    return pop
