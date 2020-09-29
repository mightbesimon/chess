from piece import *


class Move:

	def __init__(self, piece, destination=None, offset=None,
					en_passant=False, castling=False, promotion=None):
		self.board = piece.board
		self.piece = piece
		self.src   = piece.pos #origin
		self.dst   = (destination if destination else
						(self.src[0]+offset[0],
						 self.src[1]+offset[1]))

		# if en_passant: self.make = self.en_passant
		# if castling  : self.make = self.castling
		# if promotion : self.make = self.promotion

	def __repr__(self):
		return self.piece.NOTE+chr(97+self.dst[1])+str(self.dst[0]+1)

	def __eq__(self, comp):
		return self.dst==comp

	# def destination(dst):
	# 	self.dst = dst
	# 	return self

	# def offset(offset):
	# 	self.dst = (self.src[0]+offset[0],
	# 	            self.src[1]+offset[1])
	# 	return self

	def clone(self, board=None):
		if not board: board = self.board
		return Move(board[self.src], destination=self.dst)

	def is_legal(self):
		'''	legal conditions:
			 - within bounds
			 - not land on same colour
			 - will not be under check
		'''
		if self.board.check_bounds(self.dst):
			_piece = self.board[self.dst]
			if not _piece or _piece.colour!=self.piece.colour:
				copy = self.board.clone()
				self.clone(copy).make()
				if not copy.is_check(self.piece.colour): return True

		return False

	def make(self):
		captured = self.board[self.dst]
		# if captured: self.board.captured[captured.colour].append(captured)

		self.board[self.src] = None
		self.board[self.dst] = self.piece
		self.piece.pos = self.dst
		self.piece.moved += 1    # moved times += 1

	def castling(self):
		pass

	def en_passant(self):
		return self

	def promotion(self):
		pass

	def notation(self):
		pass
		# return f'{piece.NOTE}{'x' if self.get(destination) else ''}{destination[1]}{destination[0]+1}'
		# chr(97+pos[1])+str(pos[0]+1)

