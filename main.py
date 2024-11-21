import os

from board import Board
from player import Player


def get_input(player: Player):
    inp = input(f"{player.name}, please enter which row to enter our stone: ")
    return inp.isnumeric(), inp


def main():
    player1 = Player("Player 1", "x", "red")
    player2 = Player("Player 2", "o", "green")

    board = Board()

    active_player = player1
    while True:
        board.show_state()

        is_num, num = get_input(active_player)
        if not is_num:
            print("Previous Input invalid!")
            continue

        column = int(num)
        stone_dropped, err = board.drop_stone(active_player, column)
        if not stone_dropped:
            print(err)
            continue

        end, winner, locs = board.game_end()
        if end:
            break

        active_player = player2 if active_player == player1 else player1


    board.show_state(locs)
    if winner:
        print(f"The winner is {winner}!")
    else:
        print("The game finished without a winner!")


if __name__ == '__main__':
    main()
