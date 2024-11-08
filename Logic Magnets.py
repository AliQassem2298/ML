import random
from collections import deque
import time
class MagneticPuzzleBoard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [['.' for _ in range(cols)] for _ in range(rows)]
        self.targets = []
        self.pieces = []  # قائمة لتخزين القطع كـ tuples (type, (row, col))
        self.visited_states = set()  # مجموعة لتخزين الحالات المٌزارة

    def is_within_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_empty_or_target(self, row, col):
        return self.board[row][col] in ['.', 'T']

    def place_piece(self, row, col, piece_type):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.board[row][col] = piece_type
            self.pieces.append((piece_type, (row, col)))  # إضافة القطعة إلى قائمة القطع
        else:
            print(f"Position ({row}, {col}) is out of bounds.")

    def place_target(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.board[row][col] = 'T'
            self.targets.append((row, col))  # إضافة الهدف إلى قائمة الأهداف
        else:
            print(f"Target position ({row}, {col}) is out of bounds.")

    def display(self):
        for row in range(self.rows):
            display_row = []
            for col in range(self.cols):
                if self.board[row][col] in ['R', 'P', 'H'] and (row, col) in self.targets:
                    display_row.append(self.board[row][col] + 'T')
                else:
                    display_row.append(self.board[row][col])
            print(" ".join(display_row))
        print()


    def can_move(self, row, col, direction):
        new_row, new_col = row, col
        if direction == "up" and row > 0:
            new_row -= 1
        elif direction == "down" and row < self.rows - 1:
            new_row += 1
        elif direction == "left" and col > 0:
            new_col -= 1
        elif direction == "right" and col < self.cols - 1:
            new_col += 1
        else:
            return False

        return self.board[new_row][new_col] in ['.', 'T'] or (self.board[new_row][new_col] == 'H' and self.board[row][col] == 'R')

    def move_piece(self, row, col, direction):
        piece = self.board[row][col]
        if piece not in ['P', 'R']:  # تأكد من أن القطعة التي يتم تحريكها هي مغناطيس فقط
            return False
        
        if self.can_move(row, col, direction):
            # انسخ الحالة الحالية
            new_board = self.clone_board()
            new_row, new_col = row, col
            if direction == "up":
                new_row -= 1
            elif direction == "down":
                new_row += 1
            elif direction == "left":
                new_col -= 1
            elif direction == "right":
                new_col += 1

            # تحديث اللوحة
            new_board.board[row][col] = '.'
            new_board.board[new_row][new_col] = piece
            new_board.pieces.remove((piece, (row, col)))
            new_board.pieces.append((piece, (new_row, new_col)))

            # تطبيق القوة المغناطيسية بعد حركة المغناطيس
            if piece == 'P':
                new_board.apply_repulsion(new_row, new_col)
            elif piece == 'R':
                new_board.apply_attraction(new_row, new_col)

            return new_board
        return False

    def clone_board(self):
        new_board = MagneticPuzzleBoard(self.rows, self.cols)
        new_board.board = [row[:] for row in self.board]  # نسخ اللوحة
        new_board.pieces = self.pieces[:]  # نسخ قائمة القطع
        new_board.targets = self.targets[:]  # نسخ الأهداف
        return new_board

    def apply_repulsion(self, row, col):
        for r in range(self.rows):
            if r != row and self.board[r][col] in ['H', 'P', 'R']:
                self.repulse_piece(r, col, "up" if r < row else "down")

        for c in range(self.cols):
            if c != col and self.board[row][c] in ['H', 'P', 'R']:
                self.repulse_piece(row, c, "left" if c < col else "right")

    def apply_attraction(self, row, col):
        for r in range(self.rows):
            if r != row and self.board[r][col] in ['H', 'P', 'R']:
                self.attract_piece_toward(r, col, "down" if r < row else "up")

        for c in range(self.cols):
            if c != col and self.board[row][c] in ['H', 'P', 'R']:
                self.attract_piece_toward(row, c, "right" if c < col else "left")

    def repulse_piece(self, r, c, direction):
        if direction == "up" and r > 0:
            self.board[r - 1][c] = self.board[r][c]
            self.board[r][c] = '.'
        elif direction == "down" and r < self.rows - 1:
            self.board[r + 1][c] = self.board[r][c]
            self.board[r][c] = '.'
        elif direction == "left" and c > 0:
            self.board[r][c - 1] = self.board[r][c]
            self.board[r][c] = '.'
        elif direction == "right" and c < self.cols - 1:
            self.board[r][c + 1] = self.board[r][c]
            self.board[r][c] = '.'

    def attract_piece_toward(self, row, col, direction):
        if direction == "up" and row > 0:
            if self.board[row - 1][col] == '.':
                self.board[row - 1][col] = self.board[row][col]
                self.board[row][col] = '.'
        elif direction == "down" and row < self.rows - 1:
            if self.board[row + 1][col] == '.':
                self.board[row + 1][col] = self.board[row][col]
                self.board[row][col] = '.'
        elif direction == "left" and col > 0:
            if self.board[row][col - 1] == '.':
                self.board[row][col - 1] = self.board[row][col]
                self.board[row][col] = '.'
        elif direction == "right" and col < self.cols - 1:
            if self.board[row][col + 1] == '.':
                self.board[row][col + 1] = self.board[row][col]
                self.board[row][col] = '.'

    def random_fill_board(self, red_count, purple_count, barrier_count):
        while red_count > 0 or purple_count > 0 or barrier_count > 0:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            if self.board[row][col] == '.':
                if red_count > 0:
                    self.place_piece(row, col, 'R')
                    red_count -= 1
                elif purple_count > 0:
                    self.place_piece(row, col, 'P')
                    purple_count -= 1
                elif barrier_count > 0:
                    self.place_piece(row, col, 'B')
                    barrier_count -= 1

    def move_magnet_to_position(self, row, col, new_row, new_col):
        if self.is_within_bounds(new_row, new_col) and self.is_empty_or_target(new_row, new_col):
            magnet = self.board[row][col]
            self.board[row][col] = "."  
            self.board[new_row][new_col] = magnet  
            
            self.pieces.remove((magnet, (row, col)))  # إزالة القطعة من مكانها السابق
            self.pieces.append((magnet, (new_row, new_col)))  # إضافة القطعة في مكانها الجديد

            if magnet == "P":
                self.apply_repulsion(new_row, new_col)
            elif magnet == "R":
                self.apply_attraction(new_row, new_col)
        else:
            print(f"Invalid move. Target ({new_row}, {new_col}) is not an empty or target square.")

    def check_win(self):
        for target in self.targets:
            row, col = target
            if self.board[row][col] == 'T':  # هدف فارغ
                return False
        return True


    def state_as_tuple(self):
        # إنشاء الحالة كـ tuple مكون من النوع والموقع لكل قطعة
        return tuple(sorted([(piece_type, (row, col)) for piece_type, (row, col) in self.pieces]))


def bfs(start_board):
    visited_states = set()
    queue = deque([start_board])

    while queue:
        current_state = queue.popleft()

        if current_state.state_as_tuple() in visited_states:
            continue

        visited_states.add(current_state.state_as_tuple())
        
        print("Current state:")
        current_state.display()
        print(f"Visited states count: {len(visited_states)}")
        
        # تحقق من الفوز
        if current_state.check_win():
            print("You Win!")
            return current_state

        for move in generate_possible_moves(current_state):
            new_state = current_state.move_piece(*move)

            if new_state and new_state.state_as_tuple() not in visited_states:
                queue.append(new_state)

       
                
    print("No solution found!")
    return None

    
def generate_possible_moves(current_state):
    moves = []
    for piece, (row, col) in current_state.pieces:
        if piece in ['P', 'R']: 
            directions = ["up", "down", "left", "right"]
            for direction in directions:
                if current_state.can_move(row, col, direction):
                    moves.append((row, col, direction))
    return moves



board = MagneticPuzzleBoard(3,4)
board.place_target(1, 3)
board.place_target(1, 1)
board.place_piece(1, 2, 'H')
board.place_piece(2, 0, 'P')


start_time = time. time()
solution = bfs(board)

end_time = time. time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")




# ### the first level from the game hahahah
# board = MagneticPuzzleBoard(1,4)
# board.place_target(0, 3)
# board.place_target(0, 1)
# board.place_piece(0, 2, 'H')
# board.place_piece(0, 0, 'P')

# start_time = time. time()
# solution = bfs(board)

# end_time = time. time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")


##############################################

## test the attraction & repulsion over the B
# board = MagneticPuzzleBoard(5, 5)
# board.place_piece(0, 3, 'P')    
# board.place_piece(0, 2, 'H')
# board.place_piece(1, 2, 'H')
# board.place_piece(1, 1, 'H')
# board.place_piece(2, 3, 'B')
# board.place_piece(4, 2, 'R')
# board.place_target(0, 0)

# board.place_target(4, 4)
# board.place_target(4, 0)

# board.place_target(1, 1)
# print('initial board:')
# board.display()
# board.move_piece(4, 2, "right")
# print('moving the R to the right:')
# board.display()
# board.move_piece(1, 3, "right")
# print('moving the P to the right:')
# board.display()

# start_time = time. time()
# solution = bfs(board)

# end_time = time. time()
# execution_time = end_time - start_time
# print(f"Execution time: {execution_time} seconds")

##############################################

### testing if the move_magnet_to_position is running...
# board = MagneticPuzzleBoard(5,5)
# board.place_piece(0, 3, 'P')    
# board.place_piece(0, 2, 'H')
# board.place_piece(1, 2, 'H')
# board.place_piece(1, 1, 'H')
# board.place_piece(2, 3, 'B')
# board.place_piece(4, 2, 'R')
# board.display()
# board.move_piece(4, 2, "right")
# board.display()
# board.move_magnet_to_position(4, 3, 0, 0)
# board.display()

##############################################


##############################################

##testing the H over the T
### don't try this at home 🙂.
### not working but there is no time to modify the code.
# board = MagneticPuzzleBoard(5,5)
# board.place_target(0, 0)
# board.place_target(1, 0)
# board.place_piece(2, 0, 'H')
# board.place_piece(0, 1, 'R')
# board.display()
# board.move_piece(0, 1, "left")
# board.display()