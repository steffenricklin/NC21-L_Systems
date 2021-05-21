"""
"""
# general imports
import random
from PIL import Image
# local imports
import src.utils as utils
import src.turtle as turtle
import src.lsystem.mutations as mutate


class LSystem:
    """
    Represents the production rules and provides functions for changing
    the production rule strings
    """

    def __init__(self, axiom, rules, angle):
        self.axiom = axiom
        self.transformations = rules
        self.sequence = axiom
        self.angle = angle

    def evolve_transformations(self, p):
        """
        loops over the transformations and changes them
        """
        keys = list(self.transformations.keys())
        # loop over keys from transformations dict and change the value of that key with chance p
        for i in range(len(keys)):
            rndm = random.random()
            if rndm > p:
                key = keys[i]

                # point_mutation_transformation(self.transformations, key)

                # get random index in self.transformations key and change that
                index = random.randint(0, len(self.transformations[key]) - 1)
                value = self.transformations[key][index]

                # insert
                if rndm >= 0.95:
                    self.transformations = mutate.add_branch(self.transformations, key, index)

                # change existing characters
                elif value.isalpha():
                    mutate.change_letter(self.transformations, key, index)

                # remove existing characters
                elif value == '[':
                    self.transformations = mutate.remove_branch_left(self.transformations, key, index)
                elif value == ']':
                    self.transformations = mutate.remove_branch_right(self.transformations, key, index)
                elif value == '+' or '-':
                    self.transformations = mutate.remove_plus_minus(self.transformations, key, index)

                else:
                    pass

        return self.transformations

    def transform_sequence(self):
        return ''.join(self.transformations.get(c, c) for c in self.sequence)

    def transform_multiple_evolve(self, iterations, p):
        """Tranforms for multiple iterations"""
        for _ in range(iterations):
            self.transformations = self.evolve_transformations(p)
            self.sequence = self.transform_sequence()
        return self

    def transform_multiple(self, iterations):
        """Tranforms for multiple iterations"""
        for _ in range(iterations):
            self.sequence = self.transform_sequence()
        return self

    def to_coords(self):
        axiom = list(self.transformations.keys())[0]
        turtle_program = self.transform_multiple(axiom)
        coords = turtle.branching_turtle_to_coords(self.sequence, self.angle)
        return zip(*coords)

    def show_image(self):
        X, Y = self.to_coords()
        im_nump = utils.turn_coords_to_numpy(X, Y)
        img = Image.fromarray(im_nump, 'RGB')
        img.show()
