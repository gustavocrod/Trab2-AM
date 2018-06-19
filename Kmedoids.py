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
			if i not in self.medoids:
				# dissimilaridade do objeto i com relação ao objeto 
				dissimilarity = [self.m[i][j] for j in self.medoids]
				self.data[i][1] = self.medoids[dissimilarity.index(min(dissimilarity))]

	def update(self):
		changed = False
		# Percorre os medoids e verifica se mudar o medoid i por um membro j melhora a solução
		for i in range(len(self.medoids)):
			i_medoid_objects = [j for j in range(self.n) if self.data[j][1] == self.medoids[i]]
			# Custo atual antes da troca de pares
			for o in i_medoid_objects:				
				current_cost = self.get_cost()
				print(self.medoids)
				print("Custo corrente: {}".format(current_cost))
				# Objeto que era medoide
				old_medoid_obj_index = copy.copy(self.medoids[i])
				# Objeto que "tentar ser" o novo medoide
				new_medoid_candidate = copy.copy(o)
				# Faz a troca de pares
				# O medoide i, passa a ser novo candidato
				self.medoids[i] = new_medoid_candidate
				# O objeto que era medoide é conectado ao medoide novo
				self.data[old_medoid_obj_index][1] = new_medoid_candidate
				print("Trocou o medoide {}".format(i))
				print(self.medoids)
				new_cost = self.get_cost()
				print("Novo custo: {}".format(new_cost))
				if new_cost < current_cost:		
					changed = True
				else:
					print("Desfez a troca do medoide {}".format(i))
					# O medoid i recebe o objeto que era medoide antes da troca
					self.medoids[i] = old_medoid_obj_index
					# O objeto que se tornou medoide na iteração é conectado ao antigo medoide
					self.data[new_medoid_candidate][1] = old_medoid_obj_index
					print(self.medoids)				
		return changed