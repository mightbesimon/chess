from piece import *

WHITE = 'white'
BLACK = 'black'


class Board:

	PLAYERS		= 2
	DIMENSIONS	= (8, 8)

	def __init__(self, ranks=8, files=8):
		self.DIMENSIONS = (ranks, files)
		self.tiles = [ [None]*self.DIMENSIONS[1] for _ in range(self.DIMENSIONS[0]) ]

	# def __repr__(self):
	# 	return self.display()

	def set_up(self):
		self.tiles[0] = [
			Rook  (WHITE, [0, 0]),
			Knight(WHITE, [0, 1]),
			Bishop(WHITE, [0, 2]),
			Queen (WHITE, [0, 3]),
			King  (WHITE, [0, 4]),
			Bishop(WHITE, [0, 5]),
			Knight(WHITE, [0, 6]),
			Rook  (WHITE, [0, 7]),
		]
		self.tiles[1] = [
			Pawn(WHITE, [1, col])
			for col in range(self.DIMENSIONS[1])
		]

		self.tiles[self.DIMENSIONS[0]-2] = [
			Pawn(BLACK, [self.DIMENSIONS[0]-2, col])
			for col in range(self.DIMENSIONS[1])
		]
		self.tiles[self.DIMENSIONS[0]-1] = [
			Rook  (BLACK, [self.DIMENSIONS[0]-1, 0]),
			Knight(BLACK, [self.DIMENSIONS[0]-1, 1]),
			Bishop(BLACK, [self.DIMENSIONS[0]-1, 2]),
			Queen (BLACK, [self.DIMENSIONS[0]-1, 3]),
			King  (BLACK, [self.DIMENSIONS[0]-1, 4]),
			Bishop(BLACK, [self.DIMENSIONS[0]-1, 5]),
			Knight(BLACK, [self.DIMENSIONS[0]-1, 6]),
			Rook  (BLACK, [self.DIMENSIONS[0]-1, 7]),
		]

	def display(self, piece=None):
		legal_moves = piece.get_legal_moves(self) if piece else []
		
		# print('    a   b   c   d   e   f   g   h'  )
		# print('  ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓')
		print('    '+'   '.join([chr(97+n) for n in range(self.DIMENSIONS[1])]))
		print('  '  +'━━━'.join(['┏'] + ['┳']*(self.DIMENSIONS[1]-1) + ['┓']))

		for row in range(self.DIMENSIONS[0])[::-1]:
			print((row+1) % 10, '┃', end='')
			for col in range(self.DIMENSIONS[1]):
				if [row, col] in legal_moves:
					if self.tiles[row][col]:
						print(f'>{self.tiles[row][col]}<', end='')
					else:
						print(' ✕ ', end='')
				else:
					if self.tiles[row][col]:
						print(f' {self.tiles[row][col]} ', end='')
					else:
						print('   ', end='')
				print('┃', end='')

			print('', (row+1) % 10)
			# if row: print('  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫')
			if row: print('  '+'━━━'.join(['┣'] + ['╋']*(self.DIMENSIONS[1]-1) + ['┫']))


		# print('  ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛')
		# print('    a   b   c   d   e   f   g   h'  )
		print('  '  +'━━━'.join(['┗'] + ['┻']*(self.DIMENSIONS[1]-1) + ['┛']))
		print('    '+'   '.join([chr(97+n) for n in range(self.DIMENSIONS[1])]))

		print('evaluation =', self.evaluation())

		if piece and legal_moves:
			print(*[ chr(97+move[1])+str(move[0]+1)
							for move in legal_moves ])
		if piece and not legal_moves: print('[no moves]')

	def decode_coord(self, coord):
		try:
			if not coord[0].isalpha(): return None
			return [int(coord[1:])-1, ord(coord[0])-97]
		except:
			return None

	# def coords(self, pos):
	# 	return chr(97+pos[1])+str(pos[0]+1)

	def get(self, pos):
		return self.tiles[pos[0]][pos[1]]

	def set(self, pos, piece):
		self.tiles[pos[0]][pos[1]] = piece

	def make_move(self, piece, destination):
		self.set(piece.pos, None)
		self.set(destination, piece)
		piece.pos = destination
		piece.moved += 1

	def capture(self): pass			# here
	def castle(self): pass			# here

	def check_bounds(self, pos):
		return (0<=pos[0]<self.DIMENSIONS[0]
		   and  0<=pos[1]<self.DIMENSIONS[1])

	def is_check(self, colour):
		for row in range(self.DIMENSIONS[0]):
			for col in range(self.DIMENSIONS[1]):
				piece = self.tiles[row][col]

				if piece and piece.colour!=colour:
					all_moves = piece.get_moves(self)
					for move in all_moves:
						if self.check_bounds(move):
							piece = self.get(move)
							if piece and type(piece)==King and piece.colour==colour:
								return True
		return False

	def is_checkmate(self, colour):
		return self.is_check(colour) and not self.get_all_legal_moves(colour)

	def get_all_legal_moves(self, colour):
		all_legal_moves = []
		for row in range(self.DIMENSIONS[0]):
			for col in range(self.DIMENSIONS[1]):
				piece = self.tiles[row][col]

				if piece and piece.colour==colour:
					for move in piece.get_legal_moves(self):
						all_legal_moves.append([piece, move])

		return all_legal_moves

	def evaluation(self):
		_evaluation = 0
		for row in range(self.DIMENSIONS[0]):
			for col in range(self.DIMENSIONS[1]):
				piece = self.tiles[row][col]

				if piece and type(piece)!=King:
					_evaluation += piece.VALUE * (1 if piece.colour==WHITE else -1)

		return _evaluation

	def make_notation(self, piece, destination): pass
		# Qxd4
		# return f'{piece.NOTE}{'x' if self.get(destination) else ''}{destination[1]}{destination[0]+1}'

