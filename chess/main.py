import chess

from constant.constants import EXIT, MAX_DEPTH
from engine.GameEngine import GameEngine

if __name__ == "__main__":
    ALGORITHM_TO_CHECK = input("Please choose algorithm: \n1. NegaMax\n2.NegaScout3.\n3.PVS\n")
    ALGORITHM_TO_CHECK = int(ALGORITHM_TO_CHECK)
    if ALGORITHM_TO_CHECK not in [1, 2, 3]:
        raise Exception("Wrong input! Value must be in rage [1-3].")

    board = chess.Board()
    whitesTurn = True
    engine = GameEngine(ALGORITHM_TO_CHECK)

    while board.is_checkmate() == False \
            and board.is_variant_draw() == False:
        if whitesTurn:
            user_input = str(input(f"Please, enter your move [\"{EXIT}\" - to finish]: "))
            print(user_input)
            if user_input == EXIT:
                break
            try:
                move = chess.Move.from_uci(user_input)
            except:
                print(f"{user_input} is invalid move, try again.")
                continue
            print(f"Whites move {move}")
            whitesTurn = False
        else:
            score, move = engine.predict(board, MAX_DEPTH)
            print(f"Blacks moves {move}")
            whitesTurn = True
        board.push(move)
        print(board)
        print("--------")
