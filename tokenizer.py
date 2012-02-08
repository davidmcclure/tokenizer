import re

class Tokenizer(object):

    '''
    Splits a text file into an ordered list of words.
    '''

    # List of punctuation characters to scrub. Omits the single apostrophe,
    # which is handled separately so as to retain contractions.
    PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*', "'"]

    # Carriage return strings, on *nix and windows.
    CARRIAGE_RETURNS = ['\n', '\r\n']

    # Final sanity-check regex to run on words before they get pushed onto the
    # core words list.
    WORD_REGEX = "^[a-z']+$"


    def __init__(self, raw):
        '''
        Set raw source, build contractions list, initialize empty lists for lines
        and words, call tokenize.
        '''
        self.raw = raw
        self.words = []
        self.tokenize()


    def _clean_word(self, word):
        '''
        Parses a space-delimited string from the text and determines whether or
        not it is a valid word. Scrubs punctuation, retains contraction
        apostrophes. If cleaned word passes final regex, returns the word;
        otherwise, returns None.

        - param string word: The word.

        - return string word: The cleaned word. None if the passed string
          cannot be resolved down to a valid word.
        '''
        word = word.lower()
        for punc in Tokenizer.PUNCTUATION + Tokenizer.CARRIAGE_RETURNS:
            word = word.replace(punc, '')
        if not re.match(Tokenizer.WORD_REGEX, word): word = None
        return word


    def tokenize(self):
        '''
        Split file into an ordered list of words. Scrub out punctuation;
        lowercase everything; preserve contractions; disallow strings that
        include non-letters. En route, build a dictionary of {word: count}.
        '''
        self.word_counts_dictionary = {}
        self.total_wordcount = 0
        words = self.raw.split(' ')
        for word in words:
            clean_word = self._clean_word(word)
            if clean_word:
                self.total_wordcount += 1
                self.words.append(clean_word)
                try: self.word_counts_dictionary[clean_word] += 1
                except KeyError: self.word_counts_dictionary[clean_word] = 1
