from random import randint

class Problem(object):
	"""Classe para resolução do problema de clustering de Tweets"""
	def __init__(self, n, d, p_size, n_clusters):
		# Número de tweets
		self.n = n
		# Matriz de dissimilaridade
		self.d = d
		# Tamanho da população
		self.p_size = p_size
		# Lista de indivíduos
		self.population = list()
		# Número de clusters
		self.n_clusters = n_clusters
		# Valor do fitness da população
		self.p_fitness = list()
		self.random_start()
	
	def random_start(self):		
		for i in range(self.p_size):
			# Matriz len(d) x len(n_clusters) número de tweets X número de clusters
			i_individual = [[0 for col in range(self.n_clusters)] for row in range(self.n)]
			# Define o cluster o individuo i de maneira aleatória
			for j in range(self.n):
				i_individual[j][randint(0, self.n_clusters - 1)] = 1
			# Adiciona o individuo na poulação
			self.population.append(i_individual)		
			self.p_fitness.append(self.fitness(i_individual))

		# Ordena os individuos da população pelo custo(crescente)
		self.population = sorted(self.population, key = lambda x: self.fitness(x))		
	
	def fitness(self, individual):
		fitness_value = 0
		for v in range(self.n_clusters):
			for k in range(self.n):
				for l in range(self.n):
					fitness_value += individual[k][v] * individual[l][v] * self.d[k][l]
		return fitness_value

	def select(self):
		pass
		