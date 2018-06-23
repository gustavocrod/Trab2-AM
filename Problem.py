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
		# Lista de gerações
		self.generations = list()
		# Número de clusters
		self.n_clusters = n_clusters
		self.random_start()
	
	def random_start(self):
		population = list()
		for i in range(self.p_size):
			# Matriz len(d) x len(n_clusters) número de tweets X número de clusters
			i_individual = [[0 for col in range(self.n_clusters)] for row in range(self.n)]
			# Define o cluster o individuo i de maneira aleatória
			for j in range(self.n):
				i_individual[j][randint(0, self.n_clusters - 1)] = 1
			# Adiciona o individuo na poulação
			population.append(i_individual)		
		self.generations.append(population)
	
	def fitness(self):
		pass
	def select(self):
		pass
		