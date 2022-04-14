from random import shuffle, randint
from time import sleep
import turtle

class Sudoku:
	grid = [] # grade 9x9 do sudoku
	adj = [] # grafo por lista de adjacência
	index = [] # associa cada posição da matriz à um índice
	color = {} # cor do nó (cada cor representa o número)
	inv = {}

  # inicializa a grade do sudoku vazia (preenchida com zeros)
	def __init__(self, grid=None):
		if grid is None:
			for _ in range(9):
				self.grid.append([0] * 9)
		else:
			self.grid = grid

		# inicializa o array de indices
		for _ in range(9):
			self.index.append([0] * 9)

		# inicializa lista de adjacência
		for _ in range(81):
			self.adj.append([])

		# configurações do turtle
		self.myPen = turtle.Turtle()
		self.myPen._tracer(0)
		self.myPen.speed(0)
		self.myPen.color('#000000')
		self.myPen.hideturtle()

		self.topLeft_x = -150
		self.topLeft_y = 150

  # imprime o sudoku no terminal
	def __str__(self):
		str_sudoku = ''

		for row in range(9):
			str_sudoku += ' '.join([str(number) for number in self.grid[row]]).replace('0', '_') + '\n'

		return str_sudoku
	
	# imprime um texto nas coordenadas (x, y) com turtle
	def text(self, number, x, y, size, show_colors=False):
		background_colors = ['#FFFFFF', '#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA', '#F3E9DD', '#D1D1D1', '#FFC4E1']

		if show_colors:
			self.myPen.penup()
			self.myPen.goto(x-10.5, y+30.5)

			self.myPen.fillcolor(background_colors[number])
			self.myPen.begin_fill()
			
			for _ in range(4):
				self.myPen.forward(32.8)
				self.myPen.right(90)

			self.myPen.end_fill()

		if number != 0:
			self.myPen.penup()
			self.myPen.goto(x, y)
			self.myPen.write(number, align='left', font=('Arial', size, 'normal'))
		else:
			self.myPen.getscreen().update()

	# remove o valor da célula no desenho do turtle
	def draw_empty_cell(self, node):
		row, column = self.inv[node]
		intDim=35
		
		self.text(self.grid[row][column], self.topLeft_x + column*intDim + 12, self.topLeft_y - row*intDim - intDim + 3, 18, True)

	# desenha sudoku com turtle
	def draw(self, show_colors=True):
		self.myPen.clear()

		intDim=35
		for row in range(10):
			if row % 3 == 0:
				self.myPen.pensize(3)
			else:
				self.myPen.pensize(1)
			
			self.myPen.penup()
			self.myPen.goto(self.topLeft_x, self.topLeft_y - row*intDim)
			self.myPen.pendown()
			self.myPen.goto(self.topLeft_x + 9*intDim, self.topLeft_y - row*intDim)
		
		for col in range(10):
			if col % 3 == 0:
				self.myPen.pensize(3)
			else:
				self.myPen.pensize(1)
			    
			self.myPen.penup()
			self.myPen.goto(self.topLeft_x + col*intDim, self.topLeft_y)
			self.myPen.pendown()
			self.myPen.goto(self.topLeft_x + col*intDim, self.topLeft_y - 9*intDim)

		for row in range (9):
			for col in range (9):
				if self.grid[row][col] != 0:
					self.text(self.grid[row][col], self.topLeft_x + col*intDim + 12, self.topLeft_y - row*intDim - intDim + 3, 18, show_colors)
		
		self.myPen.getscreen().update()

	# colore um nó de acordo com o índice na lista de adjacência
	def paint(self, node, color):
		self.color[node] = color
		self.grid[ self.inv[node][0] ][ self.inv[node][1] ] = color

	# gera o grafo por lista de adjacência baseado na grade do sudoku
	def build_graph(self):
		# gera os índices na lista de adjacência
		current_index = 0
		for i in range(9):
			for j in range(9):
				current_index += 1

				self.inv[current_index] = (i, j)
				self.index[i][j] = current_index
				self.color[current_index] = self.grid[i][j]

		# conecta os nós da mesma linha e mesma coluna
		for row in range(9):
			for column in range(9):
				# mesma linha
				for new_row in range(9):
					if row != new_row:
						self.adj[ self.index[row][column] ].append( self.index[new_row][column] )
				
				# mesma coluna
				for new_column in range(9):
					if column != new_column:
						self.adj[ self.index[row][column] ].append( self.index[row][new_column] )
		
		# conecta os nós do mesmo bloco 3x3
		for row in range(0, 9, 3):
			for column in range(0, 9, 3):
				# processa bloco que começa na posição [row][column]
				for old_row in range(row, row+3):
					for old_column in range(column, column+3):
						for new_row in range(row, row+3):
							for new_column in range(column, column+3):
								if not (old_row == new_row and old_column == new_column):
									# cria uma aresta entre u e v
									u = self.index[old_row][old_column]
									v = self.index[new_row][new_column]

									self.adj[u].append(v)

# gera um padrão aleatório de números de 1 à 9
def generate_random_pattern():
	random_pattern = [number for number in range(1, 10)]
	shuffle(random_pattern)
	
	return random_pattern

# verifica se o array number contém exatamente uma ocorrência dos elementos de 1 até 9
def has_distinct_numbers(numbers):
	# caso não exista exatamente uma ocorrência do número retorna falso
	for number in range(1, 10):
		if numbers[number] > 1:
			return False

	return True

# checa se a linha é válida
def check_row(sudoku, row):
	numbers = [0] * 10 # indica a quantidade de números iguais a i na posição i

	for column in range(9):
		numbers[ sudoku.grid[row][column] ] += 1

	return has_distinct_numbers(numbers)

# checa se a coluna é válida
def check_column(sudoku, column):
	numbers = [0] * 10 # indica a quantidade de números iguais a i na posição i

	for row in range(9):
		numbers[ sudoku.grid[row][column] ] += 1

	return has_distinct_numbers(numbers)

# checa se o bloco 3x3 é válido (começando em [row][column])
def check_block(sudoku, row, column):
	numbers = [0] * 10 # indica a quantidade de números iguais a i na posição i

	for row_it in range(row, row+3):
		for column_jt in range(column, column+3):
			numbers[ sudoku.grid[row_it][column_jt] ] += 1

	return has_distinct_numbers(numbers)

# checa se o sudoku é uma solução válida
def check(sudoku):
	# verifica as linhas
	for row in range(9):
		if not check_row(sudoku, row):
			return False

	# verifica as colunas
	for column in range(9):
		if not check_column(sudoku, column):
			return False

	# verifica os blocos 3x3
	for row in range(0, 9, 3):
		for column in range(0, 9, 3):
			if not check_block(sudoku, row, column):
				return False

	return True

# gera um tabuleiro de sudoku aleatório
def generate(show_steps=False):
	sudoku = Sudoku()
	sudoku.build_graph() # cria grafo com lista de adjacência

	coloring(sudoku, generate_random_pattern(), 1, False, False) # colore o sudoku com o padrão aleatório

	if show_steps:
		sudoku.draw()

	# remove elementos do sudoku para gerar um jogo
	for node in range(1, 82):
		# 60% de chance de remover a célula (sudoku nível intermediário)
		if randint(0, 10) < 6:
			sudoku.paint(node, 0)

			if show_steps:
				sudoku.draw_empty_cell(node)
				sleep(0.1)

	return sudoku

def coloring(sudoku, pattern, node, show_steps=False, show_colors=False):
	if show_steps:
		sudoku.draw(show_colors)

	# caso base é chegar no nó 9*9+1 (inexistente)
	if node == 82:
		return True

	# se o nó já está colorido, avança para o próximo nó
	if sudoku.color[node] != 0:
		return coloring(sudoku, pattern, node+1, show_steps, show_colors)

	found_color = False # indica se encontrou uma cor válida para o nó atual
	for color in pattern: # testa as cores de 1 à 9
		color_is_valid = True

		# verifica se há uma cor igual nos vizinhos
		for neighbor in sudoku.adj[node]:
			if sudoku.color[neighbor] == color:
				color_is_valid = False
				break
		
		if color_is_valid:
			sudoku.paint(node, color)
			found_color = coloring(sudoku, pattern, node+1, show_steps, show_colors)
			
			# se a cor escolhida não gerou uma solução válida, preenche novamente com zero
			if not found_color:
				sudoku.paint(node, 0)
			else:
				return True

	return found_color

def main():
	# exemplos dados nas especificações do projeto
	sudoku_example = Sudoku([
		[8, 0, 0, 1, 5, 0, 6, 0, 0],
		[0, 0, 0, 3, 0, 0, 0, 4, 1],
		[5, 0, 0, 0, 0, 0, 7, 0, 0],
		[0, 0, 0, 0, 0, 9, 0, 6, 2],
		[0, 0, 0, 0, 3, 0, 0, 0, 0],
		[1, 4, 0, 8, 0, 0, 0, 0, 0],
		[0, 0, 8, 0, 0, 0, 0, 0, 9],
		[2, 9, 0, 0, 0, 1, 0, 0, 0],
		[0, 0, 5, 0, 9, 7, 0, 0, 6],
	])

	sudoku_example_solution = Sudoku([
		[8, 7, 4, 1, 5, 2, 6, 9, 3],
		[6, 2, 9, 3, 7, 8, 5, 4, 1],
		[5, 3, 1, 9, 6, 4, 7, 2, 8],
		[3, 5, 7, 4, 1, 9, 8, 6, 2],
		[9, 8, 2, 7, 3, 6, 1, 5, 4],
		[1, 4, 6, 8, 2, 5, 9, 3, 7],
		[7, 6, 8, 5, 4, 3, 2, 1, 9],
		[2, 9, 3, 6, 8, 1, 4, 7, 5],
		[4, 1, 5, 2, 9, 7, 3, 8, 6],
	])

	sudoku = generate(True) # gera um sudoku aleatório
	print(f'Sudoku gerado:\n{sudoku}')
	print('\nPressione CTRL+C para sair.')
	sleep(1)

	# gera uma solução para o sudoku com coloração de grafos
	show_steps = True # indica se é para mostrar os passos intermediários
	show_colors = True # indica se é para mostrar as cores de cada vértice (Atenção: alternância de cores frequente)
	coloring(sudoku, generate_random_pattern(), 1, show_steps, show_colors)

	print(f'Solução:\n{sudoku}')

	# verifica se a solução é válida
	print(f'A solução é válida? {"Sim" if check(sudoku) else "Não"}')

	print('\nPressione CTRL+C para sair.')
	while True:
		pass

# executa a função main por padrão
if __name__ == '__main__':
	main()