# 2048 Game

## Requirements:

Python version 3.12.*
pip

Install 2048 game:

clone the remote repository on your local machine:
git clone https://github.com/gmarlier/gm_2048.git

Optional: create a virtual environment and activate it

install python dependencies by running this command in the gm_2048 folder:
pip install -r requirements

## Game modes

The implementation provides 2 modes:

### command line mode:

run the following command: python3 main.py

help with launch options can be accessed with: python main.py --help

The game has 4 keyboard controllers:
- key "4": move the board to the left
- key "6": move the board to the right
- key "8": move the board to the top
- key "2":  move the board to the bottom
- center key "5": provide a best move suggestion

Possible message output in command line:
- you win !
- you lose !
- ai best move suggestion: up, left, down or right

### web mode:

run the following command: python3 server.py

help with launch options can be accessed with: python server.py --help
(for exemple, option to change default port is available)

a new game is launched in browser via: http://localhost:8000/NEW

The game has 4 ui controllers:
- left arrow button: move the board to the left
- right arrow button: move the board to the right
- up arrow button: move the board to the top
- down arrow button: move the board to the bottom
- center "AI" button: provide a best move suggestion

Some parameters can be specified in launch url
row:  number of rows in the new board (default is 5)
col:  number of columns in the new board (default is 5)
init: the number chosen to initialize a new board (default is 2)
depth:the number of analyze depth used by ai agent to generate the best move (default is 3)

Example: http://localhost:8000/NEW?row=4&col=4&init=2&depth=2

Expected message output in web mode:
- you win !
- you lose !
- ai best move suggestion: up, left, down or right

## Limit: 
- the server (web moce) does not manage multiple concurrent game sessions
- depth * size should be limited to 5 * 5 * 5 to avoid excessive computation


