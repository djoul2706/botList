from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer

def get_usefull_words(text):
	blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
	blob = blob.correct()
	print(blob)
	print(blob.noun_phrases)

	for tag in blob.tags:
		if tag[1] in ['NN', 'JJ', 'VB']:
			print(tag[0],tag[1])
		
while 1:
	var = input("phrase : ")
	get_usefull_words(var)