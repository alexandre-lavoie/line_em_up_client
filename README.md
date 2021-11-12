# Line Em' Up Client

Base client for the Line Em' Up tournament. This also includes extensive documentation of the server platform.

## Dependencies

You will need to install `SocketIO` and `Requests`. There are various way to install packages in Python, here are the common ones:

```
pip3 install python-socketio requests
```

or

```
pip3 install -r requirements.txt
```

## TODO

To take part of the tournament, you have to add abit of code on top of the assignment. 

You **MUST** copy the `client.py` to your repository. You should put the file at the same depth as your `main.py` (or equivalent). You should also be able to just copy paste the contents directly into your code (though it could lead to some issues).

You **MUST** include the following methods in your code. To make your life easier, an `example.py` can be found in this repo that you can base yourself off of or simply copy.

## Methods

The `client.py` library provies you the following methods:

- `join(team_name, game_id)`: Joins a game using the game_id with your team name. You will need to get an ID from the UI.
- `parameters()`: (Optional) Gets the game parameters. This can useful if you don't want to manually input board_size, line_up_size, etc.
- `receive()`: Receives the opponent's last move in `(x, y)` format from the server. **BE CAREFUL** this will be `None` on first turn (aka when no moves have been played yet).
- `send()`: Sends your coordinate move to the server. You can use a tuple in the `(x, y)` format or a string in the `"A0"` format.  

## Play

To play a round of Line Em' Up, follow this procedure:

1) Goto the server url: http://35.203.9.94/.
2) Visit the `New` game tab.
3) Enter the game details (Board Size, Line Up Size, Blocks, and Max Time) provided to you. (Note: The `Blocks` format follow `(0, 0), (0, 1), ...` or `A0, A1, ...` notation).
4) Press the `Start` button. This will redirect you to a view of the live game board.
5) Take note of the `Game ID` and provide the number to your opponent.
6) Go into your AI code and change the `game_id` variable in the `join` method.
7) Run your AI.
8) (Optional) Return to your browser to see the game in the tab.
9) Hopefully win :).

## Results

You can check the `Games` tab to see a list of all completed games. This will show which player won/tied/lost the game.

You can check the `Leaderboard` tab to see player scores and player ranking. Note final scoring may modified.

You can click on a game id link to view current/final state of the game. 

You can click a player id link to view the games they partcipated in and their rank/score.
