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

		self.make_binds()
		self.load_sprites()
		self.make_board()

		self.selected = None
		self.chess = chess.Chess()
		self.update()

	def make_binds(self):
		self.bind('<Button-1>', self.select)

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

	def make_board(self):
		self.canvas = tkinter.Canvas(self,
				width=SIZE, height=SIZE,
				highlightthickness=0)
		self.canvas.pack()

	def update(self):
		self.render_board()
		self.render_pieces()

	def select(self, cursor):
		print('[command] select')
		self.update()

		row = (SIZE-cursor.y)*8 // SIZE
		col = cursor.x*8 // SIZE
		piece = self.chess.board.get((row, col))

		if piece and piece.colour=='white': 
			print(' <Piece>', piece, piece.pos)
			self.render_moves(piece.get_legal_moves())
			self.selected = piece
		elif self.selected and (row, col) in self.selected.get_legal_moves():
			print(' <Move>', self.selected, (row, col))
		else:
			self.selected = None


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
		for row in range(8):
			for col in range(8):
				piece = self.chess.board.tiles[row][col]
				if not piece: continue
				self.canvas.create_image((length*(col+0.5), SIZE-length*(row+0.5)+2),
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

