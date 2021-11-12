"""
This an example client using the basic `client.py` library provided in this repo.

NOTE: If you are using this file as base for your AI implementation, you **MUST** copy over the `client.py` file to your code.

The code is HEAVILY commented in hopes to be as clear as possible.
To differentiate between type of commands, I use the following formats:

- (TODO): Indicates that you **MUST** implement the code in your AI.
- (Optional): Indicates a feature that the server offers that could be interesting for your but not essential.
- (Example): Indicates code for this example (which will probably be implemented totally differently on your end).
"""

# (TODO) Import these methods in your code. You **MUST** copy over the `client.py` to your code folder.
from client import join, send, receive, parameters

# (TODO) **MUST** have a team_name variable to join a game.
TEAM_NAME = "Test"
# (TODO) **MUST** get GAME_ID from UI when a game is generated.
GAME_ID = 1

def main():
    print("Join")

    # (TODO) Join game using GAME_ID. This **MUST** be done before any other client method. 
    # The GAME_ID can be found in the UI when a game is created.
    join(
        team_name=TEAM_NAME,
        game_id=GAME_ID
    )

    # (Optional) Get the game parameters (board_size, line_up_size, blocks, and max_time) for the current game from server.
    p = parameters()
    print(p)

    # (Example) Generate an empty board and add the blocks taken from the parameters.
    board = [[None for _ in range(p.board_size)] for _ in range(p.board_size)]
    for block_x, block_y in p.blocks:
        board[block_y][block_x] = "B"

    # Game loop.
    while True:
        # (TODO) Receive the (x, y) coordinate for the opponent's previous move.
        # NOTE: Will return None if this is the first turn and you are the first player (aka there were no previous moves).
        # NOTE: This method will throw an exception when the game is over, this prevents you from having to check.
        opponent_move = receive()
        print("Opponent plays", opponent_move)

        # (Example) Set the opponent's move on board.
        # NOTE: We **MUST** check if there was a move (if you are first player on first turn there won't be any). 
        if not opponent_move == None:
            opponent_x, opponent_y = opponent_move
            board[opponent_y][opponent_x] = "O"

        # (Example) Select the next available spot to play.
        # NOTE: This is where you should plug in your AI to get the next move. 
        next_move = None
        for y, row in enumerate(board):
            for x, tile in enumerate(row):
                if tile == None:
                    next_move = (x, y)
                    break
            if next_move:
                break
        print("I play", next_move)

        # (Example) Set your move on board.
        board[next_move[1]][next_move[0]] = "P"

        # (Example) Print a very basic view of the board.
        for row in board:
            print(''.join(c if c else "_" for c in row))

        # (TODO) Send your coordinates to the server. 
        # NOTE: This method accept (x, y) or "A0" format coordinates.  
        send(next_move)

if __name__ == "__main__":
    main()
