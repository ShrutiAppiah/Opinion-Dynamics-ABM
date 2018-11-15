"""
The model - a 2D lattice where agents live and have an opinion
"""


import random
from collections import Counter

from mesa import Model, Agent
from mesa.time import SimultaneousActivation
from mesa.space import Grid


class ColorCell(Agent):
    '''
    Represents a cell's opinion (visualized by a color)
    '''

    OPINIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    def __init__(self, pos, model, initial_state):
        '''
        Create a cell, in the given state, at the given row, col position.
        '''
        super().__init__(pos, model)
        self._row = pos[0]
        self._col = pos[1]
        self._state = initial_state
        self._next_state = None

    def get_col(self):
        '''Return the col location of this cell.'''
        return self._col

    def get_row(self):
        '''Return the row location of this cell.'''
        return self._row

    def get_state(self):
        '''Return the current state (OPINION) of this cell.'''
        return self._state

    def step(self):
        '''
        Determines the agent opinion for the next step by polling its neighbors
        The opinion is determined by the majority of the 8 neighbors' opinion
        A choice is made at random in case of a tie
        The next state is stored until all cells have been polled
        '''
        neighbor_iter_ = self.model.grid.neighbor_iter((self._row, self._col), True)
        neighbors_opinion = Counter(n.get_state() for n in neighbor_iter_)
        # Following is a a tuple (attribute, occurrences)
        polled_opinions = neighbors_opinion.most_common()
        tied_opinions = []
        for neighbor in polled_opinions:
            if neighbor[1] == polled_opinions[0][1]:
                tied_opinions.append(neighbor)

        # print("my state", self._state)
        # print("TIED OPINIONS", tied_opinions)
        self._next_state = random.choice(tied_opinions)[0]
        # print("next state", self._next_state)

    def advance(self):
        '''
        Set the state of the agent to the next state
        '''
        self._state = self._next_state


class ColorPatchModel(Model):
    '''
    represents a 2D lattice where agents live
    '''

    def __init__(self, width, height):
        '''
        Create a 2D lattice with strict borders where agents live
        The agents next state is first determined before updating the grid
        '''

        self._grid = Grid(width, height, torus=False)
        self._schedule = SimultaneousActivation(self)

        # self._grid.coord_iter()
        #  --> should really not return content + col + row
        #  -->but only col & row
        # for (contents, col, row) in self._grid.coord_iter():
        # replaced content with _ to appease linter
        for (_, row, col) in self._grid.coord_iter():
            cell = ColorCell((row, col), self,
                             ColorCell.OPINIONS[random.randrange(0, 16)])
            self._grid.place_agent(cell, (row, col))
            self._schedule.add(cell)

        self.running = True

    def step(self):
        '''
        Advance the model one step.
        '''
        self._schedule.step()

    # the following is a temporary fix for the framework classes accessing
    # model attributes directly
    # I don't think it should
    #   --> it imposes upon the model builder to use the attributes names that
    #       the framework expects.
    #
    # Traceback included in docstrings

    @property
    def grid(self):
        return self._grid

    @property
    def schedule(self):
        return self._schedule
