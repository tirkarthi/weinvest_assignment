from __future__ import print_function
import string
import re
from itertools import product
from collections import defaultdict


def find_optimal_word(number, dictionary):
    '''
    Accepts a number and a dictionary of the form as below to return the appropriate word for the number

    Dictionary form : 

    dictionary[keypad_sequence] = [words]

    dictionary[2255] = ['call', 'ball']
    dictionary[63]   = ['me', 'of']
    '''
    length = len(number)
    results = []
    words = dictionary.get(int(number), None)

    # Make a direct check for the entire word before splitting up
    if words is not None:
        results.extend(words)
        return set(map(lambda x: x.upper(), results))

    for i in range(length - 1):
        right = number[i + 1:]
        left = number[:i]

        if left:
            left = int(left)

        left_res = dictionary.get(left, None)

        # In some cases just the first digit needs to be taken off and everything works fine
        # Since the next if keeps the bad number at the head we just take it off and check
        # 92255 -> 9CALL
        if i == 0 and right and dictionary.get(int(right), None):
            results.extend(
                str(number[i]) + x for x in dictionary.get(int(right), []))

        if left and left_res:
            for l in left_res:
                for r in find_optimal_word(str(right), dictionary):
                    results.append(l + str(number[i]) + r)

    # Filter out the results with two numbers in a row
    pattern = re.compile(r'\d{2,}')
    return set(map(lambda y: y.upper(), filter(lambda x: not pattern.search(x), results)))


def find_all_sequences(number, dictionary):

    def product_set(number, dictionary):
        '''
        Returns a product set of all the words joined by - for the phone number sequence
        Numbers are split by . as per the document
        Star in fron of the map to make the output slurpy for the product generator

        2255.63
        2255 - Gives CALL, BALL
        63   - Gives ME, OF
        returns CALL-ME, CALL-OF, BALL-ME, BALL-OF
        '''
        return list(map(lambda x: '-'.join(x), product(*map(lambda x: find_optimal_word(x, dictionary), number.split('.')))))

    return product_set(number, dictionary)


def word_to_number(word, dial_pad_mapper):
    '''
    Return the dialpad sequence for the given word
    '''

    lstr = str
    return int(''.join([lstr(dial_pad_mapper.get(char, 0)) for char in list(word)]))


def strip_whitespace_punctuation(word):
    '''
    Strip all whitespace and punctuation. Don't replace '.'

    http://stackoverflow.com/a/266162
    http://stackoverflow.com/a/3739928
    '''
    punctuation_regex = re.compile('[%s]' % re.escape(string.punctuation.replace('.', '')))
    whitespace_regex  = re.compile(r'\s+')

    word = punctuation_regex.sub('', word)
    word = whitespace_regex.sub('', word)

    return word


def generate_dictionary(file):
    '''
    Return a dictionary with keypad sequence for the word as the key and the list of words as the value
    '''

    chars = list(string.ascii_lowercase)
    dial_pad_numbers = [x for x in range(2, 11) for _ in range(3)]
    dial_pad_mapper = dict(zip(chars, dial_pad_numbers))

    # Some changes as per the dialpad
    dial_pad_mapper['s'] = 7
    dial_pad_mapper['v'] = 8
    dial_pad_mapper['y'] = 9
    dial_pad_mapper['z'] = 9

    dictionary = defaultdict(list)

    with open(file) as f:
        for word in f:
            word = word.strip().lower()
            word = strip_whitespace_punctuation(word)
            number = word_to_number(word, dial_pad_mapper)
            dictionary[number].append(word)
    return dictionary

def process_input(file, dictionary, is_file=True):

    for line in file:
        line = line.strip()
        line = strip_whitespace_punctuation(line)
        seqs = find_all_sequences(line, dictionary)
        if seqs:
            print(seqs)
        else:
            print("")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Return the word-sequences for the given input.')
    parser.add_argument('files', metavar='File', nargs='*')
    parser.add_argument('-d', '--dictionary', help='Specify the dictionary file', action='store', dest='dictionary_file')

    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    if args.dictionary_file:
        dictionary = generate_dictionary(args.dictionary_file)
    else:
        print("Specify a dictionary file with relative path")
        exit()

    # Look for files and if not present then process the input
    if args.files:
        for file in args.files:
            with open(file) as f:
                process_input(f, dictionary)
    else:
        process_input(sys.stdin, dictionary)
