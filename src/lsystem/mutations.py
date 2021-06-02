# general imports
import random
import numpy as np
# local imports
from src.constants import LETTER_STRING


def change_letter(transformations, key, index):
    """
    The character at transformations[key][index] is a letter
    """
    new_letter = random.choice(LETTER_STRING).upper()

    list_conversion = list(transformations[key])
    list_conversion[index] = new_letter
    transformations[key] = "".join(list_conversion)

    # transformations[key][index] = new_transformation

    # if a new letter is added to the dict values that is not already a key, add it to the dict
    if new_letter not in transformations:
        transformations[new_letter] = transformations[key]  # CHANGE HERE
    return transformations


def remove_branch(transformations, key, index, is_open_bracket):
    """
    The character at transformations[key][index] is a bracket
    Removes a branch in a transformation rule.
    """
    list_conversion = list(transformations[key])

    loop_list = list_conversion[index:]
    if not is_open_bracket:
        loop_list = list_conversion[:index+1][::-1]

    index_2 = index
    bracket_counter = 0
    for idx, ch in enumerate(loop_list):
        bracket_counter += 1 if ch == '[' else 0  # should +1 at index_left
        bracket_counter -= 1 if ch == ']' else 0
        if bracket_counter == 0:
            index_2 += idx if is_open_bracket else -idx
            break
    if index_2 == index:
        raise ValueError(f"Something is wrong with the transformation rule: {transformations[key]}")

    list_conversion[index] = ''
    list_conversion[index_2] = ''

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

        index_right = np.random.randint(index_left+1, len(transformations[key])+2)
        # in case empty branches are allowed index+1

        list_conversion.insert(index_right, "]")

        transformations[key] = "".join(list_conversion)
        return transformations


def remove_plus_minus(transformations, key, index):
    """
    The character at transformations[key][index] is a plus or minus,
    Removes the character
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
