import xml.sax
import sys
import operator
import os

import xml_processing
import freq_dictionary
import plotting

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(parentdir, 'associative_text_model'))
import model_builder

def write_words_chart(in_result_file_name, in_freq_dictionary, in_critical_freq):
    TOP_SIZE = 10
    sorted_dictionary = sorted(in_freq_dictionary.items(),
                               key=operator.itemgetter(1),
                               reverse=True)
    dominants = [(word, count) for (word, count) in sorted_dictionary
                    if count > in_critical_freq]
    non_dominants = [(word, count) for (word, count) in sorted_dictionary
                        if count <= in_critical_freq]
    non_dominants_top = non_dominants[:TOP_SIZE]
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

def process_file(in_source_name, in_text_name):
    parser = xml.sax.make_parser()
    handler = xml_processing.RuscorporaAnnotatedTextParser(encode_to = 'utf-8')
    parser.setContentHandler(handler)
    parser.parse(in_source_name)
    sentences = handler.sentences
    raw_freq_dictionary = freq_dictionary.build_raw_freq_dictionary(sentences)
    stopped_freq_dictionary = freq_dictionary.build_stopped_freq_dictionary(sentences)
    fls_freq_dictionary = freq_dictionary.build_full_link_set_dictionary(sentences)
    critical_freq = model_builder.calculate_critical_frequency(raw_freq_dictionary)

    plot_filename = os.path.join('./plots_frequency_rank_stopped', in_text_name + '.png')
    plotting.make_plot(plot_filename, stopped_freq_dictionary.values(), critical_freq)
    chart_filename = os.path.join('./charts_frequency_rank_stopped', in_text_name + '.txt')
    write_words_chart(chart_filename, stopped_freq_dictionary, critical_freq)

def process_folder(in_root_folder):
    for root, dirs, files in os.walk(in_root_folder):
        for text_file in files:
            (name, ext) = os.path.splitext(text_file)
            if not ext in ['.xml', '.xhtml']:
                continue
            source_name = os.path.join(root, text_file)
            print >>sys.stderr, 'INFO: processing file %s' % source_name
            process_file(source_name, name)

def prepare_folders():
    if os.path.exists('./plots_frequency_rank_stopped'):
        os.path.rmdir('./plots_frequency_rank_stopped')
    if os.path.exists('./plots_frequency_rank_fls'):
        os.path.rmdir('./plots_frequency_rank_fls')
    if os.path.exists('./charts_frequency_rank_stopped'):
        os.path.rmdir('./charts_frequency_rank_stopped')
    if os.path.exists('./charts_frequency_rank_fls'):
        os.path.rmdir('./charts_frequency_rank_fls')
    os.mkdir('./plots_frequency_rank_stopped')
    os.mkdir('./plots_frequency_rank_fls')
    os.mkdir('./charts_frequency_rank_stopped')
    os.mkdir('./charts_frequency_rank_fls')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: process_text.py <text file name>')
    prepare_folders()
    input_folder = sys.argv[1]
    process_folder(input_folder)
