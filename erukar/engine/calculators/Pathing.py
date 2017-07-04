from erukar.engine.calculators.meta import AStarBase, Queue

class Pathing(AStarBase):
    ManhattanD = 10
    def __init__(self, collection):
        self.collection = collection

    def heuristic(self, node, goal):
        dx = abs(node[0] - goal[0])
        dy = abs(node[1] - goal[1])
        return self.ManhattanD * (dx+dy)
        
    def neighbors(self, collection, node, goal):
        possibilities = [
            (node[0]-1, node[1]),
            (node[0]+1, node[1]),
            (node[0],   node[1]-1),
            (node[0],   node[1]+1),
        ]
        return [x for x in possibilities if self.is_valid(x, collection, goal)]

    def is_valid(self, coordinate, visited, goal):
        return (coordinate not in visited and coordinate in self.collection)

    def cost(self, collection, current, node):
        return 1
