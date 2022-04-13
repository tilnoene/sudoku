from random import shuffle, randint
from timeit import default_timer

class Sudoku:
	grid = [] # grade 9x9 do sudoku

  # inicializa a grade do sudoku vazia (preenchida com zeros)
	def __init__(self, grid=None):
		if grid is None:
			for _ in range(9):
				self.grid.append([0] * 9)
		else:
			self.grid = grid

  # imprime o sudoku no terminal
	def __str__(self):
		str_sudoku = ''

		for row in range(9):
			str_sudoku += ' '.join([str(number) for number in self.grid[row]]).replace('0', '_') + '\n'

		return str_sudoku

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
	for row in range(9):
		if not check_row(sudoku, row):
			return False

	for column in range(9):
		if not check_column(sudoku, column):
			return False

	for row in range(0, 9, 3):
		for column in range(0, 9, 3):
			if not check_block(sudoku, row, column):
				return False

	return True

solution_found = False
def dfs(sudoku, pattern, row, column):
	global solution_found
	if sudoku.grid[row][column] != 0:
		if row == 8 and column == 8: # caso base = célula da direita inferior
			solution_found = True
			return
		elif column == 8:
			dfs(sudoku, pattern, row+1, 0)
		else:
			dfs(sudoku, pattern, row, column+1)
		
		return

	for number in pattern:
		if solution_found:
			return

		sudoku.grid[row][column] = number

		if check(sudoku):
			if row == 8 and column == 8: # caso base = célula da direita inferior
				solution_found = True
				return
			elif column == 8:
				dfs(sudoku, pattern, row+1, 0)
			else:
				dfs(sudoku, pattern, row, column+1)

	if not solution_found:
		# não achou uma solução, então volta no backtracking para escolher outros números
		sudoku.grid[row][column] = 0

def generate():
	global solution_found
	sudoku = Sudoku()
	pattern = generate_random_pattern()
	
	start = default_timer()

	solution_found = False
	dfs(sudoku, pattern, 0, 0)

	stop = default_timer()
	print('Time: ', stop - start) 

	return sudoku

def main():
	# exemplos dados no roteiro do projeto
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

	# verifica se a solução do sudoku de exemplo é válida
	# print(check(sudoku_example_solution))
	
	sudoku = generate()
	print(sudoku)
	print(check(sudoku))


# executa a função main por padrão
if __name__ == '__main__':
	main()