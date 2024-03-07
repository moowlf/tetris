from random import choice
from .pieces import IPiece, JPiece, LPiece, SquarePiece, SPiece, TPiece, ZPiece
from .movement import Movement


class TetrisPiece:
    def __init__(self) -> None:
        self.tetramino = choice(
            [IPiece, JPiece, LPiece, SquarePiece, SPiece, TPiece, ZPiece]
        ).data
        self.position = [0, 7]


class Game:
    def __init__(self, width, height) -> None:
        self.screen = [
            [0] * width for _ in range(height)
        ]  # x is horizontal and first coordinate
        self.piece = TetrisPiece()
        self.frame = 0

    def next_state(self):
        self.frame += 1
        # Update screen
        if self._would_collide(Movement.DOWN) and self.frame % 30 == 0:
            self.draw(self.screen)
            self._clean_board()
            self.piece = TetrisPiece()
            return self.screen

        screen = [x.copy() for x in self.screen]

        if self.frame % 30 == 0:
            self.move_piece(Movement.DOWN)

        self.draw(screen)
        return screen

    def _would_collide(self, mov):

        if mov == Movement.DOWN:
            delta_pos =  (1,0)
        elif mov == Movement.LEFT:
            delta_pos = (0,-1)
        elif mov == Movement.RIGHT:
            delta_pos = (0, 1)
        else:
            raise Exception("Rotate is not considered here")


        for point in self.piece.tetramino:
            x, y = point

            # row, column
            new_position = y + self.piece.position[0] + delta_pos[0], x + self.piece.position[1] + delta_pos[1]

            # Went outside the screen
            if new_position[0] >= len(self.screen):
                return True

            if new_position[1] >= len(self.screen[0]) or new_position[1] < 0:
                return True

            if self.screen[new_position[0]][new_position[1]] == 1:
                return True

        return False

    def _clean_board(self):
        rows_to_delete_beg = 10**9
        rows_to_delete_end = -1

        for i, row in enumerate(self.screen):
            cnts = row.count(1)
            if cnts == len(row) and cnts != 0:
                rows_to_delete_beg = min(rows_to_delete_beg, i)
                rows_to_delete_end = max(rows_to_delete_end, i)

        if rows_to_delete_beg == 10**9 and rows_to_delete_end == -1:
            return  # Nothing to do

        amount_deleted_lines = rows_to_delete_end - rows_to_delete_beg + 1
        for r in range(rows_to_delete_end, -1, -1):
            for c in range(len(self.screen[0])):
                self.screen[r][c] = (
                    self.screen[r - amount_deleted_lines][c]
                    if r - amount_deleted_lines >= 0
                    else 0
                )

    def move_piece(self, mov: Movement):
        y, x = self.piece.position

        if mov == Movement.LEFT and not self._would_collide(mov):
            self.piece.position[1] -= 1
        elif mov == Movement.RIGHT and not self._would_collide(mov):
            self.piece.position[1] += 1
        elif mov == Movement.DOWN and not self._would_collide(mov):
            self.piece.position[0] += 1
        elif mov == Movement.ROTATE:
            new_coords = []

            for w, h in self.piece.tetramino:
                new_coords.append((h, -w))

            for pos in new_coords:
                if 0 <= x + pos[0] < len(self.screen[0]) and 0 <= y + pos[1] <= len(
                    self.screen
                ):
                    continue
                else:
                    return False

            self.piece.tetramino = new_coords

    def draw(self, board):
        y_pos, x_pos = self.piece.position

        for w, h in self.piece.tetramino:
            board[y_pos + h][x_pos + w] = 1
