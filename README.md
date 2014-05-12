recursive-etiquette: poetry generator
===================

This repo has several Python scripts that helped me generate poetry.

The main program is etiquette.py -- Run it and it'll generate some poetry from three included source texts: Etiquette, Notes From Underground, and Sailor's Words. The process is described in detail on [my blog](http://www.itp.jasonsigal.cc/the-phrases-and-pronunciation/).

guessSyllables.py -- Python script to guess syllables of gibberish phrases i.e. "da dadum dum dum dee do" "shoobee doowah" "boo boo kachu".

markov.py --> a Markov object with a generate function that takes a starting word as its arguement.

nplc.py --> for generating a list of noun phrases. I wound up saving my noun phrases in text files which are included.
