from random import randrange
import copy

class Kmedoids():
	def __init__(self, data, k, m):
		self.data = data
		self.n = len(data)
		self.k = k
		self.m = m
		self.medoids = list()
	
	def get_cost(self):
		cost = 0
		# Percorre os medoides
		for i in range(len(self.medoids)):
			# percorre os objetos (dados)
			for j in range(self.n):
				# verifica se o dado[j] está conectado ao medoide[i]
				if self.data[j][1] == self.medoids[i]:
					# Se estiver conectado acrescenta ao custo, a disssimilaridade
					# do objeto j com o medoide i					
					cost += self.m[i][j]
		return cost

	def random_start(self):
		n = len(self.data)
		# Selecionar k objetos representativos randomicamente
		while len(self.medoids) < self.k:
			random_medoid = randrange(n)
			if not random_medoid in self.medoids:
				self.medoids.append(random_medoid)
	
	def assign_to_medoid(self):
		for i in range(self.n):
			# dissimilaridade do objeto i com relação ao objeto 
			dissimilarity = [self.m[i][j] for j in self.medoids]
			self.data[i][1] = dissimilarity.index(min(dissimilarity))		

	def update(self):
		changed = False
		# Percorre os medoids e verifica se mudar o medoid i por um membro j melhora a solução
		for i in range(len(self.medoids)):
			for j in range(self.n):
				current_cost = self.get_cost()				
				
				if self.data[j][1] == self.medoids[i]:
					medoid_index = copy.copy(self.medoids[i]) #indice do objeto que era medoide
					object_index = j # indice do objeto que vai virar medoide
					# Coloca o indice do objeto no lugar do antigo medoide
					self.medoids[i] = j
					# Faz com que o objeto que era medoide seja conectado ao novo medoide( Não sei se é preciso)
					self.data[medoid_index][1] = j

					new_cost = self.get_cost()					
					if new_cost > current_cost:						
						self.medoids[i] = medoid_index
						self.data[object_index][1] == medoid_index
					else:
						changed = True

		return changed