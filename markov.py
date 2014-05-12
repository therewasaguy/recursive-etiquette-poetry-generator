
class MarkovGenerator(object):

  def __init__(self, n, max):
    self.n = n # order (length) of ngrams
    self.max = max # maximum number of elements to generate
    self.ngrams = dict() # ngrams as keys; next elements as values
    self.beginnings = list() # beginning ngram of every line
    self.all_words = list() # all words

  def tokenize(self, text):
    return text.split(" ")

  def feed(self, text):

    tokens = self.tokenize(text)
    # discard this line if it's too short
    if len(tokens) < self.n:
      return

    # store the first ngram of this line
    beginning = tuple(tokens[:self.n])
    self.beginnings.append(beginning)

    for i in range(len(tokens) - self.n):

      gram = tuple(tokens[i:i+self.n])
      self.all_words.append(tokens[i])
      next = tokens[i+self.n] # get the element after the gram

      # if we've already seen this ngram, append; otherwise, set the
      # value for this key as a new list
      if gram in self.ngrams:
        self.ngrams[gram].append(next)
      else:
        self.ngrams[gram] = [next]

  # called from generate() to join together generated elements
  def concatenate(self, source):
    return " ".join(source)

  # generate a text from the information in self.ngrams
  def generate_beginning(self):

    from random import choice

    # get a random line beginning; convert to a list. 
    current = choice(self.beginnings)
    output = list(current)

    for i in range(self.max):
      if current in self.ngrams:
        possible_next = self.ngrams[current]
        next = choice(possible_next)
        output.append(next)
        for i in next:
          if i == ".":
            break
          if i == ",":
            break
          if i == "?":
            break
        # get the last N entries of the output; we'll use this to look up
        # an ngram in the next iteration of the loop
        current = tuple(output[-self.n:])
      else:
        break

    output_str = self.concatenate(output)
    return output_str

  # Generate a text from the information in self.ngrams
  def generate(self, start_word):
    from random import choice

    # If the start word is in the text, generate a markov chain
    if start_word in self.all_words:
      current = choice([item for item in self.ngrams if item[0] == start_word])
      output = list(current)

      for i in range(self.max):
        if current in self.ngrams:
          possible_next = self.ngrams[current]
          next = choice(possible_next)
          output.append(next)
          current = tuple(output[-self.n:])
        else:
          break

      output_str = self.concatenate(output)
      return output_str
    else:
      return ''

if __name__ == '__main__':

  import sys


# from markov import MarkovGenerator
  army = MarkovGenerator(2, 2)
  for line in open('../texts/militaryrules.txt', 'r'):
    army.feed(line)
  print army.generate('Crecy')
  print army.generate('crappy word not in dict')
