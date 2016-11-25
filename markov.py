

from collections import defaultdict
import random 



class TextGen(object):
   
   def __init__(self, files_to_read):
   
      # Initialise fields, sanitise input.
      self._3grams = defaultdict(lambda: [])
      if type(files_to_read) == str:
         files_to_read = [files_to_read]

      # Use this for parsing.
      def _nextToken(f):
         for line in f:
            for token in line.lstrip().rstrip().split():
               yield token.lower()

      # Read each supplied file into the data-set.
      for fname in files_to_read:
         if type(fname) != str:
            raise TypeError("Must pass str when creating TextGen, but you passed {}".format(str(type(fname))))
         with open(fname, "r") as f:
            fst, snd = _nextToken(f), _nextToken(f)
            for token in _nextToken(f):
               self._3grams[(fst, snd)].append(token)
               fst, snd = snd, token

   def generateText(self, seed=None, maxSize=30):

      # Figure out where to start in the chain.
      if not seed:
         seed = ""
      seed = seed.split()
      if len(seed) < 2:
         fst, snd = random.choice(list(self._3grams.keys()))
      else:
         seed = seed.split()
         fst, snd = seed[-2], seed[-1]
      maxSize += len(seed)
      text = [fst, snd]

      # Start producing words, based on last two items in the text.
      for i in range(maxSize - len(seed)):
         if (fst,snd) not in self._3grams:
            wordChoice = self._3grams[random.choice(list(self._3grams.keys()))]
         else:
            wordChoice = self._3grams[(fst,snd)]
         word2use = random.choice(wordChoice)
         text.append(random.choice(wordChoice))
         fst, snd = snd, word2use

      return " ".join(text)










   

