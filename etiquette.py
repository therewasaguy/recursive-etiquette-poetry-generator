import random
import sys
from textblob import TextBlob, Word
from nplc import NPLC	#this object creates noun phrases from texts
from rhymebot import rhyme_set, rhyming_word # 

#### add markov generator named underground and feed it all the source text ####
from markov import MarkovGenerator
underground = MarkovGenerator(5, 6)

utext = []
for line in open('notesfromunderground.txt', 'r'):
	utext.append(line + ' ')
utext_sentences = TextBlob(" ".join(utext).decode('ascii', errors='replace')).sentences
for sentence in utext_sentences:
	underground.feed(sentence)

print 'loaded 1/3'

sailortext = []
for line in open('sailorswordbook.txt', 'r'):
	sailortext.append(line + ' ')
sailor_sentences = TextBlob(" ".join(sailortext).decode('ascii', errors='replace')).sentences
for sentence in sailor_sentences:
	underground.feed(sentence)

print 'loaded 2/3'

posttext = []
for line in open('etiquette.txt', 'r'):
	posttext.append(line + ' ')
post_sentences = TextBlob(" ".join(posttext).decode('ascii', errors='replace')).sentences
for sentence in post_sentences:
	underground.feed(sentence)

print 'loaded 3/3'
print ' '

#### add noun phrases ####
postnouns = []
for line in open('etiquette_noun_phrases.txt', 'r'):
	postnouns.append(line)

sailornouns = []
for line in open('sailor_nouns.txt', 'r'):
	sailornouns.append(line)


def not_a_vowel(letter):
	for char_to_check in ["a", "e", "i", "o", "u"]:
		if letter == char_to_check:
			return False
	return True


def ensure_caps(line):
	if line[0].isupper():
		return False
	if line[0] == '"':
		return False
	else:
		return True


# This function tries to figures out what preposition to put before
# a Noun Phrase based on whether it is plural and based on its starting letter.
def preposition(line):
	first_letter = line[0]
	for word in line.split():
		tb = TextBlob(word)
		for w, t in tb.tags:
			if t == 'NN':
				b = Word(word)
				if word == str(b.singularize()):
					# print word + " is probably singular like " + b.singularize()
					if not_a_vowel(first_letter):
						return random.choice(['The ', 'A ', '']) + line
					else:
						return random.choice(['The ', 'An ', '']) + line
				elif word == str(b.pluralize()):
					return random.choice(['The ', 'Some ', 'Many ', 'Of ', 'For all of the ', '']) + line
	## if it gets to this point, we dont know if it is plural, so just figure out if 'a' or 'an'
	if not_a_vowel(first_letter):
		return random.choice(['A ', 'The ', '']) + line
	else:
		return random.choice(['An ', 'The ', '']) + line


# Generates a line from the Markov chain and ensures that it is capitalized
def generate_opening_line():
	next_line = underground.generate_beginning()
	while ensure_caps(next_line):
		next_line = underground.generate_beginning()
		if ensure_caps(next_line) == False:
			break
	return next_line

def generate_question():
	next_line = underground.generate(random.choice(['What', 'How', 'Why', 'When', 'Where']))
	return next_line




### used to write the text file of Noun Phrases
# post = NPLC('../texts/sailorswordbook.txt', 4)
# npz = open("sailor_nouns.txt", "wb")
# for i in post.noun_phrases:
# 	npz.write(i.encode('utf-8', errors='replace').strip() + '\n')
# npz.close()

# print "done!"

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

""" guess # of syllables in a series of gibberish, i.e. "da dadum dum dum dee do" "shoobee doowah" "boo boo kachu"""
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



def gSyls(aword):
	if aword.upper() in all_words:
		return syl_bible[aword.upper()]
	else:
		return gib_syls(aword)

# Generate a markov chain that starts with each word in a set of phrases
def makeLine(words, marko):
	words = words.split()
	new_line = ''
	for word in words:
		if word in marko.all_words:
			agram = marko.generate(word)
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
			word = random.choice(postnouns).strip()
		words = words + ' ' + word
	return words


## This function takes a word an changes it to another word that rhymes or has the same # of syllables.
## Sometimes, it also appends a random nounphrase 
## rhyming_word is in a separate file, the rhymebot module. 
def changeWord(word):
	new_word = ''
	#	nounize(word)
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
	return new_word.lower() + " " + random.choice(postnouns + sailornouns).strip()


## This function iterates recursively through a line, three words at a time.
## It transforming the last word each time by calling the changeWord function.
def redo_line(line):
	words = line.split()
	if len(words) > 0:
		w = words.pop()
		y = changeWord(w)
		if len(words) > 3:  #crucial variable
			new_line = ' '.join(words)
			try:
				print ' '.join(new_line.split()[-3:]) + " " +y.lower()
			except:
				print ' '.join(new_line.split()[-2:])
			redo_line(new_line)
		if len(words) == 3:
			new_line = ' '.join(words)
			try:
				print ' '.join(new_line.split()[-2:]) + " " +y.lower()
			except:
				print ' '.join(new_line.split()[-1:])
			redo_line(new_line)
		if len(words) == 2:
			new_line = ' '.join(words)
			try:
				print ' '.join(new_line.split()[-1:]) + " " +y.lower()
			except:
				print ' '.join(new_line.split()[-1:])
			redo_line(new_line)
		if len(words) == 1:
			print words[0] + ' ' + y
			print underground.generate(words[0])
			print underground.generate(words[0])
			print words[0] + w
			return 



### GENERATE THE POEM ###

# Generate a capitalized opening line from Markov beginnings
opening_line = generate_opening_line()

# Generate three noun phrases
nOne = random.choice(postnouns).strip()
nTwo = random.choice(postnouns).strip()
nThree = random.choice(sailornouns).strip()


# Sort the noun phrases by length
if len(nOne) > len(nTwo):
	nX = nOne
	nOne = nTwo
	nTwo = nX

if len(nTwo) > len(nThree):
	nX = nTwo
	nTwo = nThree
	nThree = nX

# Poetic structure
print preposition(nOne)
print preposition(nTwo)
print preposition(nThree)
print ''
print opening_line
print ''
print preposition(nOne)
print preposition(nTwo)
print preposition(nThree)
print ''
print generate_opening_line()
print ''
print preposition(nOne)
print random.choice(sailornouns + postnouns)
print random.choice(sailornouns + postnouns)
print random.choice(sailornouns + postnouns)
print preposition(nThree)
print ''
print underground.generate(nOne.split()[0])
print underground.generate(nOne.split()[1])

q = generate_question()
print q + '?'
print ' '
print preposition(nOne)
print preposition(nTwo)
print preposition(nThree)
print ''
print generate_question()
print random.choice(postnouns).strip()
print ''
print generate_question()
print random.choice(postnouns).strip()
print ''
print generate_opening_line()
print random.choice(postnouns).strip()
print generate_question()
print ' '
print preposition(nOne)
print preposition(nTwo)
print preposition(nThree)
redo_line(nOne + ' ' + ' ' + nTwo + ' ' + nThree)

print ' '
print generate_opening_line()
redo_line(opening_line)

print preposition(nOne)
print preposition(nTwo)
print preposition(nThree)
