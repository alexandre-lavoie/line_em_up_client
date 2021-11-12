"""
The library to connect to the server.

You **MUST** copy this file over to your code directory and import the methods you need.

You **MUST NOT** modify the contents of this code (unless if you know what you are doing).
"""

import threading
from typing import Tuple, Union, List
from dataclasses import dataclass
import string

import socketio

SERVER_URL = "http://35.203.9.94/"

@dataclass
class Parameters:
    board_size: int
    line_up_size: int
    max_time: float
    blocks: List[Tuple[int, int]]

class SocketClient(threading.Thread):
    game_id: str
    player_name: str

    parameters: Parameters
    player_id: str
    player_tile: str

    sio: socketio.Client
    previous_move: Tuple[int, int]
    
    join_lock: threading.Lock
    play_lock: threading.Lock
    done: bool

    def __init__(self, player_name: str, game_id: str):
        threading.Thread.__init__(self)
        self.game_id = game_id
        self.player_name = player_name
        self.previous_move = None
        self.join_lock = threading.Lock()
        self.join_lock.acquire()
        self.play_lock = threading.Lock()
        self.play_lock.acquire()
        self.done = False

    def run(self):
        sio = socketio.Client()
        self.sio = sio

        @sio.event
        def connect():
            sio.emit("parameters", {"game_id": self.game_id})

        @sio.event
        def parameters(data):
            self.parameters = Parameters(
                board_size=data['board_size'],
                line_up_size=data['line_up_size'],
                max_time=data['max_time'],
                blocks=data['blocks'] if data['blocks'] else []
            )

            sio.emit("join", {"game_id": self.game_id, "player_name": self.player_name, "player_type": "ai"})

        @sio.event
        def join(data):
            if data["player_name"] == self.player_name:
                self.player_id = data["player_id"]
                self.player_tile = data["tile"]
                self.join_lock.release()

        @sio.event
        def play(data):
            if data["tile"] == self.player_tile:
                if len(data["moves"]) > 0:
                    x, y, tile = data["moves"][-1]
                    self.previous_move = (x, y)
                self.play_lock.release()

        @sio.event
        def win(data):
            self.done = True
            self.play_lock.release()
            sio.disconnect()

        @sio.event
        def error(data):
            self.done = True
            self.play_lock.release()
            sio.disconnect()
            raise Exception(data["error"])

        sio.connect(SERVER_URL)

SOCKET: SocketClient = None

def join(team_name: str, game_id: str):
    """
    Join a game using the game_id. This MUST be ran before everything else to establish the connection.
    This method will block until everyone joined the game.

    - team_name: Your team name to join with.
    - game_id: Can be found in the UI after creating a game.
    """

    global SOCKET

    SOCKET = SocketClient(
        game_id=game_id,
        player_name=team_name
    )
    SOCKET.start()
    SOCKET.join_lock.acquire()

def parameters() -> Parameters:
    """
    (Optional) Gets the game parameters (board_size, line_up_size, blocks, and max_time) from the server.
    This is for convenience if you don't want to have to manually write these values in your code.
    """

    global SOCKET

    if not SOCKET:
        raise Exception("Trying to get parameters without having joined. You need to use join(...) first.")

    if SOCKET.done:
        raise Exception("Game complete.")    
    
    return SOCKET.parameters

def receive() -> Union[Tuple[int, int], None]:
    """
    Receives the previous move that the other player played. This method will block until a move is received.
    This will return None if this is the first turn (aka there were no previous moves) else it will return the (x, y) coordinate.
    """

    global SOCKET

    if not SOCKET:
        raise Exception("Trying to play without having joined. You need to use join(...) first.")

    SOCKET.play_lock.acquire()

    if SOCKET.done:
        raise Exception("Game complete.")

    return SOCKET.previous_move

def send(coordinate: Union[Tuple[int, int], str]):
    """
    Send your move coordinate to the server. This can be in "A0", "A 0", "A,0", (0, 0), or ("A", 0) format.
    """

    global SOCKET

    if not SOCKET:
        raise Exception("Trying to play without having joined. You need to use join(...) first.")

    if SOCKET.done:
        raise Exception("Game complete.")

    if isinstance(coordinate, str):
        if "," in coordinate:
            x, y = coordinate.split(",")
        elif " " in coordinate:
            x, y = coordinate.split(" ")
        else:
            x, y = coordinate

        if x.isalpha():
            x = string.ascii_lowercase.index(x.lower())
        else:
            x = int(x)
        y = int(y)

        coordinate = (x, y)
    elif isinstance(coordinate, tuple) or isinstance(coordinate, list):
        x, y = coordinate

        if isinstance(x, str) and x.isalpha():
            x = string.ascii_lowercase.index(x.lower())
        else:
            x = int(x)
        y = int(y)

        coordinate = (x, y)

    SOCKET.sio.emit("play", {"move": coordinate})
