import xml_processing
import freq_dictionary
import xml.sax
import sys
import operator
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, os.path.join(parentdir, 'associative_text_model'))
import model_builder

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: process_text.py <text file name>')

    parser = xml.sax.make_parser()
    handler = xml_processing.RuscorporaAnnotatedTextParser(encode_to = 'utf-8')
    parser.setContentHandler(handler)
    parser.parse(sys.argv[1])
    sentences = handler.sentences

    raw_freq_dictionary = freq_dictionary.build_raw_freq_dictionary(sentences)
    stopped_freq_dictionary = freq_dictionary.build_stopped_freq_dictionary(sentences)
    fls_freq_dictionary = freq_dictionary.build_full_link_set_dictionary(sentences)
    critical_freq = model_builder.calculate_critical_frequency(raw_freq_dictionary)
    for key, value in sorted(raw_freq_dictionary.items(), key=operator.itemgetter(1), reverse=True):
        print key, ': ', value
    print 'critical frequency for the text is: %d' % critical_freq
