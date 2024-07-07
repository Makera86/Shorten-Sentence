import re

def remove_specific_words_and_backslash(sentence):
    # Define the pattern to match whole words 'in' or 'the', and backslashes
    pattern = r'\b(the|in|on|my)\b\s*|\\'

    # Replace the matched words and backslashes with an empty string
    filtered_sentence = re.sub(pattern, '', sentence, flags=re.IGNORECASE)

    return filtered_sentence

