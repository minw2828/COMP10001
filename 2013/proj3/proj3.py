################################################################################
# 
# Description:
#
# This module is an attempt to satisfy the requirements of Project 3 for 
# the University of Melbourne subject COMP10001 "Foundations of Computing". 
# 
# The module: 
# - take CSV file which stores collections of reads as input 
# - chech validity of the input file
# - calculate the depth of coverage in region of interest
# - plot depth of coverage in region of interest in a bar chart
# - generate a HTML report for multiple samples
#
# Author:
#
# Min Wang (minw2828@gmail.com)
#
# Date Created:
#
# 14 Oct 2013
# 
# The program is designed to be used with Python 2.6 and 2.7.
#
# Date modified and reason:
#
# 17 October 2012: Added more detailed comments to the program.
#
################################################################################

import sys
import csv
import doctest
import plot

def read_file(filename):
    '''
    Given: a CSV file with headers. Each line records the start coordinate 
           & end coordinate of a read alignment.
    Return: lists of file contents. Each line in file returns as a list.

    Example:
    >>> read_file('example.csv')
    [['read_start', 'read_end'], ['25', '30'], ['23', '26'], ['32', '41'], 
     ['26', '30'], ['33', '36'], ['32', '41'], ['24', '28'], ['26', '29'], 
     ['35', '39']]
    '''
    f = open(filename,'rb')
    reader = csv.reader(f)
    data = [row for row in reader]
    f.close()
    return data

def _header(data):
    '''
    Given: lists of CSV file contents from read_file(filename).
    Return: True if The first line is exactly the string: read_start,read_end; 
            False otherwise
    
    Examples:
    >>> _header([['read_start', 'read_end'], ['25', '30'], ['23', '26'], 
                 ['32', '41'], ['26', '30'], ['33', '36'], ['32', '41'], 
                 ['24', '28'], ['26', '29'], ['35', '39']])
    True
    >>> _header([['readstart', 'read_end'], ['25', '30'], ['23', '26'], 
                 ['32', '41'], ['26', '30'],['33', '36'], ['32', '41'], 
                 ['24', '28'], ['26', '29'], ['35', '39']])
    False
    '''
    HEADER = 'read_start,read_end'
    if data[0] != HEADER.split(','):
        return False
    return True

def _length(data):
    '''
    Given: lists of file contents from read_file(filename).
    Return: True if there are zero or more additional lines in the file 
            containing the start and end positions of an aligned read, 
            one per line; False otherwise.
    
    Examples:
    >>> _length([['read_start', 'read_end'], ['25', '30'], ['23', '26'], 
                 ['32', '41'], ['26', '30'],['33', '36'], ['32', '41'], 
                 ['24', '28'], ['26', '29'], ['35', '39']])
    True
    >>> _length([['read_start', 'read_end'], ['28', '30 23', '26 32', 
                  '41 26', '30 33', '50 32', '41 24', '28 26', '39']])
    False
    '''
    try:
        for row in data[1:]:
            if len(row) != 2:
                return False
        return True
    except ValueError:
        return False

def _value(data):
    '''
    Given: lists of file contents from read_file(filename).
    Return: True if Each aligned read is represented by a pair of non-negative 
            integers separated by only a comma; False otherwise.

    Examples:
    >>> _value([['read_start', 'read_end'], ['25', '30'], ['23', '26'], 
                ['32', '41'], ['26', '30'], ['33', '36'], ['32', '41'], 
                ['24', '28'], ['26', '29'], ['35', '39']])
    True
    >>> _value([['read_start', 'read_end'], ['28 30'], ['23', '', '', '26'], 
                ['32\\t41'], ['26', '30'], ['33\\n50'], ['32', '41'], 
                ['24', '28'], ['26', '29'], ['35', '39']])
    False
    '''
    try:
        for v1, v2 in data[1:]:
            if not isinstance(eval(v1), int):
                return False
            elif not isinstance(eval(v2), int):
                return False
            elif eval(v1) < 0:
                return False
            elif eval(v2) < 0:
                return False
        return True
    except ValueError:
        return False

def _compare(data):
    '''
    Given: lists of file contents from read_file(filename).
    Return: True if the first integer on each line is less than or equal to 
            the second integer on each line; False otherwise.
   
    Examples:
    >>> _length([['read_start', 'read_end'], ['25', '30'], ['23', '26'], 
                 ['32', '41'], ['26', '30'], ['33', '36'], ['32', '41'], 
                 ['24', '28'], ['26', '29'], ['35', '39']])
    True
    >>> _length([['read_start', 'read_end'], ['30', '25'], ['42', '26'], 
                 ['32', '41'], ['26', '30'], ['33', '36'], ['32', '41'], 
                 ['24', '28'], ['26', '29'], ['35', '39']])
    False
    '''
    try:
        for v1, v2 in data[1:]:
            if eval(v1) > eval(v2):
                return False
        return True
    except ValueError:
        return False

def validate_alignment(alignment_filename):
    '''
    Given: a CSV file with headers. Each line records the start coordinate 
           & end coordinate of a read alignment.
    Return: True if file content meets all conditions in function _header, 
            _length, _value and _compare; False otherwise.   
    '''
    data = read_file(alignment_filename)
    if not _header(data):
        return False
    elif not _length(data):
        return False
    elif not _value(data):
        return False
    elif not _compare(data):
        return False
    return True

def coverage(starts, ends, region_start, region_end):
    '''
    Given: read coordinates and reference genome coordinates, this function 
           calculates the depth of coverage in region of interest.
    Return: a list of non-negative integers that correspond to the depth of 
            coverage in region of interest.

    Inputs:
        starts: a list of non-negative integers. Each interger coresponds to 
                the start coordinate of the read.
        ends: a list of non-negative integers. Each interger coresponds to 
              the end coordinate of the read.
        region_start: a non-negative integer that represends the start 
                      coordinate of the region of interest.
        region_end: a non-negative integer that represends the end coordinate 
                    of the region of interest.

    Example:
    >>> coverage([1,2,3,4,5,8,9,10],[23,26,27,29,32,33,38,40],3,37)
    [3, 4, 5, 5, 5, 6, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 
     7, 7, 6, 5, 5, 4, 4, 4, 3, 2, 2, 2, 2]

    Note that the function assumes the following about its arguments: 
    1. Input parameter starts and ends store a list of integers.
    2. The items in starts and ends are sorted numerically respectively.
    3. The lengths of starts and ends are the same.
    4. The value of the item in starts is no greater than that in ends of the same index.
    5. Input parameter region_start and region_end are integers.
    6. The value of region_start is less than that of region_end.
    '''

    # Define a list that records the number of reads covering each coordinate 
    # in a region of interest.
    counts = []

    # Define an integer that calculates the depth of coverage at a given coordinate 
    # of the reference genome.
    running_coverage = 0 

    # The following for loop calculates the depth of coverage (running_coverage) 
    # accumulatively by comparing each referece genome coordinate in region of 
    # interest (this_coord) with a read start coordinate in starts (this_start) 
    # and a read end coordinate in ends (this_end). If this_coord is less than 
    # this_start, then the_coord is not covered by the read. In this case, the 
    # program will not do anything. If this_coord is no less than a this_start, 
    # then this_coord is covered by a read and the program will add 1 more record 
    # to running_coverage. If this_coord is no greater than this_end, this_coord 
    # is still covered by the read. In this case, the program will not do anything. 
    # But if this_coord is greater than a this_end, this_coord is not covered by one 
    # less read than it was, the program will substract 1 record from runnning_coverage.
    for this_coord in range(region_start, region_end + 1):

        # The following while loop calculates the number of reads whose this_start is 
        # no greater than this_coord for all this_coord in region of interest.
        while starts:
            this_start = starts[0]
            if this_coord >= this_start:
                running_coverage += 1
                starts = starts[1:]
            elif this_coord < this_start:
                break
        
        # The following while loop calculates the number of reads whose this_end is no
        # less than this_coord for all this_coord in region of interest.
        while ends:
            this_end = ends[0] + 1
            if this_coord >= this_end:
               running_coverage -= 1
               ends = ends[1:]
            elif this_coord < this_end:
               break
     
        # The number of reads that cover this_coord has been calculated from the above 
        # two while loops. The program then records the result to pre-defined list count.
        counts.append(running_coverage)
    return counts

def plot_coverage(title, region_start, region_end, alignment_filename):
    '''
    Given: the title of the bar chart, region of interest and an alignment file.
    Return: an SVG file and three statistics if the alignment file is valided. 
            The SVG file contains a bar chart plot from the depth of coverage in 
            region of interest. The three statistics are the minimum coverage, 
            maximum coverage and average coverage in region of interest.

    Inputs:
        title: a string specifying the text for the title of the bar chart.
        region_start: a non-negative integer specifying the start position of 
                      the region of interest.
        region_end: a non-negative integer specifying the end position of the 
                    region of interest.
        alignment_filename: a string specifying the name of an alignment file, 
                            the name must end in .csv
    
    Examples:
    >>> plot_coverage('Project Spec Example 2', 16, 50, 'example2.csv')
    (0, 6, 2.2)
    >>> plot_coverage('Project Spec Example 3', 16, 30, 'example3.csv')
    None
    
    Note: 
    1. The name of the SVG file is based on the name of the input alignment file,
       with the '.csv' suffix is replaced with '.svg'.
    2. example2.csv is a valid alignment file.
    3. example3.csv is an invalid alignment file.
    '''
    if not validate_alignment(alignment_filename):
        return None
        exit()

    data = read_file(alignment_filename)[1:]
    starts = [eval(row[0]) for row in data]
    ends = [eval(row[1]) for row in data]
    
    counts = coverage(sorted(starts), sorted(ends), region_start, region_end)
    
    # Input parameter of plot.plot_graph: filename, is the name of the file to 
    # write the bar chart to. The name must end in '.svg'.
    filename = alignment_filename.replace('.csv', '.svg')
    svg_file = plot.plot_graph(region_start, region_end, counts, title, filename)
    
    if len(counts) == 0:
        minimum_coverage, maximum_coverage, average_coverage = 0, 0, 0
    else:
        minimum_coverage = min(item for item in counts)
        maximum_coverage = max(item for item in counts)
        average_coverage = sum(counts)/float(len(counts))

    return (minimum_coverage, maximum_coverage, round(average_coverage,2))

def document_samples(samples_filename):
    '''
    Given: a CSV file containing title of the project, multiple read alignment data
           sets and regions of interest.
    Return: a html file that reports coverage statistics and a depth of coverage bar 
            charts in regions of interest from alignment files that are valid.

    Inputs:
        title: a title for the data set to be displayed in the corresponding bar chart.
        alignment filename: the name of the alignment file for the data set.
        region start: the start position for the region of interest.
        region end: the end position for the region of interest.

    Note:
    1. The input samples file must be in CSV format.
    2. The name of the output HTML file is based on the name of the input CSV file, 
       with the '.csv' suffix replaced by '.html'.
    '''
    if not samples_filename.endswith('.csv'):
        samples_filename = '.'.join(samples_filename.split('.')[:-1])+'.csv'

    sample_data  = read_file(samples_filename)[1:]
    sample_data = [record for record in sample_data if validate_alignment(record[1])]
    countss = [plot_coverage(title, eval(region_start), eval(region_end), filename) 
               for title, filename, region_start, region_end in sample_data]
    
    output_filename = '.'.join(samples_filename.split('.')[:-1])+'.html'
    f = open(output_filename,'w')
    f.write('<!DOCTYPE html>\n<html>\n'+' '*4
            +'<head><title>DNA sequence alignment coverage</title></head>\n'
            +' '*4+'<body>\n'+' '*4+'<h1>DNA sequence alignment coverage</h1>\n')
    for i in range(len(countss)):
        f.write(' '*(4*2)+'<h2>Sample '+str(i+1)+'</h2>\n'+' '*(4*2)+'<ul>\n'
                +' '*(4*3)+'<li>file: '+sample_data[i][1]+'</li>\n'+' '*(4*3)
                +'<li>minimum depth: '+str(countss[i][0])+'</li>\n'+' '*(4*3)
                +'<li>maximum depth: '+str(countss[i][1])+'</li>\n'+' '*(4*3)
                +'<li>average depth: '+str(countss[i][2])+'</li>\n'+' '*(4*2)
                +'</ul>\n'+' '*(4*2)+'<img src=\"'+sample_data[i][1].split('.')[0]
                +'.svg\"\n'+' '*(4*3+1)+'alt=\"read alignment coverage bar chart for '
                +sample_data[i][1]+'\"/>\n')
    f.write(' '*4+'</body>\n</html>')

    return None
    f.close()


if __name__ == '__main__':

    alignment_filename = sys.argv[-1]
    document_samples(alignment_filename)
