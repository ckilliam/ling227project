# Ling 227 Final Project

import re
import sys
import random
from collections import defaultdict
import math
import numpy as np

training_file = "aesop.trans" ###

def generate_sentence_trigram():
	sentence = "# #"
	current = ''
	before_current = ''
	while current is not '#':
		if current == '' and before_current == '':
			current = '#'
			before_current = '#'
		temp = current
		current = generate_word_trigram(before_current, current)
		before_current = temp
		sentence += " " + current
	return sentence

def generate_word_trigram(word1, word2):
	rand = random.uniform(0,1)
	# following = 1
	for following in trigram[word1][word2]:
		# print following
		rand -= trigram[word1][word2][following]
		if rand < 0.0: return following
	return following

def probability_trigram(word):
	word = "# # " + word + " #"
	phones = re.split (r'\s', word)
	log_prob_total = 0
	for i in range(len(phones)-2):
		if bicounts[phones[i]][phones[i+1]] > 0: # if the denominator is zero, the fraction is undefined, so we add a probability of 0 in that case (this is only relevant when add-1 smoothing is not happening)
			log_prob_gram = np.log2( tricounts[phones[i]][phones[i+1]][phones[i+2]]/float(bicounts[phones[i]][phones[i+1]]) )
		else: log_prob_gram = 0
		log_prob_total += log_prob_gram # log_prob_total will be different for each word
		global file_sum_log_prob # file_sum_log_prob will be one value for the whole test file
		if log_prob_gram > 0:
			file_sum_log_prob += log_prob_gram
	prob_total = 2 ** log_prob_total # exponentiate to get rid of the log base 2
	return prob_total



counts = defaultdict(lambda:0)
bicounts = defaultdict(lambda:defaultdict(lambda:0))
tricounts = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))

with open(training_file) as language:
	for line in language:
		line = line.strip()
		line = re.sub('#', '# #', line)
		phones = re.split(r'\s', line)

		for i in range(len(phones)-1):
			counts[phones[i]] = counts[phones[i]] + 1
			bicounts[phones[i]][phones[i+1]] = bicounts[phones[i]][phones[i+1]] + 1

		# we go through each position and keep track of word and word pair counts
		for i in range(len(phones)-2):
			tricounts[phones[i]][phones[i+1]][phones[i+2]] = tricounts[phones[i]][phones[i+1]][phones[i+2]] + 1

		# add-1 smoothing
		for i in set(phones):
			for j in set(phones):
				for k in set(phones):
					counts[i] += 1
					bicounts[i][j] += 1
					tricounts[i][j][k] += 1
	
trigram = defaultdict(lambda:defaultdict(lambda:{}))

# this loops through all phoneme sets of 3 and computes relative frequency estimates
for word1 in counts:
	for word2 in bicounts[word1]:
		for word3 in tricounts[word1][word2]:
			trigram[word1][word2][word3] = float(tricounts[word1][word2][word3])/float(bicounts[word1][word2])

# generate 25 random sentences, which are actually words in this context
print "GENERATE RANDOM SEQUENCES"
# print 25 random 'sentences' using the trigram model
for i in range(25):
	print generate_sentence_trigram()

