#!/bin/python

import re
import sys

def words(text): 
	return re.findall('[a-z]+', text.lower()) 


def generate_utterances(slot_name, intent_name, sentence_dict):
	for sentence in sentence_dict:
		yield intent_name + '\t' + sentence.replace('$', "{" + slot_name + "}")
			
if __name__=="__main__":
	slot_name = sys.argv[1]
	intent_name = sys.argv[2]
	sentence_templates_file = sys.argv[3]
	utterances_output = sys.argv[4]
	with open(sentence_templates_file) as f:
		sentences = [line for line in f]
	with open(utterances_output, 'w') as o:
		for utterance in generate_utterances(slot_name, intent_name, sentences):
			print >> o, utterance.strip()