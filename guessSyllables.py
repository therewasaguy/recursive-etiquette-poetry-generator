#guess syllables of gibberish i.e. "da dadum dum dum dee do" "shoobee doowah" "boo boo kachu"
import sys

ngrams = dict()
n = 3

def gibs(aWord):
	sylz = 0
	characters = list(aWord)
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


# fill in blanks

# if - two syllables


for line in sys.stdin:
	line = line.strip()
	words = line.split()
	syls = ""
	for word in words:
		gibSyl = gibs(word)
		syls = syls + " " + str(gibSyl)
	print syls

