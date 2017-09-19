from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery
import json
import sys
import time
import telepot
from telepot.loop import MessageLoop
import datetime

## initialisation

cb = Bucket('couchbase://localhost/Listes')
bot = telepot.Bot('410210312:AAHvgXTuRxKKCoH6gUiR0rIrxCikSuj25ac')

## communication avec couchbase

def create_produit(name="perf", user="auto", category="defaut", liste="courses"):
        prod_id = cb.get('product_count').value + 1
        produit = {
                'name': name,
                'category': category,
                'liste': liste,
                'user_id': user
        }
        cb.upsert(str(prod_id), produit)
        cb.counter('product_count')

def get_liste(liste, user):
	print(user)
	answer='Contenu de la liste : '+liste
	print(answer)
	query = N1QLQuery('SELECT * FROM `Listes` WHERE liste=$filtre1 AND user_id=$filtre2', filtre1=liste, filtre2=user)
	for row in cb.n1ql_query(query): 
		answer+='\n'
		answer+=row['Listes']['name']
	bot.sendMessage(user, answer)
			
def delete_liste(liste, user):
	query = N1QLQuery('DELETE FROM `Listes` WHERE liste=$filtre1 AND user_id=$filtre2', filtre1=liste, filtre2=user)
	cb.n1ql_query(query).execute()
	bot.sendMessage(user, liste+' supprimee')

## communication avec telegram

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        parse_msg_rcvd(msg)

def getActionCode(word):
        query = N1QLQuery('select action FROM `Listes` WHERE $filtre IN syn', filtre=word)
        action_code = "{\"action\": 0}"
        for action_code in cb.n1ql_query(query):
                pass
        return action_code

def parse_msg_rcvd(msg):
	user=msg['from']['id']
	sentences=msg['text'].splitlines()
	if len(sentences)>1:
		for product in sentences:
			create_produit(product,user)
	else :
		sentence=msg['text'].split()
		action_type = getActionCode(sentence[0])
		if action_type['action'] == 1:
			get_liste(sentence[1],user)
		elif action_type['action'] == 2:
			delete_liste(sentence[1],user)
		else :
			product = msg['text']
			create_produit(product,user)


MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
	print(datetime.datetime.now())
	for i in range(10000):
		create_produit()
	print(datetime.datetime.now())
	time.sleep(5)

