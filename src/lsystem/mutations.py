# general imports
import random
import numpy as np
# local imports
from src.constants import LETTER_STRING


def point_mutation_transformation(transformations, key):
    """
    change the value of a transformation based on letter

    In this function we can add evolution strategies.
    I've just added a very simple evolutionary strategy that is not very stochastic or good.
    It just replaces the value of the first key with 'FA'
    """
    # generate the letter that we want to change and the letter to replace it with
    old_letter = random.choice(LETTER_STRING).upper()
    # old_letter = transformations[key]
    new_letter = random.choice(LETTER_STRING).upper()
    print(old_letter, new_letter)

    # point mutation-like change of transformation rules
    old_transformation = transformations[key]

    # replace by other letter(s) random duplication
    # transformations[key] = old_transformation.replace(old_letter, random.randint(0,4)*new_letter) #CHANGE HERE

    # replace by other letter(s) for random amount of times with random duplication
    nr_letter = old_transformation.count(old_letter)
    transformations[key] = old_transformation.replace(old_letter, random.randint(0, 4) * new_letter,
                                                      random.randint(0, nr_letter))  # CHANGE HERE

    # remove all old_letter values
    # transformations[key] = old_transformation.replace(old_letter, '') #CHANGE HERE

    # if a new letter is added to the dict values that is not already a key, add it to the dict
    if new_letter not in transformations:
        transformations[new_letter] = transformations[key] * 3  # CHANGE HERE
    return transformations


def change_letter(transformations, key, index):
    """
    the key is a letter
    """
    new_letter = random.choice(LETTER_STRING).upper()

    list_conversion = list(transformations[key])
    list_conversion[index] = new_letter
    transformations[key] = "".join(list_conversion)

    # transformations[key][index] = new_transformation

    # if a new letter is added to the dict values that is not already a key, add it to the dict
    if new_letter not in transformations:
        transformations[new_letter] = transformations[key] * 3  # CHANGE HERE
    return transformations


def remove_branch_left(transformations, key, index_left):
    """
    the key is a left bracket
    """
    list_conversion = list(transformations[key])
    # index_right = string_conversion.find(']')

    # we need to add the index from where it starts searching for the right bracket to the result
    start_index_right = len(transformations[key][:index_left])
    index_right = start_index_right + transformations[key][index_left:].index(']')
    # print(index_left, index_right)

    # remove the brackets
    list_conversion[index_right] = ''
    list_conversion[index_left] = ''

    transformations[key] = "".join(list_conversion)
    return transformations


def remove_branch_right(transformations, key, index_right):
    """
    the key is a right bracket
    """
    list_conversion = list(transformations[key])
    # index_left = string_conversion.find('[')

    index_left = transformations[key].index('[')
    print(index_left, index_right)

    # remove the brackets
    list_conversion[index_right] = ''
    list_conversion[index_left] = ''

    transformations[key] = "".join(list_conversion)
    return transformations


def add_branch(transformations, key, index_left):
    """
    transformations: the set of rules
    key: the key of the rule that is currently being altered
    index: starting index of the new branch

    Adds a new pair of brackets, starting at index given as the parameter, and ending at a random index
    within the string, right to the start of the branch
    """
    if index_left <= len(transformations[key]):  # <= if empty branches allowed
        list_conversion = list(transformations[key])
        list_conversion.insert(index_left, "[")

        index_right =  np.random.randint(index_left+1, len(transformations[key])+2)
        # in case empty branches are allowed index+1

        list_conversion.insert(index_right,"]")

        transformations[key] = "".join(list_conversion)
        return transformations


def remove_plus_minus(transformations, key, index):
    """
    the key is a plus or minus, remove the character
    """
    list_conversion = list(transformations[key])

    # remove the character
    list_conversion[index] = ''

    transformations[key] = "".join(list_conversion)
    return transformations


def add_plus_minus(transformations, key, index):
    """
    add a plus or a minus
    """
    list_conversion = list(transformations[key])

    list_conversion.insert(index+1, random.choice(["+", "-"]))

    transformations[key] = "".join(list_conversion)
    return transformations
