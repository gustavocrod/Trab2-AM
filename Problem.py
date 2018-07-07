from random import randint
from util import *
from Individual import Individual
import math
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
                d[i][j] = jaccard(i_object, j_object)
    
    p = Problem(n, d, 100, 5)    
    p.random_start()    
    
    while p.satisfaction(): 
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
        self.iterations = 0 #Número de iterações que o algoritmo executou
        self.best_fitness = float('inf') #Melhor fitness até o momento
        self.best_individual = None

    def satisfaction(self):
        return self.iterations < 20
    
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

        self.best_individual = self.population[0]
    
    def set_population_fitness(self):
        """
        Calcula e armazena o fitness de cada individuo
        :return: none
        """                
        iter_best_fitness = self.best_fitness

        for individual in self.population:
            self.fitness(individual)
            '''Caso o individuo possua um fitness menor que o melhor atual, salvamos isso para verificar
            se o fitness mudou para melhor'''
            if individual.fitness < iter_best_fitness:
                iter_best_fitness = individual.fitness

        
        # Se depois de calcular o fitness de todos os individuos, o melhor fitness diminuiu, atualizamos ele 
        # e zeramos o contador de iterações
        if iter_best_fitness != self.best_fitness:
            # Substitui o melhor fitness pelo adquirido nesta iteracao            
            self.best_fitness = iter_best_fitness
            self.iterations = 0

        self.sort_population_by_fitness()
        
        self.population.pop()
        self.population.append(self.best_individual)

        self.best_individual = self.population[0]
    
    def sort_population_by_fitness(self):
        self.population.sort(key=lambda x : x.fitness)

    def fitness(self, individual):
        """
        Define a apitidao de cada individuo (solucao)
        :param individual: matriz de tamanho n_tweets x n_clusters
        :return:
        """
        
        fitness_value = 0.0
        for v in range(self.n_clusters):
            pv = sum([individual.membership_matrix[s][v] for s in [s for s in range(0, self.n_tweets)]]) / self.n_tweets            
            pv = pv if pv > 0 else 0.1
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
        lista = list()
        lista = [self.population[randint(0, len(self.population) - 1)] for i in range(k)]
        lista.sort(key=lambda x : x.fitness)        
        
        return lista[0]
        

    def crossover(self, parents):
        """
        Faz o cruzamento entre dois individuos, gerando assim os descendentes
        :param parents: tupla contendo os pais
        :return:
        """        
        a, b = parents
        cutt_index = math.ceil(self.n_tweets/2)
            
        top_a = copy.deepcopy(a.membership_matrix[0:cutt_index])
        bottom_a = copy.deepcopy(a.membership_matrix[cutt_index:])
        
        top_b = copy.deepcopy(b.membership_matrix[0:cutt_index])
        bottom_b = copy.deepcopy(b.membership_matrix[cutt_index:])
        
        return (Individual(top_a + bottom_b), Individual(top_b + bottom_a ))
        

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
        
        self.best_individual = self.population[0]
        
        while not self.complete_population(aux_population):
            parent_a = self.selection(3)
            parent_b = self.selection(3)            
            a, b = self.crossover((parent_a, parent_b))
            #print (a.membership_matrix)
            #print (b.membership_matrix)
            aux_population.append(parent_a)
            aux_population.append(parent_b)

        # Substitui a população antiga pela nova        
        #print(self.population[5].membership_matrix == aux_population[5].membership_matrix)
        self.population = aux_population
        self.iterations += 1