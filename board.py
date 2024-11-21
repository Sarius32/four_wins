from player import Player


class Board:
    def __init__(self):
        self._matrix = [[None for _ in range(7)] for _ in range(6)]  # [row][column]

    def show_state(self, locs=None):
        if locs is None:
            print("\n".join(["|" + "|".join([str(obj) if obj else " " for obj in row]) + "|" for row in self._matrix]))
        else:
            a = []
            for row in range(6):
                r = []
                for column in range(7):
                    if self._matrix[row][column]:
                        if (row, column) in locs:
                            r.append(self._matrix[row][column].hl())
                        else:
                            r.append(str(self._matrix[row][column]))
                    else:
                        r.append(" ")
                a.append("|" + "|".join(r) + "|")

            print("\n".join(a))

    def drop_stone(self, player: Player, column: int):
        if column < 1 or column > 7:
            return False, "Invalid column chosen!"

        column = column - 1  # corrected for 0-based indexing

        if self._matrix[0][column]:
            return False, "Selected column is already full."

        for row in self._matrix[::-1]:
            if row[column] is None:
                row[column] = player
                return True, None

    def _column_winner(self, column):
        if self._matrix[2][column] is None:  # no more than 4 stones in a column => no win possible
            return None, None

        for row in range(3):  # starting from the top, check the top 4 entries
            if self._matrix[row][column]:
                player = self._matrix[row][column]
                locs = [(row + r, column) for r in range(4)]
                stones = [self._matrix[r][c] for r, c in locs]
                if all([s == player for s in stones]):
                    return player, locs

        return None, None  # no winner for this column

    def _row_winner(self, row):
        if self._matrix[row][3] is None:  # no center stone => no more than 3 stones in a chain
            return None, None

        center = self._matrix[row][3]

        locs = [(row, 3)]

        same_stones = 1
        for left in range(3)[::-1]:
            if self._matrix[row][left] == center:
                same_stones += 1
                locs.insert(0, (row, left))
            else:
                break

            if same_stones == 4:
                return center, locs  # 4 stones in a chain including the center

        for right in range(4, 7):
            if self._matrix[row][right] == center:
                same_stones += 1
                locs.append((row, right))
            else:
                break

            if same_stones == 4:
                return center, locs  # 4 stones in a chain including the center

        return None, None

    def _diagonal_winner(self, row, column, direction):
        first = self._matrix[row][column]

        if direction == "right":
            locs = [(row + i, column + i) for i in range(4)]
        else:
            locs = [(row + i, column - i) for i in range(4)]

        stones = [self._matrix[r][c] for r, c in locs]
        if all([s == first for s in stones]):  # if all stones below left/right are the same
            return first, locs  # winner found

        return None, None

    def game_end(self):
        if all([all(row) for row in self._matrix]):
            return True, None, []  # game stops, board full

        for column in range(7):
            winner, locs = self._column_winner(column)
            if winner:
                return True, winner, locs  # game stops, winner found

        for row in range(6):
            winner, locs = self._row_winner(row)
            if winner:
                return True, winner, locs  # game stops, winner found

        for row in range(3):
            for column in range(4):
                winner, locs = self._diagonal_winner(row, column, "right")
                if winner:
                    return True, winner, locs  # game stops, winner found

            for column in range(3, 7):
                winner, locs = self._diagonal_winner(row, column, "left")
                if winner:
                    return True, winner, locs  # game stops, winner found

        return False, None, None  # game continues
