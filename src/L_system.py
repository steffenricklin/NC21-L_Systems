"""
"""
# general imports
import matplotlib.pyplot as plt
plt.style.use('bmh')  # Use some nicer default colors
import random
from math import isnan
from math import pi, sin, cos
import numpy as np
import cv2  # to install: apt-get install -y python3-opencv
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from PIL import Image

# local imports
import src.utils
from src.constants import LETTER_STRING


class LSystem:
    """
    Represents the production rules and provides functions for changing
    the production rule strings
    """
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.transformations = rules
        self.sequence = axiom

    def point_mutation_transformation(self, transformations, key):
        '''
        change the value of a transformation based on letter

        In this function we can add evolution strategies. 
        I've just added a very simple evolutionary strategy that is not very stochastic or good. 
        It just replaces the value of the first key with 'FA'
        '''
        # generate the letter that we want to change and the letter to replace it with
        old_letter = random.choice(LETTER_STRING).upper()
        #old_letter = transformations[key]
        new_letter = random.choice(LETTER_STRING).upper()
        print(old_letter, new_letter)
                
        # point mutation-like change of transformation rules
        old_transformation = transformations[key]
                
        # replace by other letter(s) random duplication
        #transformations[key] = old_transformation.replace(old_letter, random.randint(0,4)*new_letter) #CHANGE HERE
                
        # replace by other letter(s) for random amount of times with random duplication
        nr_letter = old_transformation.count(old_letter)
        transformations[key] = old_transformation.replace(old_letter, random.randint(0,4)*new_letter, random.randint(0, nr_letter)) #CHANGE HERE
                
        # remove all old_letter values
        #transformations[key] = old_transformation.replace(old_letter, '') #CHANGE HERE
                
        # if a new letter is added to the dict values that is not already a key, add it to the dict
        if new_letter not in transformations: 
            transformations[new_letter] = transformations[key] *3 #CHANGE HERE

    def change_letter(self, transformations, key, index):
        '''
        the key is a letter
        '''
        new_letter = random.choice(LETTER_STRING).upper()

        list_conversion = list(transformations[key])
        list_conversion[index] = new_letter
        transformations[key] = "".join(list_conversion)

        #transformations[key][index] = new_transformation

        # if a new letter is added to the dict values that is not already a key, add it to the dict
        if new_letter not in transformations: 
            transformations[new_letter] = transformations[key] *3 #CHANGE HERE

    def remove_branch_left(self, transformations, key, index_left):
        '''
        the key is a left bracket
        '''

        list_conversion = list(transformations[key])
        #index_right = string_conversion.find(']')
        index_right = list_conversion.index(']')

        # remove the brackets
        list_conversion[index_left] = ''
        list_conversion[index_right] = ''

        transformations[key] = "".join(list_conversion)
    
    def remove_branch_right(self, transformations, key, index_right):
        '''
        the key is a right bracket
        '''
        list_conversion = list(transformations[key])
        #index_left = string_conversion.find('[')
        index_left = list_conversion.index('[')

        # remove the brackets
        list_conversion[index_right] = ''
        list_conversion[index_left] = ''

        transformations[key] = "".join(list_conversion)

    def add_branch(self, transformations, key, index_left):
        '''
        transformations: the set of rules
        key: the key of the rule that is currently being altered
        index: starting index of the new branch

        Adds a new pair of brackets, starting at index given as the parameter, and ending at a random index 
        within the string, right to the start of the branch
        '''
        if index_left < len(transformations[key]): #<= if empty branches allowed
            list_conversion = list(transformations[key])
            list_conversion.insert(index_left, "[")

            index_right =  np.random.randint(index_left+2, len(transformations[key])+2)
            #in case empty branches are allowed index+1

            list_conversion.insert(index_right,"]")

        transformations[key] = "".join(list_conversion)

    def remove_plus_minus(self, transformations, key, index):
        '''
        the key is a plus or minus, remove the character
        '''
        list_conversion = list(transformations[key])

        # remove the character
        list_conversion[index] = ''

        transformations[key] = "".join(list_conversion)

    def add_plus_minus(self, transformations, key, index):
        raise NotImplementedError

    def evolve_transformations(self, p):
        '''
        loops over the transformations and changes them 
        '''
        keys = list(self.transformations.keys())
        # loop over keys from transformations dict and change the value of that key with chance p
        for i in range(len(keys)):
            rndm = random.random()
            if rndm > p: 
                key = keys[i]
                
                #point_mutation_transformation(self.transformations, key)

                # get random index in self.transformations key and change that
                index = random.randint(0, len(self.transformations[key])-1)
                value = self.transformations[key][index]

                #insert
                if rndm >= 0.95:
                    self.add_branch(self.transformations, key, index)

                #change existing characters
                elif value.isalpha(): self.change_letter(self.transformations, key, index)

                #remove existing characters
                elif value == '[' : self.remove_branch_left(self.transformations, key, index)
                elif value == ']' : self.remove_branch_right(self.transformations, key, index)
                elif value == '+' or '-' : self.remove_plus_minus(self.transformations, key, index)

                else: pass
                
        return self.transformations

    def transform_sequence(self):
        return ''.join(self.transformations.get(c, c) for c in self.sequence)

    def transform_multiple_evolve(self, iterations, p):
        '''Tranforms for multiple iterations'''
        for _ in range(iterations):
            self.transformations = self.evolve_transformations(p)
            self.sequence = self.transform_sequence()
        return self

    def transform_multiple(self, iterations):
        '''Tranforms for multiple iterations'''
        for _ in range(iterations):
            self.sequence = self.transform_sequence()
        return self
    
    def showImage():
        X,Y = get_coords(self.transformations)
        im_nump = turn_coords_to_numpy(X,Y)
        img = Image.fromarray(im_nump, 'RGB')
        img.show()



