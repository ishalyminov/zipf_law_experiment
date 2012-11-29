import sys
import os
import collections
import operator

def read_dominants(in_file_name):
    lines = open(in_file_name).readlines()
    result = []
    # the first 2 are headers
    for line in lines[2:]:
        if line.strip() == 'Top 10 Non-dominant lexemes':
            break
        result.append(line.strip().split('\t'))
    return result



def process_folder(in_root_folder):
    lexemes_bag = collections.defaultdict(lambda: 0)

    for root, dirs, files in os.walk(in_root_folder):
        for text_file in files:
            for lexeme in read_dominants(os.path.join(root, text_file)):
                lexemes_bag[lexeme[0]] += int(lexeme[1])
    return lexemes_bag

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: extract_representative_lexemes.py <input_folder>')
    words_bag = process_folder(sys.argv[1])
    for (word, freq) in sorted(words_bag.items(), key=operator.itemgetter(1), reverse=True)[:10]:
        print '%s\t%s' % (word, freq)
