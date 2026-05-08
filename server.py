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

@app.get("/NEW", response_class=HTMLResponse, include_in_schema=False)
def new_game(request: Request, row=5, col=5, init=2, depth=5):

    app.state.grid, app.state.controllers, app.state.ai = game_init(int(row), int(col), int(init), int(depth))
    return templates.TemplateResponse(request, "grid.html", {"grid": app.state.grid})

@app.post("/{button}", response_class=HTMLResponse)
async def move(request: Request, button: str):
    app.state.grid, app.state.message = game_controller(Action[button], 
                                                        app.state.grid,
                                                        app.state.controllers, 
                                                        app.state.ai)
    return templates.TemplateResponse(request, "grid.html", {"grid": app.state.grid, "message" : app.state.message})    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    # start web controller
    uvicorn.run(app, host=args.host, port=args.port)