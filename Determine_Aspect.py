#Multi word aspect
def determine_aspect(aspect_phrase):
    """
    Determine the main aspect from a phrase based on specific rules.

    Args:
    aspect_phrase (str): The phrase containing the aspect, which can be multiple words.

    Returns:
    str: The main aspect word determined based on the presence of the word "of".
    """
    # Split the phrase into a list of words
    words = aspect_phrase.split()

    # Check if "of" is in the list and determine the main aspect accordingly
    if 'of' in words:
        # Find the index of 'of' and choose the word immediately before it
        of_index = words.index('of')
        return words[of_index - 1] if of_index > 0 else words[0]
    else:
        # Choose the last word if "of" is not present
        return words[-1]

