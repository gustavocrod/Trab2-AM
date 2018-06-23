import json
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords
import re
from Problem import Problem

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
	# Tamanho do dataset
	n = len(tweets)
	# Matriz de dissimilaridade
	d = [[0 for i in range(n)] for j in range(n)]
	for i in range(n):
		i_object = tweets[i]['text']		
		print(i_object)
		for j in range(n):
			if i != j:
				j_object = tweets[j]['text']				
				d[i][j] = levenshtein(i_object, j_object)	
	
	p = Problem(n, d, 100, 5)

if __name__ == '__main__':
	main()