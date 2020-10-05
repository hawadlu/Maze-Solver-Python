"""
IMPORTS
"""
import os
import time

# Python imports
from PIL import Image

from AStar import AStar
from BFS import BFS
from DFS import DFS
from Dijkstra import Dijkstra
# Maze related imports
from MazeNode import MazeNode  # Import the mazenode class

"""
PREDEFINED FUNCTIONS
"""


# Loads the image into the program
def loadImage():
    print("Called load image")
    imgPath = input("Please enter the image path: ")
    print("You have entered: " + imgPath)

    # Attempt to open the image
    try:
        imgFile = Image.open(imgPath)

        # Check the colour space
        if not "RGB" in str(imgFile.info.get('icc_profile', '')):
            # Break if the user does not want to continue
            if getUserInput("The colour space of this is image not supported and may not work correctly. "
                            "Do you want to continue? y/n ") == "n":
                loadImage()

        # Load the solver method
        solve(imgFile, imgPath)

    except Exception as e:
        print("Aborted")
        print(e)

        # call the load method again
        loadImage()


"""
Takes the image and calls appropriate functions to solve it.
Also takes the image name which will be used later to solve the image
"""


def solve(imgFile, imgPath):
    global end, start, end, start, end, start, end, start
    startTime = time.time()  # Timer variable

    # Calls a method to locate all of the nodes
    nodes = findNodes(imgFile)

    # print(nodes)

    # IMAGE ALTERATION FOR TESTING
    # create the image
    newImg = Image.new("RGB", (imgFile.size[0], imgFile.size[1]), "#000000")

    # Get the image dimensions
    width, height = imgFile.size

    for i in range(height):  # Height
        for j in range(width):  # width
            if nodes[i][j] is not None and nodes[i][j] != "W":
                # Mark the node as unvisited
                nodes[i][j].unvisit()

                # Looking for neighbours
                findNeighbours(nodes[i][j], nodes, imgFile)
                if i == 0:
                    print("Start y: " + str(i) + " x: " + str(j))
                    start = nodes[i][j]
                elif i == height - 1:
                    print("end y: " + str(i) + " x: " + str(j))
                    end = nodes[i][j]

    path = []  # List of nodes in the solved path

    midTime = time.time() - startTime  # Timer variable to allow pause while the user selects an option

    algorithmName = "" # Used when saving the image

    # Picking the solve method
    answer = getUserInput("Press 1 to solve dfs: \n"
                          "Press 2 to solve BFS: \n"
                          "Press 3 to solve Dijkstra: \n"
                          "Press 4 to solve AStar: ")
    if answer == "1":
        startTime = time.time()
        dfsSearch = DFS()
        path = dfsSearch.solve(start, end)
        print("Nodes in path: " + str(dfsSearch.getPathSize()))
        algorithmName = "Depth First"
    elif answer == "2":
        startTime = time.time()
        bfsSearch = BFS()
        path = bfsSearch.solve(start, end)
        print("Nodes in path: " + str(bfsSearch.getPathSize()))
        algorithmName = "Breadth First"
    elif answer == "3":
        startTime = time.time()
        dijkstraSearch = Dijkstra()
        path = dijkstraSearch.solve(start, end)
        print("Nodes in path: " + str(dijkstraSearch.getPathSize()))
        algorithmName = "Dijkstra"
    elif answer == "4":
        startTime = time.time()
        astarSearch = AStar()
        path = astarSearch.solve(start, end)
        print("Nodes in path: " + str(astarSearch.getPathSize()))
        algorithmName = "AStar"

        # Draw the image
    newImg = drawImage(newImg, imgFile, path, width, height)

    print("Solving took: " + str((time.time() - startTime) + midTime) + "s")

    # Save the file
    saveImg(newImg, imgPath, algorithmName)


"""
Draws the image
Takes the nodes and image file as parameters
"""


def drawImage(img, oldImg, path, width, height):
    pixelsNew = img.load()
    pixelsOld = oldImg.load()

    # Draw the path between the nodes
    while len(path) > 1:
        start = path.pop()
        end = path[-1]

        # Drawing parameters

        # Set colours at the ends
        pixelsNew[start.getX(), start.getY()] = (255, 0, 0)
        pixelsNew[end.getX(), end.getY()] = (255, 0, 0)

        # Draw the path down
        if start.getY() < end.getY():
            y = start.getY()
            while y < end.getY():
                pixelsNew[start.getX(), y] = (255, 0, 0)
                y += 1
            # Drawing up
        elif start.getY() > end.getY():
            y = start.getY()
            while y > end.getY():
                pixelsNew[start.getX(), y] = (255, 0, 0)
                y -= 1

            # Drawing right
        elif start.getX() < end.getX():
            x = start.getX()
            while x < end.getX():
                pixelsNew[x, start.getY()] = (255, 0, 0)
                x += 1

            # Drawing left
        elif start.getX() > end.getX():
            x = start.getX()
            while x > end.getX():
                pixelsNew[x, start.getY()] = (255, 0, 0)
                x -= 1

    # Fill in the white squares
    for i in range(height):  # Height
        for j in range(width):  # width
            if isWhite(pixelsOld, j, i) and pixelsNew[j, i] != (255, 0, 0):
                pixelsNew[j, i] = (255, 255, 255)

    return img


"""
Saves image in a predefined location
"""


def saveImg(imgFile, imgPath, algorithmName):
    # Creating the solved directory if it does not exist
    if not os.path.isdir("Images/Solved"):
        os.mkdir("Images/Solved")

    fileName = getImageName(imgPath)

    #Splitting the file name
    fileName, fileType = fileName.split(".")[0], fileName.split(".")[1]
    imgFile.save("Images/Solved/" + fileName + "Solved " + algorithmName + "." + fileType)

    print("Image saved as: Images/Solved/" + fileName + " Solved " + algorithmName + "." + fileType)

    loadImage()


"""
Takes the image path and returns tbe image name
"""


def getImageName(imgPath):
    filePath = imgPath.split("/")
    imgPath = filePath[-1]
    print("File name: " + imgPath)
    return imgPath


"""
Takes the image and finds all the nodes
"""


def findNodes(imgFile):
    print("Entered find  nodes method")

    # create the image
    pixels = imgFile.load()

    # Get the image dimensions
    imgWidth, imgHeight = imgFile.size

    # 2d list containing the nodes. False for wall, true for path
    nodes = []

    print("Calculated dimensions " + str(imgWidth) + " " + str(imgHeight))

    # Find the nodes
    for height in range(imgHeight):
        nodes.append([])  # Make a new list
        for width in range(imgWidth):
            # Uses two different clauses to deal with different img types
            if pixels[width, height] == (255, 255, 255) or pixels[width, height] == 255:
                # Marking the start and end nodes
                if height == 0 or height == imgHeight - 1:
                    nodes[height].append(MazeNode(width, height))
                    # Mark the dead ends
                elif isDeadEnd(pixels, width, height):
                    nodes[height].append(MazeNode(width, height))
                    # mark nodes at junctions
                elif getAdjacentWhite(pixels, width, height) > 2:
                    nodes[height].append(MazeNode(width, height))
                    # Mark corner nodes
                elif getAdjacentWhite(pixels, width, height) == 2 and not directOpposite(pixels, width, height):
                    nodes[height].append(MazeNode(width, height))
                else:
                    # Flag for a white square
                    nodes[height].append("W")
            else:
                nodes[height].append(None)

            # print(pixels[width, height])

    print("Array dimensions: " + str(len(nodes)) + " " + str(len(nodes[0])))

    return nodes


"""
Takes a node and looks for its neighbours
"""


def findNeighbours(currentNode, nodes, imgFile):
    # Get the image dimensions
    imgWidth, imgHeight = imgFile.size

    # Looking down for a neighbour
    for shift in range(1, imgHeight - currentNode.getY()):
        if isNode(nodes, currentNode.getX(), currentNode.getY() + shift):
            currentNode.addNeighbour(nodes[currentNode.getY() + shift][currentNode.getX()])
            break
            # Break on a wall
        elif nodes[currentNode.getY() + shift][currentNode.getX()] is None:
            break

    # Looking up for a neighbour
    shift = 1
    while currentNode.getY() - shift > -1:
        if isNode(nodes, currentNode.getX(), currentNode.getY() - shift):
            currentNode.addNeighbour(nodes[currentNode.getY() - shift][currentNode.getX()])
            break
        elif nodes[currentNode.getY() - shift][currentNode.getX()] is None:
            break
        shift += 1

    # Looking right for a neighbour
    for shift in range(1, len(nodes[currentNode.getY()])):
        if isNode(nodes, currentNode.getX() + shift, currentNode.getY()):
            currentNode.addNeighbour(nodes[currentNode.getY()][currentNode.getX() + shift])
            break
        elif nodes[currentNode.getY()][currentNode.getX() + shift] is None:
            break

    # Looking left for a neighbour
    shift = 1
    while currentNode.getX() - shift > -1:
        if isNode(nodes, currentNode.getX() - shift, currentNode.getY()):
            currentNode.addNeighbour(nodes[currentNode.getY()][currentNode.getX() - shift])
            break
        elif nodes[currentNode.getY()][currentNode.getX() - shift] is None:
            break
        shift += 1


"""
Checks if a square contains a node
"""


def isNode(nodes, x: int, y: int):
    if nodes[y][x] is not None and nodes[y][x] != "W":
        return True
    return False


"""
Checks if a pixel is at a dead end
"""


def isDeadEnd(pixels, width, height):
    blackSides = 0

    # Look at the surrounding squares
    if not isWhite(pixels, width - 1, height):
        blackSides += 1

    if not isWhite(pixels, width + 1, height):
        blackSides += 1

    if not isWhite(pixels, width, height - 1):
        blackSides += 1

    if not isWhite(pixels, width, height + 1):
        blackSides += 1

    # print("Blacks sides for height " + str(height) + ", width " + str(width) + " = " + str(blackSides))
    return blackSides > 2


"""
Gets the number of adjacent white squares
"""


def getAdjacentWhite(pixels, width, height):
    adjacent = 0

    # Look at the surrounding squares
    if isWhite(pixels, width - 1, height):
        adjacent += 1

    if isWhite(pixels, width + 1, height):
        adjacent += 1

    if isWhite(pixels, width, height - 1):
        adjacent += 1

    if isWhite(pixels, width, height + 1):
        adjacent += 1

    return adjacent


"""
Looks for directly opposite white pixels
Return true if there are direct opposites
"""


def directOpposite(pixels, width, height):
    if (isWhite(pixels, width - 1, height) and isWhite(pixels, width + 1, height)) or (
            isWhite(pixels, width, height - 1) and isWhite(pixels, width, height + 1)):
        return True
    return False


"""
Checks if a pixel is white
"""


def isWhite(pixels, x, y):
    if pixels[x, y] == (255, 255, 255) or pixels[x, y] == 255:
        return True
    return False


def getUserInput(question):
    return input(question)


# Calls definition to load the image file
loadImage()
