import nltk
import random

def rhyme_set(inp, level):
	entries = nltk.corpus.cmudict.entries()
	syllables = [(word, syl) for word, syl in entries if word == inp]
	rhymes = []
	for (word, syllable) in syllables:
		rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
	return set(rhymes)

def rhyming_word(inp, level):
	entries = nltk.corpus.cmudict.entries()
	syllables = [(word, syl) for word, syl in entries if word == inp]
	rhymes = []
	for (word, syllable) in syllables:
		rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
	if rhymes == []:
		pass
	else:
		return random.choice(rhymes)

if __name__ == "__main__":
	import sys
	for line in sys.stdin:
		line = line.strip()
		for word in line.split():
			print rhyming_word(word, 3)
