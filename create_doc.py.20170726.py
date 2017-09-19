from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery
import json
import sys
import time
import telepot
from telepot.loop import MessageLoop

## initialisation 

cb = Bucket('couchbase://localhost/Listes')
bot = telepot.Bot('410210312:AAHvgXTuRxKKCoH6gUiR0rIrxCikSuj25ac')

## communication avec couchbase

def create_produit(name, user, category="defaut", liste="courses"):
	prod_id = cb.get('product_count').value + 1
	produit = {
		'name': name,
		'category': category,
		'liste': liste,
		'user': user
	}
	cb.upsert(str(prod_id), produit)
	cb.counter('product_count')

def get_liste(liste):
	query = N1QLQuery('SELECT * FROM `Listes` WHERE liste=$filtre', filtre=liste)
	for row in cb.n1ql_query(query): print(row['Listes']['name'])

def delete_liste(liste):
	query = N1QLQuery('DELETE FROM `Listes` WHERE liste=$filtre', filtre=liste)
	cb.n1ql_query(query).execute()

## communication avec telegram

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
    	parse_msg_rcvd(msg)

def getActionCode(word):
	query = N1QLQuery('select action FROM `Listes` WHERE $filtre IN syn', filtre=word)
	for action_code in cb.n1ql_query(query):
		pass	
	return action_code

## parsing des messages recus
def parse_msg_rcvd(msg):
	sentences=msg['text'].splitlines()
	if len(sentences)>1:
		for product in sentences:
			create_produit(product,msg['from']['id'])
	else :
		sentence=msg['text'].split()
		action_type = getActionCode(sentence[0])
		if action_type['action'] == 1:
			get_liste(sentence[1])
		elif action_type['action'] == 2:
			delete_liste(sentence[1])
		else :
			product = msg['text']
			create_produit(product,msg['from']['id'])


#create_produit("couche", "sante", "fringue")
#get_liste("fringue")
#delete_liste("fringue")
#print(produits)

MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
