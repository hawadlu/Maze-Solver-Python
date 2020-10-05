"""
This class solves the maze using dijkstra.
It takes the start and end node and uses the dijkstra algorithm to find a path between them
"""

"""
Imports
"""
# from PriorityQueue import PriorityQueue
import heapq
from math import sqrt


class Dijkstra:
    """"
    Constructor
    """

    def __init__(self):
        self.path = []
        self.pathLength = 0
        self.parent = None
        self.toProcess = []

    """
    Solve the maze
    """

    def solve(self, start, end):
        start.setCost(0)
        heapq.heappush(self.toProcess, (start.getCost(), start))

        while len(self.toProcess) != 0:
            self.parent = self.toProcess.__getitem__(0)[1]  # Get the second item of the returned tuple
            self.parent.visit()

            if self.parent == end:
                break
            else:
                # Add the children
                for node in list(self.toProcess.pop(0)[1].getNeighbours()):
                    if not node.isVisited():
                        cost = self.parent.getCost() + self.calculateCost(self.parent, node)
                        # print("Cost type: " + str(type(cost)))
                        # print("Node cost type: " + str(type(node.getCost())))
                        if cost < node.getCost():
                            node.setCost(cost)
                            node.setParent(self.parent)
                            heapq.heappush(self.toProcess, (cost, node))

        # Generate a list containing the path
        while True:
            if self.parent is not None:
                self.path.append(self.parent)
                self.parent = self.parent.getParent()
                self.pathLength += 1
            else:
                break
        return self.path

    def getPathSize(self):
        return self.pathLength

    """
    Calculate the cost of moving between two nodes
    """

    @staticmethod
    def calculateCost(current, destination):
        cost = (current.getX() + destination.getX()) ** 2
        cost1 = (current.getY() + destination.getY()) ** 2
        finalCost = sqrt(cost + cost1)
        return finalCost
