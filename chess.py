from board import *
from piece import *

WHITE = 'white'
BLACK = 'black'


def main():
	player = WHITE
	board  = Board()
	board.set_up()

	while not board.is_checkmate(player):

		board.display()

		while True:
			coord = input('select piece: ')
			pos = board.decode_coord(coord)

			if not pos:
				print('[invalid coordinate] cannot decode')
				continue
			if not board.check_bounds(pos):
				print('[invalid coordinate] out of bounds')
				continue
			piece = board.get(pos)
			if not piece:
				print('[invalid square] no piece found')
				continue
			if piece.colour!=player:
				print('[invalid piece] wrong colour')
				continue
			legal_moves = piece.get_legal_moves(board)
			if not legal_moves:
				print('[invalid piece] no legal moves')
				continue

			break

		board.display(piece)

		while True:
			coord = input('select move: ')
			destination = board.decode_coord(coord)
			if destination in legal_moves: break

		board.make_move(piece, destination)
		player = WHITE if player==BLACK else BLACK



		#==== black AI ====#
		if board.is_checkmate(player): break
		# flag1 = False
		# for row in range(board.DIMENSIONS[0]):
		# 	for col in range(board.DIMENSIONS[1]):
		# 		piece = board.tiles[row][col]
		# 		if piece and piece.colour==BLACK:
		# 			legal_moves = piece.get_legal_moves(board)
		# 			if not legal_moves: continue
		# 			board.make_move(piece, legal_moves[0])
		# 			flag1 = True
		# 			break
		# 	if flag1: break
		all_legal_moves = board.get_all_legal_moves(BLACK)
		piece, move = all_legal_moves[327 % len(all_legal_moves)]
		board.make_move(piece, move)
		player = WHITE

	board.display()
	print(player, 'checkmate')



if __name__ == '__main__': main()


