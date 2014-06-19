###############################################################################
# Authors:
#
# Bernie Pope (bjpope@unimelb.edu.au)
#
# Date created:
#
# 1 July 2013
#
# Notes:
#
# This program provides a visualisation wrapper for the first project in the
# University of Melbourne subject COMP10001 "Foundations of Computing",
# Semester 2 2013. It requires the user to supply a Python module called
# proj1.py which defines a function called move_ant which imlements the
# behaviour defined in the project specification.
#
# This program is intended to be used as a CGI script.
#
# If you serve (or share) this program on IVLE it will produce an interactive
# web page which displays the motion of Langton's ant on a grid. It provides
# controls for specifying the size of the grid, the initial configuration of
# the ant, and also allows you to pause, step and adjust the speed of the
# animation.
#
# The implementation of the animation itself is done in Javascript, which runs
# in the client's web browser.
#
# The program is designed to be used with Python 2.7.
#
# Date modified and reason:
#
# 20 August 2013: Added documentation and cleaned up the code. Made it PEP8
#                 clean.
#
# 21 August 2013: Used shorter encoding for ant state in the javascript.
#                 "North" -> "N", "black" -> "b" etcetera. Fixed HTML to be
#                 valid under the W3C validator.
#
###############################################################################


from proj1 import move_ant
import cgi

# Template string for the HTML document produced by this program. This document
# will be rendered on the client's browser. It contains javascript code for
# rendering the ant animation. The template is parameterised by various
# constant values which determine the configuration of the visualisation, most
# significantly the animation steps themselves.
page_template = \
    """<!DOCTYPE html>
    <html>
        <head><title>Langton's Ant simulation</title>
        <script type="text/javascript" src="jquery-1.6.4.min.js"></script>
        </head>
    <body>
        <h1>Langton's Ant Simulation</h1>

        <form method="post">
            <table>
                <tr>
                    <td>Cell size</td>
                    <td><input type="number" name="cell_size" min="1" max="10"
                               value="{cell_size}"></td>
                    <td>Rows</td>
                    <td><input type="number" name="rows" min="1" max="100"
                               value="{rows}"></td>
                    <td>Columns</td>
                    <td><input type="number" name="columns" min="1" max="100"
                               value="{columns}"></td>
                </tr>
                <tr>
                    <td>Start Row</td>
                    <td><input type="number" name="start_row" min="0"
                               max="{max_start_row}" value="{start_row}"></td>
                    <td>Start Column</td>
                    <td><input type="number" name="start_column" min="0"
                               max="{max_start_column}"
                               value="{start_column}"></td>
                    <td>Start Direction</td>
                    <td>
                        <select name="start_direction" id="start_direction">
                            <option value="North">North</option>
                            <option value="South">South</option>
                            <option value="East">East</option>
                            <option value="West">West</option>
                        </select>
                    </td>
                </tr>
                <tr><td><input type="submit" value="Reset"/></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
            </table>
        </form>

        <table>
            <tr>
                <td>Step:</td>
                <td id="step">0</td>
                <td>Direction:</td>
                <td id="direction">{start_direction}</td>
            </tr>
        </table>

        <canvas id="gridcanvas" width="{canvas_width}"
                height="{canvas_height}"></canvas>

        <form>
            <table>
                <tr>
                    <td><input type="radio" name="speed"
                               value="fast">Fast</td>
                    <td><input type="radio" name="speed"
                               value="medium" checked>Medium</td>
                    <td><input type="radio" name="speed"
                               value="slow">Slow</td>
                </tr>
            </table>
        </form>

        <form>
            <input type="button" id="pause" value="Play">
            <input type="button" id="next" value="Next">
        </form>

        <script>
            var canvas = $('#gridcanvas')[0];
            var context = canvas.getContext('2d');
            // Array of (row, column, colour, orientation) to trace ant steps
            var draw_instructions = {instructions};
            // Number of rows in the grid (> 0)
            var rows = {rows};
            // Number of columns in grid (> 0)
            var columns = {columns};
            // Width in pixels of the drawing area
            var canvas_width = {canvas_width};
            // Height of in pixels of the drawing area
            var canvas_height = {canvas_height};
            // Width and height in pixels of a cell (not including its
            // grid border)
            var cell_size = {cell_size};
            // Animation delay in milliseconds for slow, medium and fast
            // animation
            var slow_delay = 300;
            var medium_delay = 100;
            var fast_delay = 0;
            var animation_delay = medium_delay;
            // Flag for pausing the animation (not updating the ant), starts
            // as paused
            var paused = true;
            // Flag for stepping the animation by one
            var one_step = false;

            // Set the start direction selector to be the one previously set
            // (or default).
            $('#start_direction').val("{start_direction}");


            // Convert the short single-character code for orientation into the
            // full english word. 'N' -> 'North' etc.
            function decode_orientation(orientation) {{
                if (orientation == 'N') {{
                    return 'North';
                }}
                else if (orientation == 'S') {{
                    return 'South';
                }}
                else if (orientation == 'E') {{
                    return 'East';
                }}
                // orientation == 'W' (anything else would be a fatal error)
                else {{
                    return 'West';
                }}
            }}

            // Draw a horizontal line on the canvas at pixel row
            function horizontal_line(row) {{
                context.beginPath();
                context.moveTo(0, row);
                context.lineTo(canvas_width, row);
                context.stroke();
            }}

            // Draw a vertical line on the canvas at pixel column
            function vertical_line(column) {{
                context.beginPath();
                context.moveTo(column, 0);
                context.lineTo(column, canvas_height);
                context.stroke();
            }}

            // Draw the borders of the rows and columns of the grid.
            // Note that the lines are offset by 0.5 because of the way
            // the coordinates work in the HTML canvas element. Drawing
            // a one-pixel wide line at the 0.5 positions produces a line
            // right in the middle of a pixel. If you draw on the edge of
            // a pixel it gets aliased to both sides, and becomes an extra
            // pixel wider.
            function draw_grid() {{
                for(pos = 0; pos <= rows; pos += 1) {{
                    horizontal_line((pos * (cell_size + 1)) + 0.5);
                }}

                for(pos = 0; pos <= columns; pos += 1) {{
                    vertical_line((pos * (cell_size + 1)) + 0.5);
                }}
            }}

            // Calculate the pixel offset for drawing a cell rectangle based
            // on the index of the cell in the grid. This calculation caters
            // for the extra pixels introduced by the grid borders.
            function draw_offset(n) {{
                return (n * (cell_size + 1)) + 1;
            }}

            // Draw the current position of the ant in red.
            function draw_ant(x, y) {{
                context.fillStyle = "#f00";
                context.fillRect(draw_offset(x), draw_offset(y),
                                 cell_size, cell_size);
                context.fill();
            }}

            // Draw the previous position of the ant in whatever colour it has.
            // This is required because we render the current ant position in
            // red. When we move to the next position we have to overwrite the
            // red cell with the appropriate colour.
            function draw_previous_ant(x, y, colour) {{
                if (colour == 'b') {{
                    context.fillStyle = "#000";
                }}
                else {{
                    context.fillStyle = "#fff";
                }}
                context.fillRect(draw_offset(x), draw_offset(y), cell_size,
                                 cell_size);
                context.fill();
            }}

            // Draw the next step of the ant animation.
            // index is the number of the current step (starting at 0).
            // max_index is the maximum step of the animation.
            // We stop when index >= max_index.
            // This function calls itself recursively after a given timeout
            // period. This allows us to control the speed of the animation by
            // adjusting the value of the timeout.
            function animate(index, max_index) {{
                if (index >= max_index) {{
                    // Stop the animation, we've run out of steps.
                    return;
                }}
                // Call animate again with a timeout, and possibly update the
                // display.
                setTimeout(function () {{
                    // Get the next state of the ant.
                    var data = draw_instructions[index];
                    var y = data[0];
                    var x = data[1];

                    // Draw the ant at its current position (it is always red)
                    draw_ant(x, y);

                    // If we aren't at the first step in the animation, get the
                    // previous position of the ant and update its cell with
                    // the correct colour. This will overwrite the red with the
                    // appropriate colour for the cell.
                    if (index > 0) {{
                            var previous_data = draw_instructions[index-1];
                            var y = previous_data[0];
                            var x = previous_data[1];
                            var colour = previous_data[2];
                            draw_previous_ant(x, y, colour);
                    }}

                    // If we aren't paused or in single step mode, move
                    // the ant to its next position.
                    if(!paused || one_step) {{
                        // Update the document elements which report the
                        // current step number and the orientation of the ant.
                        $('#step').text(index);
                        $('#direction').text(decode_orientation(data[3]));

                        // If we were single stepping, turn it off for the next
                        // iteration.
                        if (one_step) {{
                            one_step = false;
                        }}
                        // perform the next step of the animation
                        animate(index + 1, max_index);
                    }}
                    // Pause the animation, which is achieved by
                    // re-doing the current step again.
                    else {{
                        animate(index, max_index);
                    }}
                }}, animation_delay);
            }}

            // Draw the grid and start the animation loop when the page loads.
            window.onload = function() {{
                draw_grid();
                animate(0, draw_instructions.length);
            }}

            // Adjust the animation speed through the 'speed' radio buttons.
            $("input[name='speed']").change(function(){{
               var selection=$(this).val();
               if (selection == 'slow') {{
                  animation_delay = slow_delay;
               }}
               else if (selection == 'medium') {{
                  animation_delay = medium_delay;
               }}
               else if (selection == 'fast') {{
                  animation_delay = fast_delay;
               }}
            }});

            // Toggle single stepping mode
            $('#next').click(function() {{
                one_step = true;
            }});

            // Pause/play the animation, and adjust whether
            // the 'next' button is visible.
            $('#pause').click(function() {{
                var buttonLabel = $(this).val();
                if (buttonLabel == "Pause") {{
                   $(this).val("Play");
                   $('#next').toggle();
                }}
                else {{
                   $(this).val("Pause");
                   $('#next').toggle();
                }}
                paused = !paused;
            }});
        </script>
    </body>
    </html>
    """


# Initialise the grid with a specified number of rows and columns.
# Each cell in the grid is set to 'white'.
def init_ant_grid(grid_rows, grid_columns):
    grid = []
    for _row in range(grid_rows):
        new_row = []
        for _column in range(grid_columns):
            new_row.append('white')
        grid.append(new_row)
    return grid


# Lookup an entry in the field store corresponding to a value
# entered into the HTML page.
# store: the field store containing the values entered into the page
# field_name: the name of the entry to look up
# default: return this value if we don't find the name or it is not bound
# to a valid integer.
# min_val: clamp the entered value at this lower bound
# max_val: clamp the entered value at this upper bound
def get_cgi_field_int(store, field_name, default, min_val, max_val):
    result = default
    if field_name in store:
        store_val = store.getvalue(field_name)
        if store_val.isdigit():
            result = int(store_val)
    return max(min(result, max_val), min_val)


# Lookup the start_direction entry in the field store corresponding
# to a value entered into the HTML page.
# store:  the field store containing the values entered into the page
# default: return this value if we can't find the name or it wasn't
# bound to a valid direction.
def get_cgi_field_direction(store, default):
    result = default
    if 'start_direction' in store:
        store_val = store.getvalue('start_direction')
        if store_val in ['North', 'South', 'East', 'West']:
            result = store_val
    return result


# Convert the long English form of an orientation to a single
# character encoding. 'North' -> 'N' etc. The advantage of this
# is that it makes the generated HTML page shorter, because we
# include the orientation informaiton with every ant move as
# a javascript array.
def encode_orientation(orientation):
    if orientation == 'North':
        return 'N'
    elif orientation == 'South':
        return 'S'
    elif orientation == 'East':
        return 'E'
    # orientation == 'W'
    else:
        return 'W'


# Convert the long English form of a colour to a single character
# encoding. 'black' -> 'b', 'white' -> 'w'. The advantage of this
# is that it makes the generated HTML page shorter, because we
# include the colour informaiton with every ant move as
# a javascript array.
def encode_colour(colour):
    if colour == 'black':
        return 'b'
    # colour == 'white'
    else:
        return 'w'


# Iterate the ant simulation a number of times accumulating the steps
# made by the ant. Then render a HTML page as a CGI script containing
# a javascript visualisation of the motion of the ant.
def main():
    # Various default values for the animation. This will be used the
    # first time the page is loaded by the client browser.
    default_rows = 100
    default_columns = 100
    max_rows = 100
    max_columns = 100
    max_cell_size = 100
    max_iterations = 12000
    default_cell_size = 5
    default_direction = 'North'

    # Fetch the values (if any) entered into the HTML page by the user
    store = cgi.FieldStorage()

    # Get the requested number of rows and columns for the grid
    rows = get_cgi_field_int(store, 'rows', default_rows, 1, max_rows)
    columns = get_cgi_field_int(store, 'columns', default_columns, 1,
                                max_columns)

    # By default the start row and column are set to the 'middle' positions
    # respectively.
    default_start_row = rows // 2
    default_start_column = columns // 2

    # Get the requested start row and column for the ant
    start_row = get_cgi_field_int(store, 'start_row',
                                  default_start_row, 0, rows - 1)
    start_column = get_cgi_field_int(store, 'start_column',
                                     default_start_column, 0, columns - 1)

    # Get the requested size of a cell in pixels
    cell_size = get_cgi_field_int(store, 'cell_size', default_cell_size,
                                  1, max_cell_size)

    # Get the requested starting orientation for the ant
    start_direction = get_cgi_field_direction(store, default_direction)
    ant_orient = start_direction

    # Set up the initial empty grid
    grid = init_ant_grid(rows, columns)

    ant_row = start_row
    ant_column = start_column
    draw_instructions = []

    # Iterate the move_ant function 'max_iterations' times
    # and accumulate a list of ant states.
    for _i in range(max_iterations):
        old_row = ant_row
        old_column = ant_column
        ant_row, ant_column, ant_orient = move_ant(grid, ant_row, ant_column,
                                                   ant_orient)
        # Record the colour of the ant at its previous position before the move
        colour = grid[old_row][old_column]
        draw_instructions.append(
            "[{0}, {1}, '{2}', '{3}']".format(old_row, old_column,
                                              encode_colour(colour),
                                              encode_orientation(ant_orient)))

    # Convert the list of ant states into a string representing a javascript
    # array of tuples.
    draw_instructions_str = '[' + ','.join(draw_instructions) + ']'
    # Calculate the size of the drawing canvas in pixels, accounting for the
    #size of the cells and the one-pixel borders around each cell.
    canvas_width = columns * (cell_size + 1) + 1
    canvas_height = rows * (cell_size + 1) + 1

    # Print the required HTTP headers for our CGI output (to make this a web
    # application on IVLE).
    print("Content-Type: text/html")
    print

    # Convert the page template into a complete HTML document and print it out
    print(page_template.format(
        instructions=draw_instructions_str,
        canvas_width=canvas_width,
        canvas_height=canvas_height,
        cell_size=cell_size,
        rows=rows,
        columns=columns,
        start_row=start_row,
        start_column=start_column,
        max_start_row=rows - 1,
        max_start_column=columns - 1,
        start_direction=start_direction
        ))

# Run the whole program, starting with the main function
if __name__ == '__main__':
    main()
