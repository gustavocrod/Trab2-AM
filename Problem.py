from random import randint

def generic_logarithm():
    """
    definicao do algoritmo genetico:

        inicia_população () # Gere uma população aleatória de n cromossomas (soluções adequadas para o problema)
        repertir ate condicao final:
            avaliação () # Avalie a adequação f(x) de cada cromossoma x da população
            repetir ate nova que a nova pupulacao esteja completa:
                seleção_dos_pais ()
                cruzamento ()
                mutacao ()
            Utilize a nova população gerada para a próxima rodada do algoritmo
        retorne a melhor solução da população atual

    """
    pass

class Problem(object):
    """Classe para resolução do problema de clustering de Tweets"""

    def __init__(self, n, d, p_size, n_clusters):
        self.n = n # Matriz de dissimilaridade
        self.d = d # Tamanho da população
        self.p_size = p_size # Lista de indivíduos
        self.population = list() # Número de clusters
        self.n_clusters = n_clusters # Valor do fitness da população
        self.p_fitness = list()
        self.random_start()

    def random_start(self):
        """
        Aleatoriza p solucoes (individuos) para o problema
        (gera a populacao inicial - randomica)
        :return: none
        """

        '''Matriz len(d) x len(n_clusters) número de tweets X número de clusters'''
        for i in range(self.p_size):
            i_individual = [[0 for col in range(self.n_clusters)] for row in range(self.n)]
            '''Define o cluster o individuo i de maneira aleatória'''
            for j in range(self.n):
                i_individual[j][randint(0, self.n_clusters - 1)] = 1

            '''Adiciona o individuo na poulação'''
        self.population.append(i_individual)
        self.p_fitness.append(self.fitness(i_individual))
        self.sort_population()

    def sort_population(self):
        """
        Ordena os individuos da população pelo custo(crescente)
        :return: none
        """
        self.population = sorted(self.population, key=lambda x: self.fitness(x))

    def fitness(self, individual):
        """
        Define a apitidao de cada individuo (solucao)
        :param individual:
        :return:
        """
        fitness_value = 0
        for v in range(self.n_clusters):
            for k in range(self.n):
                for l in range(self.n):
                    fitness_value += individual[k][v] * individual[l][v] * self.d[k][l]
        return fitness_value

    def selection(self):
        """
        :param self:
        :return: uma tupla com as 2 melhores solucoes -- de melhor aptidao (fitness)
        """
        parents = (self.population.pop(0), self.population.pop(0)) # seleciona as duas melhores solucoes
        return parents

    def crossover(self, parents):
        """
        Faz o cruzamento entre dois individuos, gerando assim os descendentes
        :param parents: tupla contendo os pais
        :return:
        """
        pass

    def mutation(self, probabilidade):
        """
        Com a probabilidade de mutação, altere os cromossomas da nova geração nos locus (posição nos cromossomas).
        :return:
        """
        pass
