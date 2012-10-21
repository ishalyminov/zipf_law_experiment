import xml_processing
import freq_dictionary
import xml.sax
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage: process_text.py <text file name>')

    parser = xml.sax.make_parser()
    handler = xml_processing.RuscorporaAnnotatedTextParser()
    parser.setContentHandler(handler)
    parser.parse(sys.argv[1])
    sentences = handler.sentences

    for sentence in sentences:
        print ' '.join(sentence)
    raw_freq_dictionary = freq_dictionary.build_raw_freq_dictionary(sentences)
    stopped_freq_dictionary = freq_dictionary.build_stopped_freq_dictionary(sentences)
    fls_freq_dictionary = freq_dictionary.build_full_link_set_dictionary(sentences)
    #for key,value in stopped_freq_dictionary.iteritems():
    #    print key, ': ', value
    print len(raw_freq_dictionary)
    print len(stopped_freq_dictionary)
    print len(fls_freq_dictionary)
