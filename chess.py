'''
'''

from board import *


class Chess:

	# PLAYERS		= 2
	# DIMENSIONS	= (8, 8)

	def __init__(self):
		self.board = Board()
		# self.captured = {}
		# for _ in [WHITE, BLACK]:
		# 	self.captured[_] = []

	def set_up(self):
		self.board.set_up()

	def is_checkmate(self, colour):
		''' checkmate conditions:
			 - is currently in check
			 - no legal moves
		'''
		return self.board.is_check(colour)\
		   and not self.board.get_all_legal_moves(colour)

	def is_stalemate(self, colour):
		'''	stalemate conditions:
			 - is not currently under check
			 - no legal moves
		'''
		return not self.board.is_check(colour)\
		   and not self.board.get_all_legal_moves(colour)	
