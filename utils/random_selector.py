import random

def select_random_elements(elements, count=10):
    """
    Selects a random subset of elements from a given list.

    Args:
        elements (list): List of elements to choose from.
        count (int): Number of random elements to select.

    Returns:
        list: Randomly selected elements.
    """
    if len(elements) <= count:
        return elements
    return random.sample(elements, count)
