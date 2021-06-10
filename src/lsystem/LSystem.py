# general imports
import random
import numpy as np
# local imports
import src.utils as utils
import src.turtle as turtle
import src.fitness as fitness
import src.lsystem.mutations as mutate
from src.constants import LETTER_STRING, debug


class LSystem:
    """L-System representation that has an axiom, transformation rules, etc., with the functionality
    to mutate, produce a tree sequence string, returning the system's fitness value etc.
    """
    def __init__(self, axiom, rules, angle, iterations, rand=False):
        """Initialize the L-System with a given axiom, transformation rules and angle or create one randomly.
        Define the depths of the system with the iterations variable.

        :param axiom: the starting letter
        :param rules: transformation rules
        :param angle: the angle that the drawing program uses when turning
        :param iterations: depth of the system when creating the sequence string
        :param rand: whether to initialize a random L-System
        """
        if not rand:
            self.transformations = rules
            self.axiom = axiom
            self.angle = angle
            self.iterations = iterations

        elif rand:
            self.transformations = self.generate_random_rules()
            self.axiom = list(self.transformations.keys())[0]
            self.angle = angle
            self.iterations = iterations

    def mutate_transformations(self, p):
        """Mutate the transformation rules with probability p.
        It either adds/removes a plus/minus, a branch or changes an existing alphabet character.

        :param p: probability of mutation
        """
        assert self.axiom is not None
        assert self.transformations is not None

        keys = list(self.transformations.keys())
        # loop over keys from transformations dict and change the value of that key with chance p
        for i in range(len(keys)):
            random_nr = random.random()
            if random_nr > p:
                key = keys[i]

                # point_mutation_transformation(self.transformations, key) # no point mutation

                # get random index in self.transformations key and change that
                index = random.randint(0, len(self.transformations[key]) - 1)
                value = self.transformations[key][index]

                # insert
                if random_nr >= 0.95:
                    self.transformations = mutate.add_plus_minus(self.transformations, key, index)

                # elif random_nr >= 0.90:  '''Commented out since it generates unbalanced lists... '''
                #    add_branch(transformations, key, index)

                # change existing characters
                if value.isalpha():
                    mutate.change_letter(self.transformations, key, index)

                # remove existing characters
                elif value == '[':
                    self.transformations = mutate.remove_branch(self.transformations, key, index,
                                                                is_open_bracket=True)
                elif value == ']':
                    self.transformations = mutate.remove_branch(self.transformations, key, index,
                                                                is_open_bracket=False)
                elif value == '+' or value == '-':
                    self.transformations = mutate.remove_plus_minus(self.transformations, key, index)
                else:
                    pass

    def transform_sequence(self, sequence):
        """Applies transformation rules to the characters in the provided sequence and returns the result.

        :param sequence: string of characters
        :return: an transformed sequence
        """
        return ''.join(self.transformations.get(c, c) for c in sequence)

    def transform_multiple_evolve(self, n_iterations, p):
        """Transforms the system's axiom for n_iterations into a sequence by applying transformation rules.
        It also evolves the transformation rule in each iteration with probability p.

        :param n_iterations: depth of the system
        :param p: mutation probability
        :return: evolved system transformed into a sequence
        """
        sequence = self.axiom
        for _ in range(n_iterations):
            self.mutate_transformations(p)
            sequence = self.transform_sequence(sequence)
        return sequence

    def transform_multiple(self, n_iterations):
        """Transforms the system's axiom for n_iterations into a sequence by applying transformation rules without 
        evolving the transformation rules.
        
        :param n_iterations: depth of the system
        :return: system transformed into a sequence
        """
        sequence = self.axiom
        for _ in range(n_iterations):
            sequence = self.transform_sequence(sequence)
        return sequence

    def to_coords(self):
        """Gets the system's resulting sequence and turns it into coordinates

        :return: system translated to coordinates
        """
        sequence = self.transform_multiple(self.iterations)
        xy = turtle.branching_turtle_to_coords(sequence, self.angle)
        return zip(*xy)

    def show_image(self, title=""):
        """Plots the system's resulting sequence.

        :param title: additional title for the resulting plot, empty by default
        """
        seq = self.transform_multiple(self.iterations)
        xy = turtle.branching_turtle_to_coords(seq, self.angle)
        turtle.plot_coords(xy, title, bare_plot=True)

    def generate_random_rules(self):
        """Generates a simple dictionary with L-system rules.

        :return: generated rules
        """
        transformations = {}
        nr_rules = random.randint(1, 4)
        init_keys = "".join(random.choices(LETTER_STRING.upper(), k=nr_rules))

        for key in init_keys:
            if key not in transformations.keys():
                transformations = self.generate_random_rule_set(key, init_keys, transformations)

        return transformations

    def generate_random_rule_set(self, key, auxi_characters, transformations):
        """Generates simple, random rules containing the key and the characters from other keys and characters like []+-
        The rules are added to the dictionary.

        :param key: key/index of the transformations dictionary/list
        :param auxi_characters: allowed letters in the transformation rule
        :param transformations: dictionary/list of transformation rules
        :return: transformations with the new rule
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
        return transformations

    def get_fitness(self, goal, method='convex'):
        """Returns the system's fitness compared to a goal system computed with the provided method.

        :param goal: tuple(LSystem, numpy_array)
        :param method: fitness measure ('convex', 'hu' or 'rms')
        :return: fitness of the system
        """
        assert isinstance(goal, tuple), "goal should be (goal_system, goal_asnumpy)"
        assert isinstance(method, str), f"method should be of type str, not {type(method)}"

        goal_system, goal_np = goal
        if method == 'convex':
            return fitness.convex_hull_defect_fitness(self.to_coords(), goal_system)
        elif method == 'hu':
            return fitness.calculate_hu_fitness(self.to_coords(), goal_np) * 100  # *100 to scale up the measure
        elif method == 'rms':
            return fitness.calculate_rms(self.to_numpy(), goal_np)
        else:
            raise ValueError(f"Requested fitness measure is {method}, but should be in ['hu', 'convex', 'rms].")

    def get_transformations(self):
        """Returns the current transformation rules.

        :return: current transformation rules
        """
        return self.transformations

    def replace_rule(self, key, rule):
        """Replace the transformation rule with key 'key' with a given 'rule'.

        :param key: dictionary key of a transformation rule
        :param rule: new transformation rule consequence"""
        self.transformations[key] = rule

    def set_transformations(self, trans):
        """Replace the current dictionary of transformation rules with a new one.

        :param trans: new dictionary of transformation rules
        """
        self.transformations = trans

    def to_numpy(self):
        """Turns the system's transformed sequence into plot coordinates and from there into a numpy array.

        :return: system's sequence as numpy array
        """
        x, y = self.to_coords()
        numpy_sol = utils.turn_coords_to_numpy(x, y)
        numpy_sol = np.reshape(numpy_sol[:, :, 0], (480, 640, 1))
        return numpy_sol

    def verify_system(self, msg=""):
        """
        Checks whether a sequence is correct.
        1. closing brackets must come after opening brackets
        Only runs in debug mode (see constants.py).

        :param msg: optional additional text for the error message
        """
        if debug:  # to be changed in constants.py
            sequence = self.transform_multiple(self.iterations)
            bracket_balance = 0
            for character in sequence:
                if character == '[':
                    bracket_balance += 1
                elif character == ']':
                    bracket_balance -= 1
                if bracket_balance < 0:
                    print(f"Resulting sequence of system is faulty:\n"
                                     f"\t- bracket_balance: {bracket_balance}\n"
                                     f"\t- axiom: {self.axiom}\n"
                                     f"\t- rules: {self.transformations}\n"
                                     f"\t- sequ.: {sequence}"+msg)
                    raise ValueError

    # def __str__(self):
    #     return f"LSystem axiom is '{self.axiom}', angle is {self.angle} and rules are '{self.transformations}'"

    def __repr__(self):
        """Prints the system representation in the format LSystem(axiom, angle, rules).
        Is called with print() if __str__() is not defined.

        :return: string representation of the system in the format LSystem(axiom, angle, rules)
        """
        return f"LSystem(axiom={self.axiom}, angle={self.angle}, rules={self.transformations})"
