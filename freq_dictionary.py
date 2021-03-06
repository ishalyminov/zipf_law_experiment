import nltk.corpus
import nltk.tokenize
import collections
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(parentdir, 'associative_text_model'))
import text_model
import link_lexemes
import common

import dict_config

DEFAULT_LANGUAGE = 'russian'

# converting text into a sequence of sequences of words
def tokenize_text(in_sentences):
    sentences = []
    for sentence in in_sentences:
        sentence_tokens = nltk.tokenize.wordpunct_tokenize(sentence)
        sentences.append([token for token in sentence_tokens])
    return sentences

def build_freq_dictionary(in_sentences, in_dict_type):
    dictionary = build_stopped_freq_dictionary(in_sentences)
    if in_dict_type == 's_dict':
        return dictionary
    elif in_dict_type == 'fs_dict':
        result_dict = {word:count for (word, count) in dictionary.iteritems() if count > 1}
        return result_dict
    elif in_dict_type == 'raw_dict':
        return build_raw_freq_dictionary(in_sentences)
    elif in_dict_type == 'assoc_power_dict':
        return build_associative_power_dictionary(in_sentences)
    elif in_dict_type == 'assoc_model_dict':
        assoc_model = text_model.AssociativeModel(in_sentences, DEFAULT_LANGUAGE)
        return text_model.get_freq_dict(assoc_model)


def build_raw_freq_dictionary(in_tokenized_sentences):
    result = collections.defaultdict(lambda: 0)
    for sentence in in_tokenized_sentences:
        for token in sentence:
            result[token] += 1
    return result

# making a frequency dictionary from a word sequence with stopwords filtering
def build_stopped_freq_dictionary(in_tokenized_sentences, in_language = DEFAULT_LANGUAGE):
    result = collections.defaultdict(lambda: 0)
    stopped_sentences = common.stop(in_tokenized_sentences, in_language)
    for sentence in stopped_sentences:
        for token in sentence:
            result[token.lower()] += 1
    return result

# making a frequency dictionary based on the full link set extraction
def build_full_link_set_dictionary(in_tokenized_sentences, in_language = DEFAULT_LANGUAGE):
    stopped_sentences = common.stop(in_tokenized_sentences, in_language)
    full_link_set = link_lexemes.extract_full_link_set(stopped_sentences, True)
    result = collections.defaultdict(lambda: 0)
    for lexeme in full_link_set:
        result[lexeme[0]] = lexeme[1]
    return result

def build_associative_power_dictionary(in_tokenized_sentences, in_language = DEFAULT_LANGUAGE):
    stopped_sentences = common.stop(in_tokenized_sentences, in_language)
    filtered_sentences = []
    # we need filtered sentences 1) not to contain stop words, 2) not to contain 1-freq. words
    for sentence in stopped_sentences:
        filtered_sentence = [word for word in sentence]
        filtered_sentences.append(filtered_sentence)

    associative_power_dict = collections.defaultdict(lambda: set([]))
    for sentence in filtered_sentences:
        for index in xrange(len(sentence)):
            word = sentence[index]
            if index != 0:
                associative_power_dict[word].add(sentence[index - 1])
            if index != len(sentence) - 1:
                associative_power_dict[word].add(sentence[index + 1])
    result_dict = {word: len(context) for (word, context) in associative_power_dict.iteritems()}
    return result_dict

