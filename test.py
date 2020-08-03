from board import *
from piece import *


# board = Board()
# board.set_up()
# board.make_move(board.tiles[0][1], [2, 2])
# board.make_move(board.tiles[1][3], [2, 3])
# board.display(board.tiles[2][3])

def set_up_6x6(board):
	board.tiles[0] = [
		Rook  (WHITE, board, (0, 0)),
		Knight(WHITE, board, (0, 1)),
		Queen (WHITE, board, (0, 2)),
		King  (WHITE, board, (0, 3)),
		Knight(WHITE, board, (0, 4)),
		Rook  (WHITE, board, (0, 5)),
	]
	board.tiles[1] = [
		Pawn(WHITE, board, (1, col))
		for col in range(6)
	]

	board.tiles[board.DIMENSIONS[0]-2] = [
		Pawn(BLACK, board, (4, col))
		for col in range(6)
	]
	board.tiles[board.DIMENSIONS[0]-1] = [
		Rook  (BLACK, board, (5, 0)),
		Knight(BLACK, board, (5, 1)),
		Queen (BLACK, board, (5, 2)),
		King  (BLACK, board, (5, 3)),
		Knight(BLACK, board, (5, 4)),
		Rook  (BLACK, board, (5, 5)),
	]

board = Board(8, 6)
set_up_6x6(board)
board.display()

# board = Board(16, 8)
# board.set_up()
# board.display()

print(board.iterate())

piece = board.get((0, 0))
print('piece', piece, piece.pos)
copy = piece.clone()
copy.pos = (4, 4)
print('piece', piece, piece.pos)
print('clone', copy, copy.pos)

copy = board.clone()
copy.make_move(copy.tiles[0][1], (2, 2))
board.display()
copy.display()
print(board)
print(copy)



