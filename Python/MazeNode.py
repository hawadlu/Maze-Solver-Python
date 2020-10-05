""""
This class is used to store information about each node in the maze.
It has fields to store...
    -x position
    -y position
    -neighbouring nodes
    -The cost of reaching the node
    -a visited/unvisited flag
    -the parent node (the node that was visited before this node).
"""


class MazeNode:
    # Create an object with parameters
    def __init__(self, x, y):
        self.xPos: int = x
        self.yPos: int = y

        # Parameters used for traversals
        self.neighbours = set()  # Neighbouring nodes
        self.parent = None
        self.visited = False
        self.cost = float('inf')

    def getX(self):
        return self.xPos

    def getY(self):
        return self.yPos

    def addNeighbour(self, neighbour):
        self.neighbours.add(neighbour)

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def getNeighbours(self):
        return self.neighbours

    def visit(self):
        self.visited = True

    def unvisit(self):
        self.visited = False

    def isVisited(self):
        if self.visited:
            return True
        else:
            return False

    def setCost(self, newCost):
        self.cost = newCost

    def getCost(self):
        return self.cost
