#!/usr/bin/python

import sys,re 
from numpy import matrix

def main(fh):
    filedata = (x for x in fh.read().split('\n'))
    filedata = (re.split('\s+', x) for x in filedata)
    filedata = [[int(x) for x in y if x] for y in filedata]

    reading_header = True
    for line in filedata:
        if not line: continue
        if reading_header:
            nrows = line[0]
            ncols = line[1]
            rows = []
            reading_header = False
        else:
            rows.append(line)
            nrows -= 1
            if not nrows:
                solution = solve_it(len(rows), ncols, rows)
                print_solution(solution)
                reading_header = True

def print_solution(solution):
    for row in solution['rows']:
        print row + 1,
    print
    print solution['answer']

def solve_it(nrows, ncols, rows):
    """ Solving the TSP by using a two-step procedure:
        First, calculate a new matrix helper where each value is the
        cost of the path with the lowest cost and then walking
        backwards through that matrix, always choosing the lowest cost.
    """
    question = matrix(rows)
    helper = matrix(rows)
    
    # Fill in the helper matrix
    for col_idx in xrange(ncols - 2, -1, -1):
        for row_idx in xrange(nrows):
            cands = []
            cands.append(helper[(row_idx - 1) % nrows, col_idx + 1])
            cands.append(helper[(row_idx + 1) % nrows, col_idx + 1])
            cands.append(helper[row_idx, col_idx + 1])
            
            helper[row_idx, col_idx] = question[row_idx, col_idx] + min(*cands)
    
    row_series = []
    interesting_rows = xrange(nrows)
    for col_idx in xrange(ncols):
        answer_sum = answer_row = None
        for row_idx in interesting_rows:
            if answer_sum is None or helper[row_idx, col_idx] < answer_sum:
                answer_sum = helper[row_idx, col_idx]
                answer_row = row_idx
        if col_idx == 0:
            global_answer_sum = answer_sum
        row_series.append(answer_row)

        # Be sure to print the lexiographically smallest path
        interesting_rows = sorted(x % nrows for x in (answer_row, answer_row - 1, answer_row + 1))

    return {'rows': row_series, 'answer': global_answer_sum}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        main(sys.stdin)
    else:
        with open(sys.argv[1]) as fh:
            main(fh)
