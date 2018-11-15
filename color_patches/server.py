"""
handles the definition of the canvas parameters and
the drawing of the model representation on the canvas
"""
# import webbrowser

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from .model import ColorPatchModel

_COLORS = ['#92a8d1', '#034f84', '#f7cac9', '#f7786b', '#deeaee',
           '#b1cbbb', '#eea29a', '#98FB98', '#d5f4e6', '#80ced6', '#fefbd8',
           '#ffef96', '#DDA0DD', '#b2b2b2', '#f4e1d2', '#9370DB']


GRID_ROWS = 25
GRID_COLS = 25
CELL_SIZE = 25
CANVAS_WIDTH = GRID_ROWS * CELL_SIZE
CANVAS_HEIGHT = GRID_COLS * CELL_SIZE


def color_patch_draw(cell):
    '''
    This function is registered with the visualization server to be called
    each tick to indicate how to draw the cell in its current state.

    :param cell:  the cell in the simulation

    :return: the portrayal dictionary.

    '''
    assert cell is not None
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    portrayal["x"] = cell.get_row()
    portrayal["y"] = cell.get_col()
    portrayal["Color"] = _COLORS[cell.get_state()]
    return portrayal


CANVAS_ELEMENT = CanvasGrid(color_patch_draw,
                            GRID_ROWS, GRID_COLS,
                            CANVAS_WIDTH, CANVAS_HEIGHT)

server = ModularServer(ColorPatchModel,
                       [CANVAS_ELEMENT], "Social conformity with Ising ferromagnetics",
                       GRID_ROWS, GRID_COLS)

# webbrowser.open('http://127.0.0.1:8521')  # TODO: make this configurable
