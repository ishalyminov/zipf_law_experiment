# coding:utf-8

import sys
import nltk
import plotting
import collections
import xml
import operator
import itertools
import os

from ruscorpora_ngrams import ngrams

STOPWORDS = nltk.corpus.stopwords.words('russian')


def count_map_to_array(in_count_map):
    result = []
    for statistic, count in in_count_map.items()[5:-5]:
        for appearance in xrange(count):
            result.append(statistic)
    return result


def count_words(in_text_root, in_output_file):
    ngrams.N = 1
    ngrams.WORDS = True
    count_map_file = open(in_output_file, 'w')
    print >>count_map_file, 'word;count;rank'
    for root, dirs, files in os.walk(os.path.abspath(in_text_root), followlinks=True):
        for filename in files:
            full_filename = os.path.join(root, filename)
            handler = ngrams.TextHandler()
            xml.sax.parse(full_filename, handler)
            for ngram, rank in zip(sorted(handler.ngrams.items(),
                                       key=operator.itemgetter(1),
                                       reverse=True),
                                   itertools.count()):
                word, count = ngram
                print >>count_map_file, '%s;%d;%d' % (word, count, rank)
        print >>count_map_file, ''
    count_map_file.close()


def make_plot(in_count_stream, in_mode, in_output_file):
    count_map = collections.defaultdict(lambda: 0)
    stop_count_map = collections.defaultdict(lambda: 0)
    for line in in_count_stream.readlines()[1:]:
        tokens = line.strip().split(';')
        if len(tokens) < 3:
            continue
        word, count, rank = tokens[0], int(tokens[1]), int(tokens[2])
        statistic = (count if in_mode == 'freq' else rank)
        if word not in STOPWORDS:
            count_map[statistic] += 1
        else:
            stop_count_map[statistic] += 1
    x_label = u'%s слова в документе' % (u'Частота' if in_mode == 'freq' else u'Ранг')
    y_label = u'Количество слов с %s' %\
              (u'данной частотой' if in_mode == 'freq' else u'данным рангом')
    histogram = plotting.Histogram(u'Распределение частот частот слов',
                                   x_label,
                                   y_label,
                                   in_output_file,
                                   normed=False,
                                   bins_number=50)
    word_count_points = count_map_to_array(count_map)
    histogram.add_histogram(word_count_points, label=u'Слова')
    if len(stop_count_map):
        stop_count_points = count_map_to_array(stop_count_map)
        histogram.add_histogram(stop_count_points, label=u'Стоп-слова')
    histogram.save()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: create_histogram.py <rank/freq> <texts root> <plot file>'
        exit(0)
    mode, text_root, output_file = sys.argv[1:4]
    temp_file_name = 'word_counts_per_docs.txt'
    count_words(text_root, temp_file_name)
    make_plot(open(temp_file_name), mode, output_file)
