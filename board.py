from piece import *

WHITE = 'white'
BLACK = 'black'


class Board:

	PLAYERS		= 2
	DIMENSIONS	= (8, 8)

	def __init__(self, ranks=8, files=8):
		self.DIMENSIONS = (ranks, files)
		self.tiles = [ [None]*self.DIMENSIONS[1] for _ in range(self.DIMENSIONS[0]) ]
		self.captured = {}
		for _ in [WHITE, BLACK]:
			self.captured[_] = []

	# def __repr__(self):
	# 	return self.display()

	def set_up(self):
		# for n*8 boards only
		self.tiles[0] = [
			Rook  (WHITE, self, (0, 0)),
			Knight(WHITE, self, (0, 1)),
			Bishop(WHITE, self, (0, 2)),
			Queen (WHITE, self, (0, 3)),
			King  (WHITE, self, (0, 4)),
			Bishop(WHITE, self, (0, 5)),
			Knight(WHITE, self, (0, 6)),
			Rook  (WHITE, self, (0, 7)),
		]
		self.tiles[1] = [
			Pawn(WHITE, self, (1, col))
			for col in range(self.DIMENSIONS[1])
		]

		self.tiles[self.DIMENSIONS[0]-2] = [
			Pawn(BLACK, self, (self.DIMENSIONS[0]-2, col))
			for col in range(self.DIMENSIONS[1])
		]
		self.tiles[self.DIMENSIONS[0]-1] = [
			Rook  (BLACK, self, (self.DIMENSIONS[0]-1, 0)),
			Knight(BLACK, self, (self.DIMENSIONS[0]-1, 1)),
			Bishop(BLACK, self, (self.DIMENSIONS[0]-1, 2)),
			Queen (BLACK, self, (self.DIMENSIONS[0]-1, 3)),
			King  (BLACK, self, (self.DIMENSIONS[0]-1, 4)),
			Bishop(BLACK, self, (self.DIMENSIONS[0]-1, 5)),
			Knight(BLACK, self, (self.DIMENSIONS[0]-1, 6)),
			Rook  (BLACK, self, (self.DIMENSIONS[0]-1, 7)),
		]

	def display(self, piece=None):
		legal_moves = piece.get_legal_moves() if piece else []

		# print('    a   b   c   d   e   f   g   h'  )
		# print('  ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓')
		print('    '+'   '.join([chr(97+n) for n in range(self.DIMENSIONS[1])]))
		print('  '  +'━━━'.join(['┏'] + ['┳']*(self.DIMENSIONS[1]-1) + ['┓']))

		for row in range(self.DIMENSIONS[0])[::-1]:
			print((row+1) % 10, '┃', end='')
			for col in range(self.DIMENSIONS[1]):
				if (row, col) in legal_moves:
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

		if legal_moves:
			print(*[ chr(97+move.dst[1])+str(move.dst[0]+1)
							for move in legal_moves ])
		elif piece: print('[no moves]')

	def decode_coord(coord):
		try:
			if not coord[0].isalpha(): return None
			return (int(coord[1:])-1, ord(coord[0])-97)
		except:
			return None

	def clone(self):
		copy = Board()
		copy.DIMENSIONS = self.DIMENSIONS[:]
		for row in range(self.DIMENSIONS[0]):
			for col in range(self.DIMENSIONS[1]):
				piece = self.tiles[row][col]
				copy.tiles[row][col] = piece.clone(copy) if piece else None

		return copy

##### ^ initialise, setup || input/output ^ #####
##### condition functions #####


	def get(self, pos):
		return self.tiles[pos[0]][pos[1]] if self.check_bounds(pos) else False

	def set(self, pos, piece):
		self.tiles[pos[0]][pos[1]] = piece

	def check_bounds(self, pos):
		return (0<=pos[0]<self.DIMENSIONS[0]
		   and  0<=pos[1]<self.DIMENSIONS[1])

	def iterate(self):
		return [piece for row in self.tiles
						for piece in row if piece]

	def is_check(self, colour):
		# check to see if opponent can make
		# any move to take the king
		# does not have to be legal moves
		# since player is under check if there is any move
		for piece in self.iterate():
			if piece.colour==colour: continue
			for move in piece.get_moves():
				_piece = self.get(move.dst)
				if type(_piece)==King and _piece.colour==colour:
					return True
		return False

	def is_checkmate(self, colour):
		''' checkmate conditions:
			 - is currently in check
			 - no legal moves
		'''
		return self.is_check(colour)	\
		   and not self.get_all_legal_moves(colour)

	def is_stalemate(self, colour):
		'''	stalemate conditions:
			 - is not currently under check
			 - no legal moves
		'''
		return not self.is_check(colour)	\
		   and not self.get_all_legal_moves(colour)

##### eval functions #####

	def get_all_legal_moves(self, colour):
		all_legal_moves = []
		for piece in self.iterate():
			if piece.colour!=colour: continue
			all_legal_moves.extend(piece.get_legal_moves())

		return all_legal_moves

	def evaluation(self):
		_evaluation = 0
		for piece in self.iterate():
			if type(piece)==King: continue
			_evaluation += piece.VALUE * (1 if piece.colour==WHITE else -1)

		return _evaluation

