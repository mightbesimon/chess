from board import *
from piece import *


class Move:

	def __init__(self, piece, destination=False, offset=False,
					en_passant=False, castling=False, promotion=None):
		self.board = piece.board
		self.piece = piece
		self.src   = piece.pos #origin
		self.dst   = (destination if destination else
						(self.src[0]+offset[0],
						 self.src[1]+offset[1]))

		if en_passant: self.make = self.en_passant
		if castling  : self.make = self.castling
		if promotion : self.make = self.promotion

	def __repr__(self):
		return self.piece.NOTE+chr(97+self.dst[1])+str(self.dst[0]+1)

	def __eq__(self, comp):
		return self.dst==comp

	def is_legal(self):
		'''	legal conditions:
			 - within bounds
			 - not land on same colour
			 - will not be under check
		'''
		if self.board.check_bounds(self.dst):
			_piece = self.board.get(self.dst)
			if not _piece or _piece.colour!=self.piece.colour:
				copy = self.board.clone()
				Move(copy.get(self.src), destination=self.dst).make() ###
				if not copy.is_check(self.piece.colour): return True

		return False

	def make(self):
		captured = self.board.get(self.dst)
		if captured: self.board.captured[captured.colour].append(captured)

		self.board.set(self.src, None)
		self.board.set(self.dst, self.piece)
		self.piece.pos = self.dst
		self.piece.moved += 1

	def castling(self):
		pass

	def en_passant(self):
		pass

	def promotion(self):
		pass

	def notation(self):
		pass
		# return f'{piece.NOTE}{'x' if self.get(destination) else ''}{destination[1]}{destination[0]+1}'
		# chr(97+pos[1])+str(pos[0]+1)

