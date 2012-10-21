import xml.sax

# raw text in ruscorpora is a set of paragraphs enclosed in <p> </p> tags
# and some <meta>-attributes in the header
class RuscorporaRawTextParser(xml.sax.handler.ContentHandler):
    def __init__(self, encode_to = None):
        self.within_sentence = False
        self.sentences = []
        self.char_buffer = ''
        self.output_encoding = encode_to

    def startElement(self, name, attrs):
        if name == 'p':
            self.within_sentence = True
            self.char_buffer = ''

    def endElement(self, name):
        if name == 'p':
            self.within_sentence = False
            if len(self.char_buffer):
                if self.output_encoding:
                    self.char_buffer = self.char_buffer.encode(self.output_encoding)
                self.sentences.append(self.char_buffer)
                self.char_buffer = ''

    def characters(self, ch):
        # only collect word forms char-by-char
        if self.within_sentence:
            self.char_buffer += ch

# annotated text is divided into sentences (<se> ... </se>); each sentence's raw words
# stored as raw text in its node
class RuscorporaAnnotatedTextParser(xml.sax.handler.ContentHandler):
    def __init__(self, encode_to = None):
        self.within_sentence = False
        self.within_word = False
        self.sentences = []
        self.words_buffer = []
        self.char_buffer = ''
        self.out_encoding = encode_to

    def startElement(self, name, attrs):
        if name == 'se':
            self.within_sentence = True
        if name == 'w':
            self.within_word = True

    def endElement(self, name):
        if name == 'w':
            self.within_word = False
            self.char_buffer = self.char_buffer.lower()
            if self.out_encoding:
                self.char_buffer = self.char_buffer.encode(self.out_encoding)
            if len(self.char_buffer):
                self.words_buffer.append(self.char_buffer)
            self.char_buffer = ''
        if name == 'se':
            self.within_sentence = False
            if len(self.words_buffer):
                self.sentences.append(self.words_buffer)
            self.words_buffer = []

    def characters(self, ch):
        # only collect word forms char-by-char
        if self.within_sentence and self.within_word:
            self.char_buffer += ch
