from random import randint
from util import *
from Individual import Individual
import math

def satisfaction(problem):
    """
    recebe um problema e retorna o quão bom ele esta
    :param problem:
    :return: um numero que representa o quao bom o algoritmo esta
    """
    pass

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

    # Tweets com algumas normalizações
    tweets = remove_stop_words(load_tweets())
    # Tamanho do dataset
    n = len(tweets)
    # Matriz de dissimilaridade
    d = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        i_object = tweets[i]['text']        
        for j in range(n):
            if i != j:
                j_object = tweets[j]['text']
                d[i][j] = 0.5 * jaccard(i_object, j_object) +  0.5 * levenshtein(i_object, j_object)

    p = Problem(n, d, 100, 5)
    p.random_start()

    while satisfaction(p.population) > 0.3:
        p.set_population_fitness()
        p.new_population()



class Problem(object):
    """Classe para resolução do problema de clustering de Tweets"""

    def __init__(self, n, d, p_size, n_clusters):
        self.n_tweets = n # Número de tweets
        self.d = d # Matriz de dissimilaridade
        self.p_size = p_size # Tamanho da populacao
        self.population = list() # Lista de individuos/candidato (populacao)
        self.n_clusters = n_clusters # Numero de clusters         

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
            self.population.append(Individual(membership_matrix))
    
    def set_population_fitness(self):
        """
        Calcula e armazena o fitness de cada individuo
        :return: none
        """
        for individual in self.population:
            self.fitness(individual)

    def fitness(self, individual):
        """
        Define a apitidao de cada individuo (solucao)
        :param individual: matriz de tamanho n_tweets x n_clusters
        :return:
        """
        fitness_value = 0        
        for v in range(self.n_clusters):
            2pvN = 2 * (sum(individual.membership_matrix[s][v] for s in [s for s in range(1, self.n_tweets + 1)]) / self.n_tweets) * self.n_tweets
            temp = 0
            for k in range(self.n_tweets):
                for l in range(self.n_tweets):
                    temp += (individual.membership_matrix[k][v] * individual.membership_matrix[l][v] * self.d[k][l])
            fitness_value += temp/2pvN
        
        individual.fitness = fitness_value  

    def selection(self, k):
        """
        :param k: Número de individuos participantes do torneio
        :return: uma tupla com os 2 individuos vencedores do torneio
        """
        better = None
        best = None
        for i in range(k):
            candidate_index = randint(0, len(self.population) - 1)
            candidate_fitness = self.population[candidate_index].fitness
            if better == None or candidate_fitness < self.population[better].fitness:
                second_best = better
                better = self.population[candidate_index]
            self.population.pop(candidate_index)

        return (better, second_best)

    def crossover(self, parents):
        """
        Faz o cruzamento entre dois individuos, gerando assim os descendentes
        :param parents: tupla contendo os pais
        :return:
        """
        a, b = parents
        cutt_index = math.ceil(self.n_tweets/2)
        
        top_a = a.membership_matrix[0:cutt_index]
        bottom_a = a.membership_matrix[cutt_index:]
        
        top_b = b.membership_matrix[0:cutt_index]
        bottom_b = b.membership_matrix[cutt_index:]

        return (Individual(top_left + bottom_right), Individual(bottom_left + top_right))
        

    def mutation(self, probabilidade):
        """
        Com a probabilidade de mutação, altere os cromossomas da nova geração nos locus (posição nos cromossomas).
        :return:
        """
        pass

    def complete_population(self, aux_population):
        """
        verifica e uma populacao esta completa - se ela tem o tamanho correto de cromossomos
        :return: retorna true caso esteja completa. false para contrario
        """
        return len(aux_population) == self.p_size        

    def new_population(self, prob_mutation):
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
            parents = self.selection()
            a, b = self.crossover(parents)
            aux_population.append(a)
            aux_population.append(b)

        self.population = aux_population