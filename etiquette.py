import random
import sys

from nplc import NPLC	#this object creates noun phrases from texts
from rhymebot import rhyme_set, rhyming_word # 
# from guessSyllables import gib_syls

#### add markov generator for military text
# from markov import MarkovGenerator
# military = MarkovGenerator(2, 20)
# #military.feed('../texts/militaryrules.txt')
# for line in open('../texts/militaryrules.txt', 'r'):
# 	military.feed(line.decode('ascii', errors='replace'))

# post = NPLC('../texts/etiquette.txt', 2)


""" dictionary of words with number of syllables as the key """
syl_bible = {} #number of syllables in the word
syl_lookup = {} #key

def count_syl(cmu_word_obj):
	sylcount = 0
	joinedphonemes = "".join(cmu_word_obj)
	for char in joinedphonemes:
		if char in ("0", "1", "2", "3"):	#if the value if the char is in this tuple
			sylcount += 1
	return sylcount

for line in open('cmu_rhymedict.txt'):
	words = line.split() #break the line apart into sections, store it in a dictionary of how many phonemes it has + a set of the words
	count = len(words) - 1
	word = {words[0]: words[1:]}  #probably too complicated, could just use the word itself

	syl_bible[words[0]] = count_syl(words[1:])
	if count in syl_lookup:
		syl_lookup[count].append(str(words[0]))  #a set that contains word
	else:
		syl_lookup[count] = [str(words[0])]  #this is a set, not just the word itself, so we can add more words later

all_words = list(syl_bible.keys())

""" guess syllables #guess syllables of gibberish i.e. "da dadum dum dum dee do" "shoobee doowah" "boo boo kachu"""
def gib_syls(aWord):
	n = 3
	sylz = 0
	characters = list(aWord)

	#test first letter
	if not_a_vowel(characters[0]):
		sylz = 0
	else:
		sylz = 1

	#test ngrams
	for c in range(len(characters) - n+1):
		gram = tuple(characters[c:c+n])
		curChar = gram[1]
		prevChar = gram[0]
		nextChar = gram[2]

		for char_to_check in ["a", "e", "i", "o", "u"]:
			if curChar == char_to_check:
				if not_a_vowel(prevChar):
					sylz += 1
	if sylz == 0:
		sylz = 1

	for char_to_check in ["a", "e", "i", "o", "u"]:
		if characters[-1] == char_to_check:
			if len(characters) > 2:
				if not_a_vowel(characters[-2]):
					sylz += 1

	return sylz


def not_a_vowel(letter):
	for char_to_check in ["a", "e", "i", "o", "u"]:
		if letter == char_to_check:
			return False
	return True


## TO DO ##
# def fill_in_blanks
# def synonym

## fun stuff happens here ///////////////////////////// commented temporarily
# x = post.random_np()
# x = x + " " + military.generate()
# print x
# y = []
# for i in x.split():
# 	z = rhyming_word(i, 3)
# 	if z == None:
# 		pass
# 	else: 
# 		y.append(z)
# print " ".join(y)


for line in sys.stdin:
	line = line.strip()
	words = line.split()
	syls = ""
	for word in words:
		if word.upper() in all_words:
			new_word = rhyming_word(word, 1)
			if new_word:
				syls = syls + " " + new_word
			else:
				new_word = random.choice(syl_lookup[syl_bible[word.upper()]])
				syls = syls + " " + new_word
			# print word + " is in the word bible and has " + str(syl_bible[word.upper()]) + " syllables"
		else:
			gibSyl = gib_syls(word)
			new_word = random.choice(syl_lookup[gibSyl])
			syls = syls + " " + str(new_word).lower()
	print syls