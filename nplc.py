from textblob import TextBlob
import random

class NPLC:
	def __init__(self, somefile, phraselength):
		self.sometext = somefile
		self.noun_phrases = []
		for line in open(somefile, 'r'):
			self.noun_phrases = self.noun_phrases + list_noun_phrases(self, line, phraselength)

	def random_np(self):
		return random.choice(self.noun_phrases)


def list_noun_phrases(self, some_text, phraselength):
	np = []
	blob = TextBlob(some_text.decode('ascii', errors='replace'))
	for nounphrase in blob.noun_phrases:
		if len(nounphrase.split()) >= phraselength:
			x = nounphrase.split()[0]
			if len(x) > 3:
				np.append(nounphrase)
	if len(np) == 0:
		pass
	return np

def pick_random_noun_phrase(self, some_list):
	# for i in range(len(some_list)):
	return random.choice(some_list)


if __name__ == "__main__":
	import sys
	noun_phrases = []
	for line in sys.stdin:
		line = line.strip()
		noun_phrases = noun_phrases + list_noun_phrases(__name__, line, 1)
	print noun_phrases
	a_np = pick_random_noun_phrase(__name__, noun_phrases)
#	print a_np
#	print random.choice(noun_phrases)


# for i in range(0,10):
# 	print random.choice(np)
# 	# line = line.strip()
# 	# blob = TextBlob(line.decode('ascii', errors='replace'))
# 	# for nounphrase in blob.noun_phrases:
# 	# 	print nounphrase
