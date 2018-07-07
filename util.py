import json
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords
import re
from Problem import *

def levenshtein(a,b):
    """
    Calcula o numero de operações para transformar a em b

    :param a: primeira string
    :param b: segunda string
    :return: distancia de levenshtein
    """
    return edit_distance(a,b)

def jaccard(a,b):
    """
    Medida de similaridade baseada em quantos elementos dois conjuntos compartilham

    :param a: primeira string
    :param b: segunda string
    :return: retorna 0 caso ?
             retorna a medida de jaccard
    """
    a_words = set(a.split())
    b_words = set(b.split())

    numerator = 0
    
    if a_words > b_words:
        greater = a_words
        shorter = b_words
    else:
        greater = b_words
        shorter = a_words
    
    for a in shorter:
        for b in greater:            
            if levenshtein(a, b)/len(b if b > a else a) <= 0.4:
                numerator += 1
    

    if a_words.isdisjoint(b_words):
        return 0
    return 1 - (numerator / (len(a_words) + len(b_words) - numerator))

def load_tweets():
    """
    Carrega os tweets do arquivo Tweets.json
    :return: lista de objetos
    """
    try:
        with open('Tweets.json', 'r') as f:
            file_text = f.read()
            tweets = json.loads(file_text)
            return tweets
    except Exception as e:
        print("Falha ao abrir arquivo json")
        raise e


def remove_stop_words(tweets):
    """
    Remove palavras que não acrescentam informação, adicionalmente remove pontuação
    :param tweets: lista com os tweets
    :return:
    """
    for t in tweets:
        t['text'] = " ".join([re.sub(r'[\.\?\!\,]', '', word.lower()) for word in t['text'].split() if not word in stopwords.words('english')])
    return tweets