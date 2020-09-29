from board import *

WHITE = 'white'
BLACK = 'black'


class Chess:

	def __init__(self):
		self.player = WHITE
		self.board  = Board()
		self.board.set_up()

	def loop_player(self):
		self.board.display()
		self.select_piece()
		self.board.display(self.piece)
		self.select_move().make()
		self.player = WHITE if self.player==BLACK else BLACK

	def loop_ai(self):
		if self.board.is_checkmate(self.player): return
		all_legal_moves = self.board.get_all_legal_moves(BLACK)
		move = all_legal_moves[327 % len(all_legal_moves)]
		move.make()
		self.player = WHITE

	def end(self):
		self.board.display()
		print(self.player, 'checkmate')

	def select_piece(self):
		while True:
			coord = input('select piece: ')
			pos = Board.decode_coord(coord)

			if not pos:
				print('[invalid coordinate] cannot decode')
				continue
			self.piece = self.board.get(pos)
			if self.piece is False:
				print('[invalid coordinate] out of bounds')
				continue
			if self.piece is None:
				print('[invalid square] no piece found')
				continue
			if self.piece.colour!=self.player:
				print('[invalid piece] wrong colour')
				continue
			self.legal_moves = self.piece.get_legal_moves()
			if not self.legal_moves:
				print('[invalid piece] no legal moves')
				continue

			return

	def select_move(self):
		while True:
			coord = input('select move: ')
			destination = Board.decode_coord(coord)
			if destination in self.legal_moves:
				_move, *_ = [move for move in self.legal_moves if destination==move]
				return _move
			touch = self.board.get(destination)
			if touch and touch.colour==self.player:
				self.piece = touch
				self.legal_moves = self.piece.get_legal_moves()
				if not self.legal_moves:
					print('[invalid piece] no legal moves')
				else:
					self.board.display(self.piece)


	def main():
		chess = Chess()

		while True:
			chess.loop_player()
			if chess.board.is_checkmate(chess.player): break
			chess.loop_ai()
			if chess.board.is_checkmate(chess.player): break

		chess.end()


if __name__ == '__main__': Chess.main()


