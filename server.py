"""
Implementation of the web mode of 2048 game.
Warning: this controller does not support concurrent session
"""

import uvicorn
import argparse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from game import game_init
from main import game_controller
from grid import Action

app = FastAPI()

templates = Jinja2Templates(directory="templates")

TEMPLATE_NAME = "ui.html"


@app.get("/NEW", response_class=HTMLResponse, include_in_schema=False)
def new_game(request: Request, row=4, col=4, init=2, depth=3):
    """Web controller to bootstrap a new game. Example: http://localhost:8000/NEW

    Args:
        request: the restful http GET request
        row: number of rows (default is 5)
        col: number of columns (default is 5)
        init: the random number selected to initialize the board
        depth: maximum depth of ai search

    Returns:
        http response including the new random board

    """
    app.state.grid, app.state.ai = game_init(int(row), int(col), int(init), int(depth))
    return templates.TemplateResponse(request, TEMPLATE_NAME, {"grid": app.state.grid})


@app.post("/{button}", response_class=HTMLResponse)
async def move(request: Request, button: str):
    """Web controller to move an existing game. Example: http://localhost:8000/[LEFT|UP|RIGHT|LEFT|AI]

    Args:
        request: the restful http GET request
        button: the identifier of button clicked in the web page

    Returns:
        http response including the next board state following user action

    """

    app.state.grid, app.state.message = game_controller(
        Action[button], app.state.grid, app.state.ai
    )
    return templates.TemplateResponse(
        request, TEMPLATE_NAME, {"grid": app.state.grid, "message": app.state.message}
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    # start web controller
    uvicorn.run(app, host=args.host, port=args.port)
