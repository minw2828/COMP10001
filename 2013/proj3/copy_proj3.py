import sys
import csv
import doctest
import plot

def read_file(filename):
    f = open(filename,'rb')
    reader = csv.reader(f)
    data = [row for row in reader]
    f.close()
    return data

def _header(data):
    HEADER = 'read_start,read_end'
    if data[0] != HEADER.split(','):
        return False
    return True

def _length(data):
    try:
        for row in data[1:]:
            if len(row) != 2:
                return False
        return True
    except ValueError:
        return False

def _value(data):
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
    try:
        for v1, v2 in data[1:]:
            if eval(v1) > eval(v2):
                return False
        return False
    except ValueError:
        return False

def validate_alignment(alignment_filename):
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
    counts = []
    running_coverage = 0 
    for this_coord in range(region_start, region_end + 1):
        print 'this_coord: '+str(this_coord)
        while starts:
            this_start = starts[0]
            print 'this_start: '+str(this_start)
            if this_coord >= this_start:
                running_coverage += 1
                print 'running_coverage: '+str(running_coverage)
                starts = starts[1:]
                print 'starts: '+str(starts)
            elif this_coord < this_start:
                print 'this_coord < this_start'
                break
        while ends:
            this_end = ends[0] + 1
            print 'this_end: '+str(this_end)
            if this_coord >= this_end:
               running_coverage -= 1
               print 'running_coverage: '+str(running_coverage)
               ends = ends[1:]
               print 'end:' + str(ends)
            elif this_coord < this_end:
               print 'this_coord < this_end'
               break
        
        counts.append(running_coverage)
        print ''
    print 'counts:'+str(counts)
    return counts

def plot_coverage(title, region_start, region_end, alignment_filename):
    if not validate_alignment(alignment_filename):
        return None
        exit()
    data = read_file(alignment_filename)[1:]
    starts = [eval(row[0]) for row in data]
    ends = [eval(row[1]) for row in data]
    
    counts = coverage(sorted(starts), sorted(ends), region_start, region_end)
    
    alignment_filename = alignment_filename.replace('.csv', '.svg')
    svg_file = plot.plot_graph(region_start, region_end, counts, title, alignment_filename)
    
    if len(counts) == 0:
        minimum_coverage, maximum_coverage, average_coverage = 0, 0, 0
    else:
        minimum_coverage = min(item for item in counts)
        maximum_coverage = max(item for item in counts)
        average_coverage = sum(counts)/float(len(counts))
    return (minimum_coverage, maximum_coverage, round(average_coverage,2))

def document_samples(samples_filename):
    if not samples_filename.endswith('.csv'):
        samples_filename = samples_filename.split('.')[0]+'.csv'
    sample_data  = read_file(samples_filename)[1:]
    sample_data = [record for record in sample_data if validate_alignment(record[1])]
    countss = [plot_coverage(title, eval(region_start), eval(region_end), filename) 
               for title, filename, region_start, region_end in sample_data]
    
    output_filename = '.'.join(samples_filename.split('.')[:-1])+'.html'
    f = open(output_filename,'w')
    f.write('<!DOCTYPE html>\n<html>\n'+' '*4+'<head><title>DNA sequence alignment coverage</title></head>\n'+' '*4+'<body>\n'+' '*4+'<h1>DNA sequence alignment coverage</h1>\n')
    for i in range(len(countss)):
        f.write(' '*(4*2)+'<h2>Sample '+str(i+1)+'</h2>\n'+' '*(4*2)+'<ul>\n'+' '*(4*3)+'<li>file: '+sample_data[i][1]+'</li>\n'+' '*(4*3)+'<li>minimum depth: '+str(countss[i][0])+'</li>\n'+' '*(4*3)
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
