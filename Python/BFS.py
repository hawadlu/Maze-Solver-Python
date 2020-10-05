"""
This class solves the maze breadth first.
It takes the start and end node and finds the shortest path between them.
"""
"""
Imports
"""
from MazeNode import MazeNode
from collections import deque


class BFS:
    """"
    Constructor
    """

    def __init__(self):
        self.path: list = []
        self.pathLength = 0
        self.toProcess = deque()
        self.parent = None

    """
    Solve the maze
    """

    def solve(self, start: MazeNode, end: MazeNode) -> list:
        print("Start type: " + str(type(start)))
        start.visit()
        self.toProcess.append(start)

        # Repeat until path found
        while len(self.toProcess) != 0:
            self.parent = self.toProcess.__getitem__(0)  # Get the top of the queue
            self.parent.visit()

            if self.parent == end:
                print("Path found")
                break
            else:
                # Add the children
                for node in self.toProcess.popleft().getNeighbours():
                    if not node.isVisited():
                        node.setParent(self.parent)
                        self.toProcess.append(node)

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
