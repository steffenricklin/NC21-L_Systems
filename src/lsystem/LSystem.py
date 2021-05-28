"""
"""
# general imports
import random
import numpy as np
from PIL import Image
# local imports
import src.utils as utils
import src.turtle as turtle
import src.lsystem.mutations as mutate
from src.fitness import calculate_hu_fitness
from src.constants import LETTER_STRING


class LSystem:
    """
    Represents the production rules and provides functions for changing
    the production rule strings
    """

    def __init__(self, axiom, rules, angle, iterations=5, rand=False):
        """

        :param axiom:
        :param rules:
        :param angle:
        :param iterations:
        :param rand:
        """
        if not rand:
            self.axiom = axiom
            self.transformations = rules
            self.sequence = axiom
            self.angle = angle
            self.iterations = iterations

        elif rand:
            self.transformations = self.generate_random_rules()
            self.axiom = list(self.transformations.keys())[0]
            self.sequence = list(self.transformations.keys())[0]
            self.angle = angle
            self.iterations = iterations

    def mutate_transformations(self, p):
        """
        loops over the transformations and changes them
        """
        assert self.axiom is not None
        assert self.transformations is not None

        keys = list(self.transformations.keys())
        # loop over keys from transformations dict and change the value of that key with chance p
        for i in range(len(keys)):
            random_nr = random.random()
            if random_nr > p:
                key = keys[i]

                # point_mutation_transformation(self.transformations, key)

                # get random index in self.transformations key and change that
                index = random.randint(0, len(self.transformations[key]) - 1)
                value = self.transformations[key][index]

                # insert
                if random_nr >= 0.95:
                    self.transformations = mutate.add_plus_minus(self.transformations, key, index)
                '''I've commented this out because it generates unbalanced lists... '''
                # insert
                # elif random_nr >= 0.90:
                #    add_branch(transformations, key, index)

                if random_nr >= p:
                    # change existing characters
                    if value.isalpha():
                        mutate.change_letter(self.transformations, key, index)

                    # remove existing characters
                    elif value == '[':
                        self.transformations = mutate.remove_branch_left(self.transformations, key, index)
                    elif value == ']':
                        self.transformations = mutate.remove_branch_right(self.transformations, key, index)
                    elif value == '+' or value == '-':
                        self.transformations = mutate.remove_plus_minus(self.transformations, key, index)
                    else:
                        pass
        return self.transformations

    def transform_sequence(self):
        return ''.join(self.transformations.get(c, c) for c in self.sequence)

    def transform_multiple_evolve(self, iterations, p):
        """Tranforms for multiple iterations"""
        for _ in range(iterations):
            self.mutate_transformations(p)
            self.sequence = self.transform_sequence()
        return self.sequence

    def transform_multiple(self, iterations):
        """Tranforms for multiple iterations"""
        for _ in range(iterations):
            self.sequence = self.transform_sequence()
        return self.sequence

    def to_coords(self):
        sequence = self.transform_multiple(self.iterations)
        coords = turtle.branching_turtle_to_coords(sequence, self.angle)
        return zip(*coords)

    def show_image(self):
        x, y = self.to_coords()
        im_nump = utils.turn_coords_to_numpy(x, y)
        img = Image.fromarray(im_nump, 'RGB')
        img.show()

    def generate_random_rules(self):
        """
        Generates a simple dictionary with L-system rules.
        return:
        :return: rules
        """
        transformations = {}
        nr_rules = random.randint(1, 4)
        init_keys = "".join(random.choices(LETTER_STRING.upper(), k=nr_rules))

        for key in init_keys:
            if key not in transformations.keys():
                self.generate_random_rule(key, init_keys, transformations)

        return transformations

    def generate_random_rule(self, key, auxi_characters, transformations):
        """Generates simple, random rules containing the key and the characters from other keys and characters like []+-
        The rules are added to the dictionary

        :param key:
        :param auxi_characters:
        :param transformations:
        :return:
        """
        nr_chars_left = random.randint(1, 3)
        nr_chars_right = random.randint(1, 3)
        rule = key + "".join(random.choices(key + auxi_characters + "+" + "-", k=nr_chars_right))
        rule = "".join(random.choices(key + auxi_characters + "+" + "-", k=nr_chars_left)) + rule

        transformations[key] = rule
        # add branch with some probability
        ind_branch = random.randint(0, 2)
        if ind_branch < len(rule):
            mutate.add_branch(transformations, key, ind_branch)

    def get_fitness(self, optimal, method='hu'):
        if method == 'hu':
            return calculate_hu_fitness(self.to_coords(), optimal)
        else:
            raise NotImplementedError
