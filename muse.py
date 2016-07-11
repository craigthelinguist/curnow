__author__ = 'craig'

# Requires the averaged_perceptron_tagger & punkt models.
from nltk import word_tokenize, pos_tag
# Requires the CMU corpus.
from nltk.corpus import cmudict

from collections import defaultdict
from string import digits

ARPABET = ["AA", "AE", "AH", "AO", "AW", "AY", "B", "CH", "D", "DH", "EH", "ER", "EY", "F", "G", "HH",
           "IH", "IY", "JH", "K", "L", "M", "N", "NG", "OW", "OY", "P", "R", "S", "SH", "T", "TH", "UH",
           "V", "W", "Y", "Z", "ZH"]

FEET = {
    "iambic": [False, True],
    "trochaic": [True, False],
    "dactylic": [True, False, False],
    "anapestic": [False, False, True],
    "bacchiatic": [False, True, True],
    "antibacchiatic": [True, True, False],
    "cretic": [True, False, True]
}


class Muse(object):

    PHONEMES = 0
    STRESSES = 1
    SYLLABLES = 2
    _cmudict = None

    def __init__(self):
        self._cmudict = cmudict.dict()
        self.muse = defaultdict(lambda x : None)
        for word in self._cmudict.keys():
            pronounciation = self._cmudict[word.lower()][0]
            phonemes = [ph.rstrip(digits) for ph in pronounciation]
            stresses = [0 if not ph[-1].isdigit() else int(ph[-1]) for ph in pronounciation]

            syllables, sy = [], ""
            for ph, st in zip(phonemes, stresses):
                if st and sy != "":
                    syllables.append(sy)
                    sy = ph
                else:
                    sy += ph
            if sy != "":
                syllables.append(sy)

            self.muse[word] = (phonemes, stresses, syllables)

    def phonemes(self, word):
        return self.muse[word][Muse.PHONEMES]

    def stress(self, word):
        return self.muse[word][Muse.STRESSES]

    def syllables(self, word):
        return self.muse[word][Muse.SYLLABLES]

    def matches_foot(self, poem, foot):
        '''
        Check if the given text matches a particular stress pattern (a foot).
        '''
        if len(poem) % len(foot) != 0:
            return False
        i, j = 0, 0
        while i < len(poem):
            stress_pattern = self.stress(poem[i])
            k = 0
            while i < len(poem) and k < len(stress_pattern):
                if not (stress_pattern[k] and foot[j]):
                    return False
                else:
                    i += 1
                    j = (j + 1) % len(foot)

    def matches(self, poem, metre):
        '''
        Check if a poem matches a particular metre.
        '''
        if metre not in FEET:
            raise ValueError("{} not a recognised poetic form".format(metre))
        return self.matches_foot(poem, FEET[metre])

    def rhyme(self, word1, word2, type="any"):

        # Sanity-check.
        valid_types = ["any", "masculine", "feminine"]
        if type not in valid_types:
            raise ValueError("Type of rhyme must be one of {} but was {}".format(valid_types, type))
        stress1, stress2 = self.phonemes(word1), self.phonemes(word2)

        # Two words have a feminine rhyme if the two ending phonemes are the same.
        if type in ["feminine", "any"] \
            and stress1[-1] == stress2[-1] \
            and (len(stress1) > 1 and len(stress2) > 1) \
            and stress1[-2] == stress2[-2]:
                return True

        # A word has a masculine rhyme if the last phonemes are the same.
        if type in ["masculine", "any"] \
            and stress1[-1] == stress2[-1] \
            and (len(stress1) == 1 or len(stress2) == 1 or stress1[-2] != stress2[-2]):
                return True

        # Could not ascertain a rhyme.
        return False

    def POS_tagging(self, text):
        '''
        Tag each part in some text with a particle of speech.
        '''
        return pos_tag(word_tokenize(text))
