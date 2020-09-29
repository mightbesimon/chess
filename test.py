from board import Board


class Test:

	passed   = 0
	senarios = 0
	errors   = []

	def verify(self, actual, expected, code):
		self.senarios += 1
		if actual==expected:
			self.passed += 1
		else:
			self.errors.append(f'{code}: actual={actual} | expected={expected}')
			print(actual, expected, actual==expected, '♕'=='♕')

	def log(self, feature='untitled'):
		f = f'Feature {feature}'
		fill = " "*(20-len(f))
		print(f'{f}{fill}{self.passed}/{self.senarios} Senarios passed')
		for idx, error in enumerate(self.errors):
			print(f'{idx+1}) {error}')
		self.passed = 0
		self.senarios = 0
		self.errors.clear()


class TestBoard(Test):

	def test_init(self):
		# When
		board1 = Board()
		board2 = Board(12, 8)
		# Then
		self.verify(
			actual=board1.dim,
			expected=(8, 8),
			code='board1.dim'
		)
		self.verify(
			actual=board2.dim,
			expected=(12, 8),
			code='board2.dim'
		)
		self.log('__init__')
		return board1, board2

	def test_set_up(self):
		# Given
		board1, board2 = self.test_init()
		# When
		board1.set_up()
		board2.set_up()
		# Then
		self.verify(
			actual=board1._repr_small(),
			expected='♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜\n'
			         '♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙\n'
			         '♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖',
			code='board1._tiles'
		)
		self.verify(
			actual=board2._repr_small(),
			expected='♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜\n'
			         '♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '. . . . . . . .\n'
			         '♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙\n'
			         '♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖',
			code='board2._tiles'
		)
		# print(eval('board2._tiles'))
		self.log('set_up')
		return board1, board2

	def test_board11(self):
		# Given
		board1, board2 = self.test_set_up()
		# Then
		self.verify(
			actual=str(board1[0, 3]),
			expected='♕',
			code='board1[0, 3]'
		)
		self.verify(
			actual=str(board1[0, 3]),
			expected='♕',
			code='board2[0, 3]'
		)
		self.log('board[0, 3]')
		return board1, board2

	def test_board_pos(self):
		# Given
		board1, board2 = self.test_board11()
		# When
		pos = (0, 4)
		# Then
		self.verify(
			actual=str(board1[pos]),
			expected='♔',
			code='board1[pos]'
		)
		self.verify(
			actual=str(board1[pos]),
			expected='♔',
			code='board2[pos]'
		)
		self.log('board[pos]')
		return board1, board2

	run_tests = test_board_pos


TestBoard().run_tests()


