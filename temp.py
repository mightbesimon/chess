print('''
    a   b   c   d   e   f   g   h
  ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
8 ┃ ♜ ┃ ♞ ┃ ♝ ┃ ♛ ┃ ♚ ┃ ♝ ┃ ♞ ┃ ♜ ┃ 8
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
7 ┃ ♟ ┃ ♟ ┃ ♟ ┃>♟<┃ ♟ ┃>♟<┃ ♟ ┃ ♟ ┃ 7
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
6 ┃   ┃   ┃ ✕ ┃   ┃   ┃   ┃ ✕ ┃   ┃ 6
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
5 ┃   ┃   ┃   ┃   ┃ ♘ ┃   ┃   ┃   ┃ 5
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
4 ┃   ┃   ┃ ✕ ┃   ┃   ┃   ┃ ✕ ┃   ┃ 4
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
3 ┃   ┃   ┃   ┃ ✕ ┃   ┃ ✕ ┃   ┃   ┃ 3
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
2 ┃ ♙ ┃ ♙ ┃ ♙ ┃ ♙ ┃ ♙ ┃ ♙ ┃ ♙ ┃ ♙ ┃ 2
  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
1 ┃ ♖ ┃ ♘ ┃ ♗ ┃ ♕ ┃ ♔ ┃ ♗ ┃ ♘ ┃ ♖ ┃ 1
  ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
    a   b   c   d   e   f   g   h
''')

print('    a   b   c   d   e   f   g   h'  )
print('  ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓')
board=[None]*8; i = 7
board[i] = ['♟']*8
print(' ┃ '.join([str(i+1)]+board[i]+[str(i+1)]))
print('  ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫')
print(i+1, '┃', ' ┃ '.join(board[i]), '┃', i+1)
print('  ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛')