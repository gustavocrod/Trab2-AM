class Individual():
	"""
		Um individuo eh uma matriz
	"""
	def __init__(self, membership_matrix, generation):
		self.fitness = 0.0000000 # Aptidao do moco no mundo a fora
		self.membership_matrix = membership_matrix # membership de cada tweet (n_tweets x n_cluster)
		self.id = 0
		self.generation = generation
