
from curses import newpad
from graph import Digraph, Node, WeightedEdge


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    g = Digraph()
    with open(map_filename) as file:
        for line in file:
            src, dest, total, outdoors = line.split()
            src, dest = Node(src), Node(dest)
            try:
                g.add_node(src)
            except:
                ValueError
            try:
                g.add_node(dest)
            except:
                 ValueError
            g.add_edge(WeightedEdge(src, dest, int(total), int(outdoors)))
    return g
    
print(load_map('lines.txt'))
# print(load_map('mit_map.txt'))


# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    if digraph.has_node(start) == False and digraph.has_node(end) == False:
        raise ValueError('These are not valid nodes') # raise an error

    path[0] = path[0] + [str(start)]
    

    if str(start) == str(end):
        return (path) #update the global variables appropriately, suspect we will return more than path 
        
    for node in digraph.get_edges_for_node(start):
        
        dest = node.get_destination()
        if str(dest) not in path[0]:
            path[1] += int(node.get_total_distance())
            path[2] += int(node.get_outdoor_distance())
            if (best_path == None) or (path[2] < best_dist):
                newPath = get_best_path(digraph, dest, end, path, max_dist_outdoors, best_dist, best_path)
                if newPath != None:
                    best_path = newPath
                    best_dist = newPath[2]
                    

        if best_dist > max_dist_outdoors:
            result = None
        else:
            result = (best_path)
        
    return result 


# first = load_map('lines.txt')
# # second = load_map('mit_map.txt')
# alpha = Node('1')
# beta = Node('4')
# print(get_best_path(first, alpha, beta, [[], 0, 0], 1000, 0, None))
# # 32 -> 12 is 80, 12 -> 24 is 0, 24 -> 13 is 30, 13 -> 31 is 25
