import tkinter
import palette
import chess

TITLE = 'chess | @mightbesimon'
SIZE  = 600

TILE_DARK  = palette.RED_DARK
TILE_LIGHT = palette.RED_LIGHT
MEAN  = palette.RED_MEAN


class Frame(tkinter.Tk):

	def __init__(self):
		super().__init__()

		self.title(TITLE)
		self.geometry(f'{SIZE}x{SIZE}')

		self.load_sprites()
		self.make_canvas()
		self.make_binds()

		self.selected = None
		self.chess = chess.Chess()
		self.chess.board.set_up()
		self.update()

	def make_binds(self):
		self.canvas.bind('<Button-1>', self.select_handler)

	def load_sprites(self, folder='sprites'):
		self.sprites = {
			'bishop' : None,
			'king'   : None,
			'knight' : None,
			'pawn'   : None,
			'queen'  : None,
			'rook'   : None,
		}

		for piece in self.sprites:
			self.sprites[piece] = (
				tkinter.PhotoImage(file=f'{folder}/light_{piece}_60.png'),
				tkinter.PhotoImage(file=f'{folder}/dark_{piece}_60.png'))

	def make_canvas(self):
		self.canvas = tkinter.Canvas(self,
				width=SIZE, height=SIZE,
				highlightthickness=0)
		self.canvas.pack()

	def update(self):
		self.canvas.delete('all')
		self.render_board()
		self.render_pieces()

	def select_handler(self, cursor):
		print('[command] SELECT')
		self.update()

		row = (SIZE-cursor.y)*8 // SIZE
		col = cursor.x*8 // SIZE
		piece = self.chess.board[row, col]

		if piece and piece.colour=='white': 
			print(' <Piece>', piece, piece.pos)
			self.piece_moves = piece.get_legal_moves()
			self.render_moves(self.piece_moves)
			self.selected = piece

		elif self.selected and (row, col) in self.piece_moves:
			print(' <Move>', self.selected, (row, col))
			move, *_ = [m for m in self.piece_moves if (row, col)==m]
			move.make()
			self.update()
			# make AI move
			self.AI_move()

		else:
			print('<De-select>')
			self.selected = None


	def AI_move(self):
		min_eval = 40
		best_moves = []
		
		all_legal_moves = self.chess.board.get_all_legal_moves('black')
		if not all_legal_moves:
			self.canvas.create_rectangle(290, 0, 310, 600)
			self.over = True
			return

		for move in all_legal_moves:
			board_copy = self.chess.board.clone()
			move_copy = move.clone(board_copy)
			move_copy.make()
			# evaluation = board_copy.evaluate()

			# anticipate player responce
			max_responce = -40
			responce_moves = board_copy.get_all_legal_moves('white')
			for responce in responce_moves:
				board_copy_responce = board_copy.clone()
				responce_copy = responce.clone(board_copy_responce)
				responce_copy.make()

				eval_responce = board_copy_responce.evaluate()
				if eval_responce > max_responce:
					max_responce = eval_responce
					evaluation = eval_responce

			# evaluate position
			if evaluation < min_eval:
				min_eval = evaluation
				best_moves = [move]
			elif evaluation==min_eval:
				best_moves.append(move)

		# print(min_eval, best_moves)

		best_move = best_moves[327 % len(best_moves)]
		best_move.make()
		print(best_move.piece, best_move)
		print('evaluation =', self.chess.board.evaluate())
		self.update()

	def recursive_search(self, depth):
		pass


	def render_board(self, tile_dark=TILE_DARK,
	                       tile_light=TILE_LIGHT):
		length = SIZE // 8		# length of tiles sides
		for row, col in [(r, c) for c in range(0, SIZE, length)
		                        for r in range(0, SIZE, length)]:
			# x0, y0 = (x, y)
			# point = (x+self.length, y+self.length)
			self.canvas.create_rectangle((row, col),
				(row+length, col+length),
				fill=MEAN if (row+col)/length%2 \
				else tile_light, width=6, outline=tile_dark) #outline= , width=6

	def render_pieces(self):
		length = SIZE // 8
		for piece in self.chess.board:
			row, col = piece.pos
			self.canvas.create_image(
				(length*(col+0.5), SIZE-length*(row+0.5)+2),
				image=self.sprites[piece.NAME][0 if piece.colour=='white' else 1])

	def render_moves(self, moves):
		length = SIZE // 8
		for move in moves:
			point0 = (length*(move.dst[1]+0.5-0.172), SIZE-length*(move.dst[0]+0.5+0.172))
			point1 = (length*(move.dst[1]+0.5+0.172), SIZE-length*(move.dst[0]+0.5-0.172))
			self.canvas.create_oval(point0, point1,
				fill='#363636', width=0)


if __name__ == '__main__':
	frame = Frame()
	frame.mainloop()

