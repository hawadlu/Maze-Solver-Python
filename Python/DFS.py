"""
This class solves the maze depth first.
It takes the start and end node and finds a path between them.
"""
"""
Imports
"""
from Stack import Stack


class DFS:
    """"
    Constructor
    """

    def __init__(self):
        self.path = []
        self.pathLength = 0
        self.toProcess = Stack()
        self.parent = None

    """
    Solve the maze
    """

    def solve(self, start, end):
        print("Start type: " + str(type(start)))
        start.visit()
        self.toProcess.push(start)

        # Repeat until path found
        while not self.toProcess.isEmpty():
            self.parent = self.toProcess.peek()
            self.parent.visit()

            if self.parent == end:
                print("Path found")
                break
            else:
                # Add the children
                for node in self.toProcess.pop().getNeighbours():
                    if not node.isVisited():
                        node.setParent(self.parent)
                        self.toProcess.push(node)

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
