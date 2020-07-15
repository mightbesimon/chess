WHITE = 'white'
BLACK = 'black'


class Piece:

	def __init__(self, colour, pos):
		self.colour	= colour
		self.pos	= pos
		self.moved	= 0
		# self.rank, self.file = pos

	def __repr__(self):
		return (self.FIG[0] if self.colour==WHITE
		  else  self.FIG[1])

	def crawl(self, board, offsets):
		moves = []
		for row, col in offsets:
			r = self.pos[0]+row
			c = self.pos[1]+col

			while (board.check_bounds([r, c])
					and board.tiles[r][c] is None):
				moves.append([r, c])
				r += row
				c += col

			moves.append((r, c))

		return moves

	def is_legal(self, board, move):
		return (board.check_bounds(move)
			and (board.get(move).colour!=self.colour
					if board.get(move) else True)
			and not board.is_check(self.colour))	# this is wrong and needs fixing

	def get_legal_moves(self, board):
		return [ move for move in self.get_moves(board)
				if self.is_legal(board, move) ]





class King(Piece):

	NAME	= 'king'
	NOTE	= 'K'
	FIG		= '♔♚'

	def get_moves(self, board):
		cardinal_offsets = [
			[-1,  0], [ 0, -1],
			[ 1,  0], [ 0,  1],
		]
		diagonal_offsets = [
			[-1, -1], [-1,  1],
			[ 1, -1], [ 1,  1],
		]

		# CASTLING!!!!

		return [(self.pos[0]+row, self.pos[1]+col)		##pos##
							for row, col in cardinal_offsets
							               +diagonal_offsets]

class Pawn(Piece):

	NAME	= 'pawn'
	NOTE	= ''
	FIG		= '♙♟'
	VALUE	= 1

	def get_moves(self, board):
		offset = 1 if self.colour==WHITE else -1
		all_moves = []
		'''
		advance
			┏━━━┳━━━┳━━━┓
			┃   ┃ ✕ ┃   ┃
			┣━━━╋━━━╋━━━┫
			┃   ┃ ✕ ┃   ┃
			┣━━━╋━━━╋━━━┫
			┃   ┃ ♟ ┃   ┃
			┗━━━┻━━━┻━━━┛
		'''
		advance = (self.pos[0]+offset, self.pos[1])
		if (board.check_bounds(advance)
				and not board.get(advance)):
			all_moves.append(advance)

			advance_two = (self.pos[0] + offset*2, self.pos[1])
			if (board.check_bounds(advance_two)
					and not self.moved
					and not board.get(advance_two)):
				all_moves.append(advance_two)
		'''
		capture
			┏━━━┳━━━┳━━━┓
			┃   ┃   ┃   ┃
			┣━━━╋━━━╋━━━┫
			┃>♙<┃ ✕ ┃>♙<┃
			┣━━━╋━━━╋━━━┫
			┃   ┃ ♟ ┃   ┃
			┗━━━┻━━━┻━━━┛
		'''
		for offset_col in [-1, 1]:
			capture = (self.pos[0]+offset, self.pos[1]+offset_col)
			if (board.check_bounds(capture)
					and  board.get(capture)
					and  board.get(capture).colour!=self.colour):
				all_moves.append(capture)
		'''
		en passant
			┏━━━┳━━━┳━━━┓
			┃ ♙ ┃   ┃ ♙ ┃
			┣━━━╋━━━╋━━━┫
			┃ ✕ ┃ ✕ ┃   ┃
			┣━━━╋━━━╋━━━┫
			┃ ♟ ┃ ♙ ┃   ┃
			┗━━━┻━━━┻━━━┛
		'''
		# all_moves.append()
		'''
		promotion
		'''
		return all_moves

class Knight(Piece):

	NAME	= 'knight'
	NOTE	= 'N'
	FIG		= '♘♞'
	VALUE	= 3

	def get_moves(self, board):
		'''	┏━━━┳━━━┳━━━┳━━━┳━━━┓
			┃   ┃ ✕ ┃   ┃ ✕ ┃   ┃	[ 2, -1], [ 2,  1]
			┣━━━╋━━━╋━━━╋━━━╋━━━┫
			┃ ✕ ┃   ┃   ┃   ┃ ✕ ┃	[ 1, -2], [ 1,  2]
			┣━━━╋━━━╋━━━╋━━━╋━━━┫
			┃   ┃   ┃ ♞ ┃   ┃   ┃
			┣━━━╋━━━╋━━━╋━━━╋━━━┫
			┃ ✕ ┃   ┃   ┃   ┃ ✕ ┃	[-1, -2], [-1,  2]
			┣━━━╋━━━╋━━━╋━━━╋━━━┫
			┃   ┃ ✕ ┃   ┃ ✕ ┃   ┃	[-2, -1], [-2,  1]
			┗━━━┻━━━┻━━━┻━━━┻━━━┛
		'''
		offsets = [
			[-2, -1], [-2,  1],
			[-1, -2], [-1,  2],
			[ 1, -2], [ 1,  2],
			[ 2, -1], [ 2,  1],
		]

		return [(self.pos[0]+row, self.pos[1]+col)
							for row, col in offsets]


class Bishop(Piece):

	NAME	= 'bishop'
	NOTE	= 'B'
	FIG		= '♗♝'
	VALUE	= 3

	def get_moves(self, board):
		diagonal_offsets = [
			[-1, -1], [-1,  1],
			[ 1, -1], [ 1,  1],
		]
		return self.crawl(board, diagonal_offsets)

class Rook(Piece):

	NAME	= 'rook'
	NOTE	= 'R'
	FIG		= '♖♜'
	VALUE	= 5

	def get_moves(self, board):
		cardinal_offsets = [
			[-1,  0], [ 0, -1],
			[ 1,  0], [ 0,  1],
		]
		return self.crawl(board, cardinal_offsets)

class Queen(Piece):

	NAME	= 'queen'
	NOTE	= 'Q'
	FIG		= '♕♛'
	VALUE	= 9

	def get_moves(self, board):
		cardinal_offsets = [
			[-1,  0], [ 0, -1],
			[ 1,  0], [ 0,  1],
		]
		diagonal_offsets = [
			[-1, -1], [-1,  1],
			[ 1, -1], [ 1,  1],
		]
		return self.crawl(board, cardinal_offsets
								+diagonal_offsets)


