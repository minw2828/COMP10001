"""
 Bar chart plotting library
 --------------------------

 Authors:

 Bernie Pope (bjpope@unimelb.edu.au)

 Date created:

 October 2013

 Notes:

 This module implements a simple bar chart plotting function for the
 purposes of plotting read alignment coverage data for Project 3,
 COMP10001 Foundations of Computing at The University of Melbourne. It
 uses the Matplotlib Python library to generate the bar chart.

 The module is designed to be used with Python 2.7.

 Date modified and reason:

 1 Oct 2013: Initial working version.
 2 Oct 2013: Changed from line chart to bar chart
 4 Oct 2013: Set edge color to 'none' and linewidth to 0.
 7 Oct 2013: Added more documentation.

"""

import matplotlib
# Generate output graphs in SVG format and turn off warnings which
# are normally generated when the module is reloaded.
matplotlib.use('svg', warn=False)
import matplotlib.pyplot as plt

def plot_graph(start, end, counts, title, filename):
    """
    Plot a bar chart of a list of counts representing read alignment
    information. The output is written to a SVG file.

    Inputs:
        start: a non-negative integer indicating the start of the
             region of interest. This will be the lower X coordinate.
        end: a non-negative integer indicating the end of the region
             of interest. This will be the upper X coordinate.
        counts: a list of non-negative integers. Each element represents
             a single data point; the height of a bar in the chart.
             We assume: len(counts) == end - start + 1. If the length
             of counts is 0 the function does not generate a bar chart,
             and instead prints a warning message.
        title: a string for the title of the graph
        filename: the name of the file to write the bar chart to. The
             name must end in '.svg'.

    Result:
        None
    
    Examples:
        >>> plot_graph(5, 8, [22, 0, 9, 11], "This is a title string",
                       "output.svg")
    """
    # the consecutive sequence of X coordinates between start and end
    # this represents the values on the X axis
    coords_range = range(start, end + 1)
    # check that we have at least one value to plot
    num_counts = len(counts)
    if num_counts == 0:
        print("plot_graph: warning, counts list has zero length")
        # do not plot the graph
        return None
    # check that the specified region of interest is the same size as
    # the number of elements in counts
    elif len(coords_range) != num_counts:
        print("Coordinate range size {} not equal to number of counts{}"
              .format(len(coords_range), num_counts))
        # do not plot the graph
        return None
    else:
        # Draw the bar chart and save it to a file
        max_count = max(counts)
        plt.ylabel("Coverage")
        plt.xlabel("Position")
        # Generate a title for the graph using the input title string
        # plus the start and end coordinates of the region of interest
        plt.title("{}\n{}-{}".format(title, start, end))
        # Generate a bar chart from the supplied data. Bars are colored
        # blue with no edges. Anti-aliasing is turned off. Bars are
        # centered over their X axis points.      
        plt.bar(coords_range, counts, color='blue', edgecolor='none',
                aa=False, linewidth=0, align='center')
        # Set the X and Y axes
        # The X axes ranges from start to end +/- 0.5 to account
        # for the bars being centered over their X axis points.
        # The Y axis ranges from 0 to the maximum value in counts.
        plt.axis([start-0.5,end+0.5,0,max_count])
        # Write the graph to the specified filename
        plt.savefig(filename)
        # Finish drawing the graph, so that subsequent graphs will
        # be drawn separately (not on top of the same axes).
        plt.close()
