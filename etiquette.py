import random
import sys
from textblob import TextBlob
from nplc import NPLC	#this object creates noun phrases from texts
from rhymebot import rhyme_set, rhyming_word # 

#### add markov generator for military text
from markov import MarkovGenerator
military = MarkovGenerator(2, 10)
for line in open('../texts/dickens_bleakhouse.txt', 'r'):
	military.feed(line) #decode('ascii', errors='replace')
# for line in open('../texts/militaryrules.txt', 'r'):
# 	military.feed(line) #decode('ascii', errors='replace')

post = NPLC('../texts/etiquette.txt', 2)
etiquettenp = open("etiquette_noun_phrases.txt", "wb")
for i in post.noun_phrases:
	etiquettenp.write(i.encode('utf-8', errors='replace').strip() + '\n')
# print " ".join(post.noun_phrases)
etiquettenp.close()

print "done writing file!"

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

def gSyls(aword):
	if aword.upper() in all_words:
		return syl_bible[aword.upper()]
	else:
		return gib_syls(aword)


def makeLine(words):
	words = words.split()
	new_line = ''
	for word in words:
		if word in military.all_words:
			agram = military.generate(word)
			new_line = new_line + " " + agram
		else:
			new_line = new_line + " " + word
	#print new_line
	return new_line

def nounize(aline):
	words = ''
	aline = TextBlob(aline.decode('ascii', errors='replace'))
	for word, tag in aline.tags:
		if tag == 'NN':
			word = post.random_np()
		words = words + ' ' + word
	return words

def changeWord(word):
	new_word = ''
	nounize(word)
	if word.upper() in all_words:
		new_word = rhyming_word(word, 1)
		if new_word:
			return new_word.lower()
		else:
			new_word = str(random.choice(syl_lookup[syl_bible[word.upper()]]))
			# new_line = new_line + " " + new_word.lower()
	else:
		gibSyl = gib_syls(word)
		new_word = str(random.choice(syl_lookup[gibSyl]))
		# new_line = new_line + " " + 
	return new_word.lower() + " " + post.random_np()

def redo_line(line):
	words = line.split()
	if len(words) > 0:
		w = words.pop()
		y = changeWord(w)
		if len(words) > 8:  #crucial variable
			new_line = ' '.join(words)
			try:
				print ' '.join(new_line.split()[-7:]) + " " +y.lower()
			except:
				print ' '.join(new_line.split()[-1:])
			redo_line(new_line)

for line in sys.stdin:
	line = line.strip()
	words = line.split()

	# new stuff
	for word in words:
		# print rhyming_word(word, 2)
		x = post.random_np()
		firstArmyVersion = makeLine(word)
		# print x
		# print firstArmyVersion
		armyVersion = makeLine(x)
		# print armyVersion
		redo_line(firstArmyVersion)
		redo_line(x)
		redo_line(armyVersion)
		y = []
		for i in x.split():
			z = rhyming_word(i, 3)
			if z: 
				y.append(z)
		print " ".join(y)

# #
# sentence
# a noun_phrases(1) --> 2 syllables
# a noun_phrases(1) --> 2 syllables
# a noun_phrases(1) --> 3 syllables
# a nounphrase (4) --> 5 syllables
# sentence
# a noun_phrases(1) x 3. --> 2 syllables
# a nounphrase (4) --> 5 syllables
# question (army markov gen)
# question (army markov gen)
# question (army markov gen)
# a noun_phrases(1) x 3 --> 2 syllables
# a nounphrase (4) --> 5 syllables

	# for word in words:
	# 	armyVersion = makeLine(word)
	# 	print armyVersion
	# 	redo_line(armyVersion)
	# 	manneredVersion = nounize(armyVersion)
	# 	print manneredVersion
	# 	redo_line(manneredVersion)
	# aLine = makeLine(words)
	# print aLine
	# redo_line(aLine)
	# nLine = nounize(aLine)
	# print nLine
	# redo_line(nLine)
	# changedLine = ''
	# for each_word in aLine.split():
	# 	changedLine = changedLine + ' ' + changeWord(each_word)
	# print changedLine
	# changedLine = ''
	# for each_word in nLine.split():
	# 	changedLine = changedLine + ' ' + changeWord(each_word)
	# redo_line(changedLine)
