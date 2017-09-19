# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import WhitespaceTokenizer
from nltk.tokenize import SpaceTokenizer
from nltk.tokenize import RegexpTokenizer
data = "Vous êtes au volant d'une voiture et vous roulez à vitesse"
#wst = WhitespaceTokenizer()
#tokenizer = RegexpTokenizer('\s+', gaps=True)
token=WhitespaceTokenizer().tokenize(data)
print(data)
print(token)