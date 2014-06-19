"""
 Langton's Ant Simulator
 -----------------------

 Authors:

 Bernie Pope (bjpope@unimelb.edu.au)
 Daniel Williams (daniel.williams@unimelb.edu.au)

 Date created:

 September 2013

 Notes:

 This program is a sample solution for the first project in the
 University of Melbourne subject COMP10001 "Foundations of Computing".

 This program models the behaviour of "Langton's Ant", which is a simple
 cellular automata existing on a grid of black and white square cells. The
 ant walks about the grid one step at a time, obeying the following two rules:

   - If the ant is standing on a white cell, it changes the cell to black,
     turns right 90 degrees and takes one step forward.
   - If the ant is standing on a black cell, it changes the cell to white,
     turns left 90 degrees and takes one step forward.

 The move_ant() simulates the movement of the ant by one step; iterating
 this function will produce the movement of the ant over time.

 We do very little error checking in the program and assume the inputs to
 the functions are valid.

 The program is designed to be used with Python 2.7.

 Date modified and reason:

 10 Sept 2013: Initial working version.
 24 Sept 2013: Added documentation and tidied up code.
 26 Sept 2013: Fixed issues found by pep8 and pylint.

"""

# grid cell colours
WHITE = 'white'
BLACK = 'black'

# compass directions
NORTH = 'North'
EAST = 'East'
SOUTH = 'South'
WEST = 'West'

# turn directions
LEFT = 'left'
RIGHT = 'right'


def rotate(orientation, turn):
    """
    Given the current orientation of the ant and a direction in which to
    turn, return the new orientation after making the turn.

    Inputs:
        orientation: current orientation of ant, a compass direction
        turn: a direction to turn, left or right

    Result:
        the new orientation of the ant, a compass direction

    Examples:
        >>> rotate('North', 'left')
        'West'
        >>> rotate('North', 'right')
        'East'
        >>> rotate('East', 'right')
        'South'
    """
    # left rotations go counter-clockwise
    left_rotation = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
    # right rotations go clockwise
    right_rotation = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}
    rotation = {LEFT: left_rotation, RIGHT: right_rotation}
    return rotation[turn][orientation]


def step_forward(row, col, orientation, num_rows, num_cols):
    """
    Given the current coordinates and orientation of the ant,
    return the new coordinates after taking one step forward.

    Note: we need to wrap the ant's coordinates to the opposite side
    of the grid if it steps over an edge, hence we need to know
    how many rows and columns there are in the grid.

    Inputs:
        row: the current row coordinate of the ant (0 <= row < num_rows)
        col: the current column coordinate of the ant (0 <= col < num_cols)
        orientation: current orientation of ant, a compass direction
        num_rows: the number of rows in the grid
        num_cols: the number of columns in the grid

    Result:
        the new row and column of the ant after taking a step forward

    Examples:
        >>> step_forward(0, 0, 'East', 10, 10)
        (0, 1)
        >>> step_forward(0, 0, 'North', 10, 10)
        (9, 0)
        >>> step_forward(9, 5, 'South', 10, 10)
        (0, 5)
    """
    new_row = row
    new_col = col
    if orientation == NORTH:
        # North is towards row 0
        new_row = (row - 1) % num_rows
    elif orientation == EAST:
        # East is towards num_cols
        new_col = (col + 1) % num_cols
    elif orientation == SOUTH:
        # South is towards num_rows
        new_row = (row + 1) % num_rows
    else:  # orientation == WEST
        new_col = (col - 1) % num_cols
    return new_row, new_col


def move_ant(grid, ant_row, ant_col, orientation):
    """
    Given the current grid, and coordinates and orientation of
    the ant, return its new coordinates and orientation after
    taking one step, and modify the colour of the grid cell that
    the ant is standing on.

    If the ant is currently standing on a white cell it changes
    it to black, turns right 90 degrees and steps forward.

    If the ant is currently standing on a black cell it changes
    it to white, turns left 90 degrees and steps forward.

    If the ant steps over any of the edges of the grid it
    wraps to the opposite side.

    Inputs:
        grid: a rectangular list of lists of cells. Each cell
              is either 'white' or 'black'.
        ant_row: the current row coordinate of the ant
        ant_col: the current column coordinate of the ant
        orientation: current orientation of ant, a compass direction

    Result:
        The new row, column and orientation of the ant after taking a step

    Examples:
        >>> grid = [['black', 'black'], ['white', 'black'], ['black', 'white']]
        >>> move_ant(grid, 0, 0, 'South')
        (0, 1, 'East')
        >>> grid
        [['white', 'black'], ['white', 'black'], ['black', 'white']]
        >>> move_ant(grid, 0, 1, 'East')
        (2, 1, 'North')
        >>> grid
        [['white', 'white'], ['white', 'black'], ['black', 'white']]
    """
    # Get the number of rows and columns in the grid
    # NOTE: we assume there is at least one row in the grid.
    num_rows = len(grid)
    num_cols = len(grid[0])
    cell_colour = grid[ant_row][ant_col]
    # Modify the current cell colour and rotate.
    if cell_colour == WHITE:
        grid[ant_row][ant_col] = BLACK
        new_orientation = rotate(orientation, RIGHT)
    else:
        grid[ant_row][ant_col] = WHITE
        new_orientation = rotate(orientation, LEFT)
    # Step forward in the new direction that the ant is facing.
    new_row, new_col = step_forward(ant_row, ant_col, new_orientation,
                                    num_rows, num_cols)
    return new_row, new_col, new_orientation
