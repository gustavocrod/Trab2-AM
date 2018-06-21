import json
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords
import re
from Kmedoids import Kmedoids

# Calcula o numero de operações para transformar a em b
def levenshtein(a,b):
	return edit_distance(a,b)

# Medida de similaridade baseada em quantos elementos dois conjuntos compartilham
def jaccard(a,b):	
	a_words = set(a.split())
	b_words = set(b.split())	
	if a_words.isdisjoint(b_words):
		return 0	
	return 1 - (len(a_words.intersection(b_words)) / (len(a_words) + len(b_words) - len(a_words.intersection(b_words))))

# Carrega os tweets do arquivo Tweets.json
def load_tweets():
	try:		
		with open('Tweets.json', 'r') as f:
			file_text = f.read()
			tweets = json.loads(file_text)
			return tweets
	except Exception as e:
		print("Falha ao abrir arquivo json")
		raise e

# Remove palavras que não acrescentam informação, adicionalmente remove pontuação
def remove_stop_words(tweets):	
	for t in tweets:
		t['text'] = " ".join([re.sub(r'[\.\?\!\,]', '', word.lower()) for word in t['text'].split() if not word in stopwords.words('english')])
	return tweets

def main():
	# Tweets com algumas normalizações
	tweets = remove_stop_words(load_tweets())
	# Armazena tweets e a qual medoid eles pertencem	


if __name__ == '__main__':
	main()