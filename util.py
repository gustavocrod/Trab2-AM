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

def jaccard_velho(a,b):
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
            if levenshtein(a, b)/len(b if b > a else a) <= 0.3:
                numerator += 1
    
    if numerator == 0:
        return 0
    return 1 - (numerator) / (len(a_words) + len(b_words) - numerator)

def jaccarddd(a,b):
    """
    Medida de similaridade baseada em quantos elementos dois conjuntos compartilham
    :param a: primeira string
    :param b: segunda string
    :return: retorna 0 caso ?
             retorna a medida de jaccard
    """
    a_words = set(a.split())
    b_words = set(b.split())
    
    
    if len(a_words.intersection(b_words)) == 0:
        return 1.0
    return 1 - len(a_words.intersection(b_words)) / len(a_words.union(b_words))

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

def print_population(p):
    cont = 1
    for ind in p.population:
        print("=================")
        print("membership matrix, geracao: {}, individuo: {}".format(p.generation, cont))
        for row in ind.membership_matrix:
            print(row)
        print("Fitness", ind.fitness)
        print("==================")
        input()
        cont += 1

def remove_stop_words(tweets):
    """
    Remove palavras que não acrescentam informação, adicionalmente remove pontuação
    :param tweets: lista com os tweets
    :return:
    """
    for t in tweets:
        t['text'] = " ".join([re.sub(r'[\.\?\!\,]', '', word.lower()) for word in t['text'].split() if not word in stopwords.words('english')])
    return tweets
