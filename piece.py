from move  import *

WHITE = 'white'
BLACK = 'black'


cardinal_offsets = [		#	┏━━━┳━━━┳━━━┓
	[-1,  0], [ 0, -1],		#	┃   ┃ ✕ ┃   ┃	[ 1,  0], [ 0,  1]
	[ 1,  0], [ 0,  1],		#	┣━━━╋━━━╋━━━┫
]							#	┃ ✕ ┃ ♜ ┃ ✕ ┃
							#	┣━━━╋━━━╋━━━┫
							#	┃   ┃ ✕ ┃   ┃	[-1,  0], [ 0, -1]
							#	┗━━━┻━━━┻━━━┛

diagonal_offsets = [		#	┏━━━┳━━━┳━━━┓
	[-1, -1], [-1,  1],		#	┃ ✕ ┃   ┃ ✕ ┃	[ 1, -1], [ 1,  1]
	[ 1, -1], [ 1,  1],		#	┣━━━╋━━━╋━━━┫
]							#	┃   ┃ ♝ ┃   ┃
							#	┣━━━╋━━━╋━━━┫
							#	┃ ✕ ┃   ┃ ✕ ┃	[-1, -1], [-1,  1]
							#	┗━━━┻━━━┻━━━┛

knight_offsets = [			#	┏━━━┳━━━┳━━━┳━━━┳━━━┓
	[-2, -1], [-2,  1],		#	┃   ┃ ✕ ┃   ┃ ✕ ┃   ┃	[ 2, -1], [ 2,  1]
	[-1, -2], [-1,  2],		#	┣━━━╋━━━╋━━━╋━━━╋━━━┫
	[ 1, -2], [ 1,  2],		#	┃ ✕ ┃   ┃   ┃   ┃ ✕ ┃	[ 1, -2], [ 1,  2]
	[ 2, -1], [ 2,  1],		#	┣━━━╋━━━╋━━━╋━━━╋━━━┫
]							#	┃   ┃   ┃ ♞ ┃   ┃   ┃
							#	┣━━━╋━━━╋━━━╋━━━╋━━━┫
							#	┃ ✕ ┃   ┃   ┃   ┃ ✕ ┃	[-1, -2], [-1,  2]
							#	┣━━━╋━━━╋━━━╋━━━╋━━━┫
							#	┃   ┃ ✕ ┃   ┃ ✕ ┃   ┃	[-2, -1], [-2,  1]
							#	┗━━━┻━━━┻━━━┻━━━┻━━━┛

class Piece:

	def __init__(self, colour, board, pos):
		self.colour	= colour
		self.board  = board
		self.pos	= pos
		self.moved	= 0

	def __repr__(self):
		return (self.FIG[0] if self.colour==WHITE
		  else  self.FIG[1])

	def clone(self, board):
		return type(self)(self.colour, board, self.pos[:])
								# clone a piece of the same type
								# same colour and position
								# this is for Board.clone()

	def crawl(self, offsets):
		moves = []
		for row, col in offsets:
			increment = (self.pos[0]+row, self.pos[1]+col)

			while self.board.get(increment) is None:
				moves.append(Move(self, destination=increment))
				increment = (increment[0]+row, increment[1]+col)

			moves.append(Move(self, destination=increment))

		return moves

	def get_legal_moves(self):
		# all moves that are legal
		return [ move for move in self.get_moves()
				if move.is_legal() ]





class King(Piece):

	NAME	= 'king'
	NOTE	= 'K'
	FIG		= '♔♚'

	def get_moves(self):
		all_moves = [Move(self, offset=offset)
				for offset in cardinal_offsets
				             +diagonal_offsets]

		# CASTLING!!!
		# if not self.moved
		# all_moves.append
		return all_moves

class Pawn(Piece):

	NAME	= 'pawn'
	NOTE	= ''
	FIG		= '♙♟'
	VALUE	= 1

	def get_moves(self):
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
		if self.board.get(advance) is None:
			all_moves.append(Move(self, destination=advance))

			advance_two = (self.pos[0] + offset*2, self.pos[1])
			if not self.moved and self.board.get(advance_two) is None:
				all_moves.append(Move(self, destination=advance_two))
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
			_piece = self.board.get(capture)
			if _piece and _piece.colour!=self.colour:
				all_moves.append(Move(self, destination=capture))
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

	def get_moves(self):
		return [Move(self, offset=offset)
					for offset in knight_offsets]


class Bishop(Piece):

	NAME	= 'bishop'
	NOTE	= 'B'
	FIG		= '♗♝'
	VALUE	= 3

	def get_moves(self):
		return self.crawl(diagonal_offsets)

class Rook(Piece):

	NAME	= 'rook'
	NOTE	= 'R'
	FIG		= '♖♜'
	VALUE	= 5

	def get_moves(self):
		return self.crawl(cardinal_offsets)

class Queen(Piece):

	NAME	= 'queen'
	NOTE	= 'Q'
	FIG		= '♕♛'
	VALUE	= 9

	def get_moves(self):
		return self.crawl(cardinal_offsets
						 +diagonal_offsets)


