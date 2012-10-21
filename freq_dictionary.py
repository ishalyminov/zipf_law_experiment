import nltk.corpus
import nltk.tokenize
import collections
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(parentdir, 'associative_text_model'))
import link_lexemes
import model_builder

DEFAULT_LANGUAGE = 'russian'

# converting text into a sequence of sequences of words
def tokenize_text(in_sentences):
    sentences = []
    for sentence in in_sentences:
        sentence_tokens = nltk.tokenize.wordpunct_tokenize(sentence)
        sentences.append([token for token in sentence_tokens])
    return sentences

# making a frequency dictionary from a word sequence
def build_raw_freq_dictionary(in_tokenized_sentences):
    result = collections.defaultdict(lambda: 0)
    for sentence in in_tokenized_sentences:
        for token in sentence:
            result[token] += 1
    return result

# making a frequency dictionary from a word sequence with stopwords filtering
def build_stopped_freq_dictionary(in_tokenized_sentences, in_language = DEFAULT_LANGUAGE):
    result = collections.defaultdict(lambda: 0)
    stopped_sentences = model_builder.stop(in_tokenized_sentences, in_language)
    for sentence in stopped_sentences:
        for token in sentence:
            result[token.lower()] += 1
    return result

# making a frequency dictionary based on the full link set extraction
def build_full_link_set_dictionary(in_tokenized_sentences, in_language = DEFAULT_LANGUAGE):
    stopped_sentences = model_builder.stop(in_tokenized_sentences, in_language)
    full_link_set = link_lexemes.extract_full_link_set(stopped_sentences, True)
    result = collections.defaultdict(lambda: 0)
    for lexeme in full_link_set:
        result[lexeme[0]] = lexeme[1]
    return result
