import sys,re 
from numpy import matrix

def main(fh):
    states = ('NUMBER_OF_CITIES', 'CITIES', 'NUMBER_OF_ROUTES', 'ROUTES')
    trans = dict(zip(states, states[1:] + states[0:1]))

    cities = []; routes = {}
    ncities = None; nroutes = None
    map_num = 1
    state = 'NUMBER_OF_CITIES'
    for line in fh:
        line = line.strip()
        if not line: continue
        if state == 'NUMBER_OF_CITIES':
            ncities = int(line)
            # Quit when reaching ncities = 0
            cities = []
            routes = {}
            if ncities == 0:
                return
            state = trans[state]
        elif state == 'CITIES':
            cities.append(line)
            routes[line] = []
            ncities -= 1
            if ncities == 0:
                state = trans[state]
        elif state == 'NUMBER_OF_ROUTES':
            nroutes = int(line)
            state = trans[state]
        elif state == 'ROUTES':
            nroutes -= 1
            city1, city2 = re.split(r'\s+', line)
            routes[city1].append(city2)
            routes[city2].append(city1)
            if nroutes == 0:
                solution = solve_it(cities, routes)
                print_solution(map_num, solution)
                map_num += 1
                state = trans[state]
                
def print_solution(map_num, solution):
    if map_num != 1:
        print
    print "City map #%d: %d camera(s) found" % (map_num, len(solution))
    for sol in solution:
        print sol

def solve_it(cities, routes):
    """In turn we try to travel from each city as far as we can, each
    time removing one other city to see if we were dependent on it,
    for further traversal. """
    res = []
    for city1 in cities:
        # first determine which cities we can travel to from city1.
        to_be_explored = set((city1, ))
        have_seen = set()
        while to_be_explored:
            examinee = to_be_explored.pop()
            have_seen.add(examinee)
            to_be_explored = to_be_explored.union(routes[examinee])
            # Remove cities already seen
            to_be_explored = to_be_explored - have_seen
        cities_from_city1 = have_seen

        # Remove one city and see which cities we get
        for city2 in cities:
            if city2 in res or city2 == city1:
                continue
            to_be_explored = set((city1, ))
            have_seen = set((city2, ))
            while to_be_explored:
                examinee = to_be_explored.pop()
                have_seen.add(examinee)
                to_be_explored = to_be_explored.union(routes[examinee])
                to_be_explored = to_be_explored - have_seen
            
            if cities_from_city1 - set(have_seen):
                res.append(city2)
    return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        main(sys.stdin)
    else:
        with open(sys.argv[1]) as fh:
            main(fh)
