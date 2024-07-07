# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 07:07:58 2023

@author: msi
"""
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize
from nltk import StanfordTagger
import stanza #Last version
from collections import OrderedDict
from Modify_Sentence import modify_sentence
from Determine_Aspect import determine_aspect
from remove_specific_words import remove_specific_words_and_backslash
# Download and set up the Stanford CoreNLP client
stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
client = stanza.Pipeline('en')
x=0
def is_adjective(word):
    """
    Check if the input word is an adjective.
    Returns 1 if the word is an adjective, otherwise 0.

    Args:
    word (str): The word to check.

    Returns:
    int: 1 if the word is an adjective, 0 otherwise.
    """
    # Process the word
    doc = nlp(word)

    # Check if the word is an adjective
    for sent in doc.sentences:
        for word in sent.words:
            if word.xpos in ['JJ', 'JJR', 'JJS']:
                return 1
    return 0
def is_nouns(word):
    """
    Check if the input word is an adjective.
    Returns 1 if the word is an adjective, otherwise 0.

    Args:
    word (str): The word to check.

    Returns:
    int: 1 if the word is an adjective, 0 otherwise.
    """
    # Process the word
    doc = nlp(word)

    # Check if the word is an adjective

    for sent in doc.sentences:
        for word in sent.words:
            if word.xpos in ['NNh', 'NNSh' , 'NNPh']:
                return 1
    return 0
def parse_sentence(input_sentence, aspect_word,wordd,distan):
    # Process the input sentence using the pipeline
    doc = client(input_sentence)
    dst=60
    aa=0
    aspect_word1=aspect_word
    rm="popopo"
    # Variables to hold related words and their indices
    related_words = []
    related_indices = []
    tokens = []

    # Iterate through sentences (assuming one sentence for simplicity)
    for sent in doc.sentences:
        aspect_found = False
        aspect_id = None

        # Find the aspect word and store its ID
        for index, word in enumerate(sent.words):
            if word.text.lower() == aspect_word.lower():
                aspect_found = True
                aspect_id = word.id
                related_words.append(word.text)  # Include aspect word itself
                related_indices.append(index)
                break

        if aspect_found:
            # Check if the aspect word is a head

            if any(dependent.head == aspect_id for dependent in sent.words) :  # Aspect is a head
                # Collect all dependencies of the aspect
                for dependent in sent.words:

                    tokens = []
                    tokens.append(dependent.text)
                    words = nltk.pos_tag(tokens)
                    head_word = sent.words[dependent.head - 1].text if dependent.head > 0 else "ROOT"
                    print(head_word, 'AA', dependent.deprel, 'oooooooooooooooooooooooooooooooooooooooooo')
                    if (dependent.head == aspect_id) and  (dependent.deprel != 'conj') and (dependent.deprel != 'case') and (dependent.deprel != 'nmod') and (dependent.deprel != 'compound') and (dependent.deprel != 'cc'):
                    #if (dependent.head == aspect_id)and(is_nouns(dependent.text)==0) :
                        x=0
                        related_words.append(dependent.text)
                        related_indices.append(dependent.id - 1)
                        # Collect heads of these dependencies
                        #print(dependent.text,'AA' ,dependent.deprel, 'oooooooooooooooooooooooooooooooooooooooooo')
                        if dependent.id in [w.head for w in sent.words] : #and (dependent.deprel != 'compound'):
                            for head in sent.words:
                                if head.head == dependent.id:
                                    print(dependent.deprel,'DSDS')
                                    related_words.append(head.text)
                                    related_indices.append(head.id - 1)
                
            list_example = aspect_word1.split()
            #converted_string = ' '.join(related_indices)
            if list_example==related_words:
                aa=1

            
            if(aa==1):
                # Collect the head of the aspect
                x=0
                if aspect_id > 0:
                    head_word = sent.words[aspect_id - 1].head
                    head_word = sent.words[head_word - 1] if head_word > 0 else None
                    #if head_word:
                    if head_word and(is_nouns(head_word.text)==0):
                        related_words.append(head_word.text)
                        related_indices.append(head_word.id - 1)
                        # Collect all dependents of the head of the aspect
                        for dependent in sent.words:
                            if dependent.head == head_word.id and dependent.deprel != 'conj' and dependent.deprel != 'nmod':
                            #if (dependent.head == head_word.id)and(is_nouns(dependent.text)==0):
                                related_words.append(dependent.text)
                                related_indices.append(dependent.id - 1)


            unique_words = OrderedDict((word, None) for _, word in sorted(zip(related_indices, related_words), key=lambda pair: pair[0]))#added

            s=" ".join(unique_words.keys())
            print("Sentence ",related_words)
            rmv = []

            tokens = nltk.word_tokenize(s)
            words = nltk.pos_tag(tokens)
           
            for g in s.split() :
                for i in words:

                  bb=is_adjective(str(i[0]))
                  if str(i[0])==str(g) and bb==1:

                      for k,h in zip(wordd,distan):
                          if k==str(i[0]):

                              if h < dst:
                                  rmv.append(rm)
                                  rm=k
                                  dst=h
                              else:
                                  rmv.append(k)






            print("the words that will remove " ,rmv)
            s=s.split()
            filtered_sentence = ' '.join([word for word in s if word not in rmv])
            print(filtered_sentence)
            return(filtered_sentence)

def build_dependency_tree(sentence):
    nlp = stanza.Pipeline('en')
    doc = nlp(sentence)

    tree_map = {}
    words_list = []
    for sent in doc.sentences:
        for word in sent.words:
            tree_map[word.id - 1] = word.head - 1
            words_list.append(word.text)

    return tree_map, words_list

def calculate_edge_distance(tree_map, source_node, target_node):
    if source_node == target_node:
        return 0

    # Convert tree_map to a bi-directional graph
    graph = {}
    for child, parent in tree_map.items():
        if parent >= 0:
            graph.setdefault(child, []).append(parent)
            graph.setdefault(parent, []).append(child)

    # BFS to find shortest path
    visited = set()
    queue = [(source_node, 0)]
    while queue:
        current, distance = queue.pop(0)
        if current == target_node:
            return distance
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get(current, []):
                queue.append((neighbor, distance + 1))

    return float('inf')
def F_distance(sentence,aspect_word):
    #sentence = "The food is surprisingly good, and the decor is nice."
    #aspect_word = "decor"
    distan= []
    wordd = []
    tree_map, words_list = build_dependency_tree(sentence)

    aspect_word_index = None
    for index, word in enumerate(words_list):
        if word.lower().strip(".,?!") == aspect_word.lower():
            aspect_word_index = index
            break

    if aspect_word_index is not None:
        distances = {}
        for node in range(len(words_list)):
            distance = calculate_edge_distance(tree_map, aspect_word_index, node)
            distances[words_list[node]] = distance if distance != float('inf') else 'No path'

        for word, distance in distances.items():
            print(f"Distance from '{aspect_word}' to '{word}': {distance}")
            distan.append(distance)
            wordd.append(word)

    else:
        print(f"The aspect word '{aspect_word}' was not found in the sentence.")
    return (wordd,distan)

# Example usage
#input_sentence = "Coffee is a better deal than overpriced Cosi sandwiches ."
#aspect_word = "Coffee"
#input_sentence = "The falafal was rather over cooked and bad but the cheken was fine ."
#aspect_word = "falafal"
#input_sentence = " Its size is ideal and the weight is acceptable ."
#aspect_word = "size"
#input_sentence = "mojitos and  service are the best part in there."
#aspect_word = "service"
#input_sentence="food is good but service is bad"
#aspect_word="food"
#input_sentence = "Certainly not the best sushi in New York , however , it is always fresh , and the place is very clean , sterile ."
#aspect_word = "sushi"
#input_sentence = " chicken was completely dried out and on the cold side and the sauce was not very flavorful ."
#aspect_word = "sauce"
#input_sentence = "fast ,   great screen  , beautiful  apps  for a laptop ; priced at 1100 on the apple website ; amazon had it for 1098 + tax - plus i had a 10 % off coupon from amazon-cost me 998 plus tax - 1070 -"
#aspect_word = "screen"
#input_sentence="Having heard from friends and family about how reliable a Mac product is , I never expected to have an application crash within the first month , but I did"
#aspect_word="application"
#input_sentence = "The Mac mini is about 8x smaller than my old computer which is a huge bonus and runs very quiet , actually the fans are n't audible unlike my old pc"
#aspect_word = "fans"
#input_sentence = "Had a great experience at Trio ... staff was pleasant; food was tasty and large in portion size - I would highly recommend the portobello gorgonzola sausage appetizer and the lobster risotto ."
#input_sentence="Had a great experience at Trio ... staff was pleasant; food was tasty or large in portion size - I would highly recommend   risotto."
#aspect_word = 'lobster risotto '
#input_sentence= "It is really thick around the battery ."
#aspect_word='battery' 
input_sentence = "Did not like the new Android version and the new navigation bar feature" 
aspect_word = "Android version"
n11=input_sentence
g=aspect_word
aspect_word= determine_aspect(aspect_word)

input_sentence = input_sentence.replace(g, aspect_word)

a = remove_specific_words_and_backslash(input_sentence)
a=modify_sentence(aspect_word,a)
#a = a.replace('and','and1')
input_sentence=a

wordd,distan=F_distance(input_sentence, aspect_word)

Last=parse_sentence(input_sentence, aspect_word,wordd,distan)
print(Last,'tttt')
sub_sentence= str(Last)+" " +g
original_sentence=n11
print(process_sub_sentence(original_sentence, sub_sentence))




