from piece import *

WHITE = 'white'
BLACK = 'black'


class Board:

	def __init__(self, ranks=8, files=8):
		self.dim    = (ranks, files)
		self._tiles = [ [None]*self.dim[1]
				for _ in range(self.dim[0]) ]

	def __getitem__(self, key):
		'''	@use
			board[r, c] <- board._tiles[r][c]
		'''
		if not self.check_bounds(key): return False
		row, col = key
		return self._tiles[row][col]

	def __setitem__(self, key, value):
		row, col = key
		self._tiles[row][col] = value

	def __iter__(self):
		'''iterate through the pieces on the board'''
		return iter([piece for row in self._tiles
						for piece in row if piece])

	def __repr__(self):
		return self._repr_small()

	def _repr_small(self):
		return '\n'.join(
			[' '.join([repr(p) if p else '.' for p in rank])
			for rank in self._tiles[::-1]]
		)

	def _repr_large(self, piece=None):
		legal_moves = piece.get_legal_moves() if piece else []

		num_rows = self.dim[0]
		num_cols = self.dim[1]
		#     a   b   c   d   e   f   g   h
		file_letters = [chr(97+n) for n in range(num_cols)]
		ret = '    '+'   '.join(file_letters)+'\n'
		#   ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
		top_corners = '━━━'.join(['┏'] + ['┳']*(num_cols-1) + ['┓'])
		ret += f'  {top_corners}\n'

		for row in range(self.dim[0])[::-1]:
			ret += str((row+1) % 10) + ' '
			ret +='┃'
			for col in range(num_cols):
				piece = self[row, col]
				if (row, col) in legal_moves:
					ret += f'>{self[row, col]}<'\
					if piece else ' ✕ '
				else:
					ret += f' {self[row, col]} '\
					if piece else '   '
				ret += '┃'
			ret += ' '
			ret += str((row+1) % 10) + '\n'
			#   ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
			cells = '━━━'.join(['┣'] + ['╋']*(num_cols-1) + ['┫'])
			if row: ret += f'  {cells}\n'
		#   ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
		bottom_corners = '━━━'.join(['┗'] + ['┻']*(num_cols-1) + ['┛'])
		ret += f'  {bottom_corners}\n'
		#     a   b   c   d   e   f   g   h
		ret += '    '+'   '.join(file_letters)+'\n'

		if piece and not legal_moves:
			ret += '[no moves]\n'
		ret += f'evaluation = {self.evaluate()}'
		return ret

	def clone(self):
		copy = Board(*self.dim)
		for piece in self:
			copy[piece.pos] = piece.clone(board=copy)
		return copy

	# def get_pieces(self, colour):
	# 	return [piece for piece in self
	# 			if piece.colour==colour]

	def set_up(self):
		last_rank = self.dim[0]-1
		num_files = self.dim[1]

		# types = [ Rook, Knight, Bishop, Queen,
		#           King, Bishop, Knight, Rook ]

		self[0, :] = [
			Rook  (WHITE, self, (0, 0)),
			Knight(WHITE, self, (0, 1)),
			Bishop(WHITE, self, (0, 2)),
			Queen (WHITE, self, (0, 3)),
			King  (WHITE, self, (0, 4)),
			Bishop(WHITE, self, (0, 5)),
			Knight(WHITE, self, (0, 6)),
			Rook  (WHITE, self, (0, 7)),
		]
		self[1, :] = [
			Pawn(WHITE, self, (1, col))
			for col in range(num_files)
		]

		self[last_rank-1, :] = [
			Pawn(BLACK, self, (last_rank-1, col))
			for col in range(num_files)
		]
		self[last_rank, :] = [
			Rook  (BLACK, self, (last_rank, 0)),
			Knight(BLACK, self, (last_rank, 1)),
			Bishop(BLACK, self, (last_rank, 2)),
			Queen (BLACK, self, (last_rank, 3)),
			King  (BLACK, self, (last_rank, 4)),
			Bishop(BLACK, self, (last_rank, 5)),
			Knight(BLACK, self, (last_rank, 6)),
			Rook  (BLACK, self, (last_rank, 7)),
		]

	def check_bounds(self, pos):
		return 0<=pos[0]<self.dim[0]\
		   and 0<=pos[1]<self.dim[1]

	def is_check(self, colour):
		# check to see if opponent can make
		# any move to take the king
		# does not have to be legal moves
		# since player is under check if there is any move
		for piece in self:
			if piece.colour==colour: continue
			for move in piece.get_moves():
				dst_tile = self[move.dst]
				if type(dst_tile)==King \
				and dst_tile.colour==colour:
					return True
		return False

	def get_all_legal_moves(self, colour):
		# print('TIME TIME')
		all_legal_moves = []
		for piece in self:
			if piece.colour!=colour: continue
			all_legal_moves.extend(piece.get_legal_moves())

		return all_legal_moves

	def evaluate(self):
		evaluation = 0
		mul = { WHITE: 1, BLACK: -1 }
		for piece in self:
			if type(piece)==King: continue
			evaluation += piece.VALUE * mul[piece.colour]

		return evaluation



# if __name__ == '__main__':

# 	board = Board()
# 	print('dim:', board.dim)

# 	board.set_up()
# 	print('board:', board, sep='\n')
# 	print(board._repr_large())
# 	print(board._repr_large(board[1, 1]))
	# print('board._tiles:', board._tiles)

	# print('board[1, 1]:', board[1, 1])
	# print('__iter__:', [p for p in board])

	# copy = board.clone()
	# copy[1, 1] = None
	# print('clone, {original} {copy}:',
	# 									)
	# 			# board, copy, sep='\n')
	# print(board.dim, copy.dim)

	# pos = (0, 8)
	# print('check_bounds, pos=(0, 8):',
	# 			board.check_bounds(pos))

	# print(board.get_all_legal_moves('white'))


