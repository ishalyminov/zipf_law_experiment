import xml.sax
import sys
import operator
import os
import shutil

from text_reading import ruscorpora
import freq_dictionary
import plotting
import matplotlib.pyplot as plot

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(parentdir, 'associative_text_model'))
import text_model
import dict_config
import critical_frequency_analysis
import numpy

GLOBAL_SENTENCES_STAT = {'sentence_counts':[], 'dominant_counts':[]}
GLOBAL_WORDS_STAT = {'word_counts':[], 'dominant_counts':[]}
GLOBAL_CRITICAL_FREQUENCY_ERROR_STAT = []

def write_words_chart(in_result_file_name, in_freq_dictionary, in_critical_freq):
    TOP_SIZE = 10
    sorted_dictionary = sorted(in_freq_dictionary.items(),
                               key=operator.itemgetter(1),
                               reverse=True)
    dominants = [(word, count) for (word, count) in sorted_dictionary
                    if count > in_critical_freq]
    non_dominants = [(word, count) for (word, count) in sorted_dictionary
                        if count <= in_critical_freq]
    non_dominants_top = non_dominants[:]
    out_file = open(in_result_file_name, 'w')
    print >>out_file, 'Dominant lexemes'
    print >>out_file, '================'
    for word_count in dominants:
        print >>out_file, '%s\t%d' % word_count
    print >>out_file, 'Top %d Non-dominant lexemes' % TOP_SIZE
    print >>out_file, '================'
    for word_count in non_dominants_top:
        print >>out_file, '%s\t%d' % word_count
    out_file.close()


def different_dictionaries_experiment(in_text_name, in_text_handler):
    for dictionary in dict_config.DICTS:
        freq_dict = freq_dictionary.build_freq_dictionary(in_text_handler.sentences, dictionary)
        critical_freq = text_model.calculate_critical_frequency(freq_dict)
        empirical_critical_freq = critical_frequency_analysis.get_empirical_critical_frequency(freq_dict.values())
        plot_filename = os.path.join('./plots_w_cr_%s' % dictionary, in_text_name + '.png')
        plotting.make_plot_with_critical_frequency(plot_filename, \
                                                   in_text_handler.text_info, \
                                                   freq_dict.values(), \
                                                   critical_freq)
        two_w_cr_plot_filename = os.path.join('./plots_two_w_cr_%s' % dictionary, in_text_name + '.png')
        plotting.make_plot_with_two_critical_frequencies(two_w_cr_plot_filename, \
                                                         in_text_handler.text_info, \
                                                         freq_dict.values(), \
                                                         critical_freq,
                                                         empirical_critical_freq)
        chart_filename = os.path.join('./charts_%s' % dictionary, in_text_name + '.txt')
        write_words_chart(chart_filename, freq_dict, critical_freq)

        if (dictionary == 'fs_dict'):
            dominant_lexemes = [lexeme for lexeme in freq_dict if freq_dict[lexeme] > critical_freq]
            GLOBAL_SENTENCES_STAT['sentence_counts'].append(int(in_text_handler.text_info['sentences']))
            GLOBAL_SENTENCES_STAT['dominant_counts'].append(len(dominant_lexemes))
            GLOBAL_WORDS_STAT['word_counts'].append(int(in_text_handler.text_info['words']))
            GLOBAL_WORDS_STAT['dominant_counts'].append(len(dominant_lexemes))
            critical_frequency_error = critical_frequency_analysis.get_critical_frequency_error(freq_dict)
            GLOBAL_CRITICAL_FREQUENCY_ERROR_STAT.append(critical_frequency_error)

def empirical_critical_frequency_experiment(in_text_name, in_text_handler):
    for dictionary in ['fs_dict', 'assoc_power_dict']:
        freq_dict = freq_dictionary.build_freq_dictionary(in_text_handler.sentences, dictionary)
        critical_freq = critical_frequency_analysis.get_empirical_critical_frequency(freq_dict.values())
        chart_filename = os.path.join('./charts_empirical_%s' % dictionary, in_text_name + '.txt')
        write_words_chart(chart_filename, freq_dict, critical_freq)

def process_file(in_source_name, in_text_name):
    parser = xml.sax.make_parser()
    handler = ruscorpora.RuscorporaAnnotatedTextParser(encode_to = 'utf-8')
    parser.setContentHandler(handler)
    parser.parse(in_source_name)

    different_dictionaries_experiment(in_text_name, handler)
    empirical_critical_frequency_experiment(in_text_name, handler)

def process_folder(in_root_folder):
    for root, dirs, files in os.walk(in_root_folder):
        for text_file in files:
            (name, ext) = os.path.splitext(text_file)
            if not ext in ['.xml', '.xhtml']:
                continue
            source_name = os.path.join(root, text_file)
            print >>sys.stderr, 'INFO: processing file %s' % source_name
            process_file(source_name, name)
    plot.scatter(GLOBAL_WORDS_STAT['word_counts'], GLOBAL_WORDS_STAT['dominant_counts'])
    plot.xlim(20000)
    plot.title('Word count - dominant lexemes number correlation')
    plot.savefig('./dominant_word_count_correlation.png')
    plot.clf()
    plot.scatter(GLOBAL_SENTENCES_STAT['sentence_counts'], GLOBAL_SENTENCES_STAT['dominant_counts'])
    plot.xlim(2000)
    plot.title('Sentence count - dominant lexemes number correlation')
    plot.savefig('./dominant_sentence_count_correlation.png')
    plot.clf()

    plotting.make_histogram('./crirical_freq_error.png', \
                            'Critical frequency error histogram', \
                            GLOBAL_CRITICAL_FREQUENCY_ERROR_STAT, \
                            in_normed = False)
    print 'Critical frequency error mean: ', numpy.mean(GLOBAL_CRITICAL_FREQUENCY_ERROR_STAT)
    print 'Critical frequency error variance: ', numpy.std(GLOBAL_CRITICAL_FREQUENCY_ERROR_STAT)

def prepare_folders():
    for dictionary in ['fs_dict', 'assoc_power_dict']:
        if os.path.exists('./charts_empirical_%s' % dictionary):
            shutil.rmtree('./charts_empirical_%s' % dictionary)
        os.mkdir('./charts_empirical_%s' % dictionary)

    for dictionary in dict_config.DICTS:
        plots_w_cr_folder_name = './plots_w_cr_%s' % dictionary
        plots_two_w_cr_folder_name = './plots_two_w_cr_%s' % dictionary
        charts_folder_name = './charts_%s' % dictionary
        if os.path.exists(plots_w_cr_folder_name):
            shutil.rmtree(plots_w_cr_folder_name)
        os.mkdir(plots_w_cr_folder_name)
        if os.path.exists(plots_two_w_cr_folder_name):
            shutil.rmtree(plots_two_w_cr_folder_name)
        os.mkdir(plots_two_w_cr_folder_name)
        if os.path.exists(charts_folder_name):
            shutil.rmtree(charts_folder_name)
        os.mkdir(charts_folder_name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: process_text.py <texts root folder>')
    prepare_folders()
    input_folder = sys.argv[1]
    process_folder(input_folder)
