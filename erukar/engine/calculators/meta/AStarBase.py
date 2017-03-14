from erukar.engine.calculators.meta.PriorityQueue import PriorityQueue

class AStarBase:
    def heuristic(self, node, goal):
        raise NotImplementedError('heuristic() must be defined in implementation of AStarTemplate')

    def neighbors(self, collection, node, goal):
        raise NotImplementedError('neighbors() must be defined in implementation of AStarTemplate')

    def cost(self, collection, current, node):
        raise NotImplementedError('cost() must be defined in implementation of AStarTemplate')

    def search(self, collection, start, goal):
        '''Thanks to http://www.redblobgames.com/pathfinding/a-star/implementation.html'''
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        elapsed_cost = {}
        came_from[start] = None
        elapsed_cost[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break
            
            for next in self.neighbors(came_from, current, goal):
                new_cost = elapsed_cost[current] + self.cost(collection, current, next)
                if next not in elapsed_cost or new_cost < elapsed_cost[next]:
                    elapsed_cost[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, elapsed_cost

    def reverse(self, came_from, start, goal):
        current = goal
        path = [current]
        
        try:
            while current != start:
                current = came_from[current]
                path.append(current)
        except:
            return []

        path.append(start) # optional
        path.reverse() # optional

        return path
