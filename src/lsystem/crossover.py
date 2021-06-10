import copy
import random


def cross_over(parent_a, parent_b, children):
    # find matching keys
    rules_a = parent_a.get_transformations()
    rules_b = parent_b.get_transformations()
    matches = set(rules_a.keys()) & set(rules_b.keys())
    if matches:
        chosen_key = random.choice(list(matches))

        # swap matching rules
        child_a = copy.deepcopy(parent_a)
        child_b = copy.deepcopy(parent_b)
        child_a.replace_rule(chosen_key, rules_b[chosen_key])
        child_b.replace_rule(chosen_key, rules_a[chosen_key])

        # add children
        children.append(child_a)
        children.append(child_b)
    else:
        chosen_key_a = random.choice(list(rules_a.keys()))
        chosen_key_b = random.choice(list(rules_b.keys()))

        # swap matching rules
        child_a = copy.deepcopy(parent_a)
        child_b = copy.deepcopy(parent_b)
        child_a.replace_rule(chosen_key_b, rules_b[chosen_key_b])
        child_b.replace_rule(chosen_key_a, rules_a[chosen_key_a])

        # add children
        children.append(child_a)
        children.append(child_b)
