from random import randint
from random import sample
from random import random
from util import *
from Individual import Individual
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import math
from time import time
import copy
cont = 0

def generic_logarithm():
    """
      definicao do algoritmo genetico:
          inicia_população () # Gere uma população aleatória de n cromossomas (soluções adequadas para o problema)
          repertir ate satisfeito com a populacao:
              avaliação () # Avalie a adequação f(x) de cada cromossoma x da população
              repetir ate nova que a nova pupulacao esteja completa:
                  seleção_dos_pais ()
                  cruzamento ()
                  mutacao ()
              Utilize a nova população gerada para a próxima rodada do algoritmo
          retorne a melhor solução da população atual
    """
    print("Carregando tweets")
    # Tweets com algumas normalizações
    tweets = [t['text'] for t in remove_stop_words(load_tweets())]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(tweets)
    
    print("Calculando matriz de dissimilaridade")
    # Matriz de dissimilaridade    
    d = pairwise_distances(X=tfidf_matrix, Y=None, n_jobs=-1, metric='cosine')    
    # Tamanho do dataset
    n = len(tweets)
    p = Problem(n, d, 8, 10)

    print("Gerando população aleatória inicial")    
    p.random_start()
    p.set_population_fitness()
    p.best_individual = min(p.population, key=lambda ind: ind.fitness)
    
    while p.satisfaction():
        p.new_population()
        print("\n--------------------------------------------------------")
        print("Iterações sem mudança no melhor indivíduo: ", p.iterations)        
        print("Número de gerações: ", p.generation)
        print("Melhor fitness: ", p.best_individual.fitness)

    for v in range(p.n_clusters):
        v_tweets_index = [i for i in range(p.n_tweets) if p.best_individual.membership_matrix[i][v] == 1]        
        v_tweets = [tweets[i] for i in v_tweets_index]
        with open('{}.txt'.format(v), 'w') as f:
            f.write('\n'.join(v_tweets))
            f.write('\n')        
        
class Problem(object):
    """Classe para resolução do problema de clustering de Tweets"""

    def __init__(self, n, d, p_size, n_clusters):
        self.n_tweets = n # Número de tweets
        self.d = d # Matriz de dissimilaridade
        self.p_size = p_size # Tamanho da populacao
        self.population = list() # Lista de individuos/candidato (populacao)
        self.n_clusters = n_clusters # Numero de clusters         
        self.iterations = 0 #Número de iterações que o algoritmo executou
        self.best_fitness = float('inf') #Melhor fitness até o momento
        self.best_individual = None
        self.max_iterations = 200 # Númeoro máximo de iterações SEM MELHORIA na solução
        self.generation = 0

    def satisfaction(self):
        return self.iterations < self.max_iterations or self.generation == 10000
    
    def random_start(self):
        """
        Aleatoriza p solucoes (individuos) para o problema
        (gera a populacao inicial - randomica)
        :return: none
        """        
        ''' Precisamos criar p_size individuos (ex: 100)'''
        for individual_index in range(self.p_size):
            
            ''' Pra cada um dos individuos, tem que criar a matriz de membership '''
            membership_matrix = [[0 for col in range(self.n_clusters)] for row in range(self.n_tweets)] #individuo

            '''Define o cluster o individuo de maneira aleatória'''
            for i in range(self.n_tweets):
                membership_matrix[i][randint(0, self.n_clusters - 1)] = 1

            '''Adiciona o individuo na poulação'''
            self.population.append(Individual(membership_matrix, self.generation))

    def set_population_fitness(self):
        """
        Calcula e armazena o fitness de cada individuo
        :return: none
        """ 
        for individual in self.population:
            self.fitness(individual)            
            '''Caso o individuo possua um fitness menor que o melhor atual, salvamos isso para verificar
            se o fitness mudou para melhor'''        

    def fitness(self, individual):
        """
        Define a apitidao de cada individuo (solucao)
        :param individual: matriz de tamanho n_tweets x n_clusters
        :return:
        """
        fitness_value = 0.0
        for v in range(self.n_clusters):
            pv = sum([individual.membership_matrix[s][v] for s in [s for s in range(self.n_tweets)]]) / self.n_tweets
            pv = pv if pv > 0 else 0.001
            denominator = 2.0 * pv * self.n_tweets
            temp = 0.0
            for k in range(self.n_tweets):
                for l in range(self.n_tweets):
                    temp += (individual.membership_matrix[k][v] * individual.membership_matrix[l][v] * self.d[k][l])
            fitness_value += temp/denominator        

        individual.fitness = fitness_value

    def selection(self, k):
        """
        :param k: Número de individuos participantes do torneio
        :return: individuo vencedor do torneio
        gera uma lista random com K elementos, ordena eles por fitness, e retorna o de melhor aptidao
        """        
        lista = sample(self.population, k)
        lista.sort(key=lambda x : x.fitness)
        # print(self.population.index(lista[0]))
        return lista[0]
        

    def crossover(self, parents):
        """
        Faz o cruzamento entre dois individuos, gerando assim os descendentes
        :param parents: tupla contendo os pais
        :return:
        """        
        a, b = parents
        # cutt_index = math.ceil(self.n_tweets/2)
        cutt_index = randint(int(self.n_tweets * 0.1), self.n_tweets -1)
            
        top_a = copy.deepcopy(a.membership_matrix[0:cutt_index])
        bottom_a = copy.deepcopy(a.membership_matrix[cutt_index:])
        
        top_b = copy.deepcopy(b.membership_matrix[0:cutt_index])
        bottom_b = copy.deepcopy(b.membership_matrix[cutt_index:])

        new_membership_matrix_a = top_a + bottom_b
        new_membership_matrix_b = top_b + bottom_a        

        son_a = Individual(new_membership_matrix_a, self.generation)
        son_b = Individual(new_membership_matrix_b, self.generation)        

        return (son_a, son_b)
        

    def mutation(self, individual):
        """
        Com a probabilidade de mutação, altere os cromossomas da nova geração nos locus (posição nos cromossomas).
        :return:
        """
        for row in individual.membership_matrix:
            # probabilidade aleatória
            mutation_rate = random()
            if mutation_rate <= 0.011:                
                # Efetiva a mutação
                new_cluster_index = randint(0, self.n_clusters - 1)
                row[row.index(1)] = 0
                row[new_cluster_index] = 1 

    def complete_population(self, aux_population):
        """
        verifica e uma populacao esta completa - se ela tem o tamanho correto de individuos
        :return: retorna true caso esteja completa. false para contrario
        """
        return len(aux_population) == self.p_size        

    def new_population(self):
        """
        Repete
            seleção_dos_pais ()
            cruzamento ()
        ate que a populacao esteja completa
        mutacao ()
        :return:
        """        
        aux_population = list()
        while not self.complete_population(aux_population):
            # Seleciona os individuos para gerar os novos individuos
            parent_a = self.selection(5)
            parent_b = self.selection(5)
            # Gera dois novos individuos cruzando parent_a e parent_b
            a, b = self.crossover((parent_a, parent_b))            
            # Mutação dos novos indivíduos
            self.mutation(a)            
            self.mutation(b)
            self.fitness(a)
            self.fitness(b)
            # Adiciona na lista da nova população os novos indivíduos
            aux_population.append(a)
            aux_population.append(b)
        
        best_from_old = min(self.population, key=lambda ind: ind.fitness)
        best_from_new = min(aux_population, key=lambda ind: ind.fitness)
        
        # Elitismo
        ## Remove o individuo de maior custo da nova população
        aux_population.remove(max(aux_population, key=lambda ind: ind.fitness))
        ## Insere na nova população o melhor individuo da população anterior
        aux_population.append(best_from_old)
        
        if best_from_new.fitness < self.best_individual.fitness:
            self.best_individual = best_from_new
            self.iterations = 0

        # Substitui a população antiga pela nova
        self.population = aux_population
        self.iterations += 1
        self.generation += 1
