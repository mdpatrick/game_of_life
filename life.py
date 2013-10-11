from scanner import Scanner
from time import sleep
import os
from sys import argv

######################## RULES #######################
# A game board with a size of n*m (n rows, and m columns), represented as a matrix.
# Each entry in the game board matrix can be either 1 for living, or 0 for dead.
# Additionally, for each cell in the matrix the following rules apply:
# Any living cell with fewer than two living neighbors dies, as if caused by under-population.
# Any living cell with more than three living neighbors dies, as if caused by over-population.
# Any living cell with two or three living neighbors lives on to the next generation.
# Any dead cell with exactly three living neighbors becomes alive, as if by reproduction.
#####################################################
#matrix = [ [3, 1, 4], [1, 5, 9], [2, 6, 5] ]
#element = matrix[r][c]
#firstRow = matrix[0] # [3, 1, 4]
#value = matrix[0][1] # 1

def printMatrix(matrix):
    for i in range(0, len(matrix), 1):
      for j in range(0, len(matrix[0]), 1):
         print(matrix[i][j], end=' ')
      print("")

def buildMatrix(fname, rows, cols):
   # Construct an empty matrix with specified rows and cols
   matrix = []
   for i in range(0, rows):
       matrixCols = []
       for i in range(0, cols):
           matrixCols.append(0)
       matrix.append(matrixCols)

   # Open the file using Scanner or File Pointer
   # scanner example from http://troll.cs.ua.edu/cs150/projects/practice1.html
   if (fname):
       s = Scanner(fname)
       
       # Read the data from each row into an array
       scannedArray = []
       token = s.readtoken()
       while token != '':
           scannedArray.append(token)
           token = s.readtoken()

       # Append the array onto the matrix
       for rowNumber in range(0, len(matrix)):
           for columnNumber in range(0, len(matrix[rowNumber])):
               if (len(scannedArray) > 0):
                   matrix[rowNumber][columnNumber] = scannedArray.pop(0)

       # Close the file
       s.close()

   return matrix

def nextGeneration(mat):
    # Construct a new matrix with the same size as mat
    num_of_rows = len(mat)
    num_of_cols = len(mat[0])
    newMatrix = buildMatrix(0, num_of_rows, num_of_cols)

    # For each cell in mat, determine the number of living neighbors
    # Based on the living neighbor count update the new matrix w/ appropriate values
    for y in range(0, len(mat)):
        for x in range(0, len(mat[0])):
            numLive = numLiveNeighbors(mat, x, y)
            if (mat[y][x] == "1"):
                if ((numLive > 3) or (numLive < 2)):
                    newMatrix[y][x] = "0"
                else:
                    newMatrix[y][x] = "1"
            else:
                if (numLive == 3):
                    newMatrix[y][x] = "1"
                    
    # Return the next generation matrix
    return newMatrix

def numLiveNeighbors(matrix, j, i):
    numLive = 0

    # iterate over the rows i-1 to i+2
    if (i == 0):
        beginningRow = 0
    else:
        beginningRow = i-1
    
    if (i == (len(matrix) - 1)):
        endingRow = i
    else:
        endingRow = i+1
        
    if (j == 0):
        beginningColumn = 0
    else:
        beginningColumn = j-1

    if (j == (len(matrix[0]) - 1)):
        endingColumn = j
    else:
        endingColumn = j+1
   # iterate over the columns j-1 to j+2
     # Perform a set of checks to find living neighbors of (i,j)   
    for y in range(beginningRow, endingRow+1):
        for x in range(beginningColumn, endingColumn+1):
            if (y == i and x == j):
                continue
            if (matrix[y][x] == "1"):
                numLive += 1
    return numLive

##### This function wasn't specifically defined in instructions #####
##### however, its existence is implicitly needed               #####
def convertBoardToHashmarks(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    newMatrix = buildMatrix(0, num_rows, num_cols)

    for y in range(0, num_rows):
        for x in range(0, num_cols):
            if (matrix[y][x] == "1"):
                newMatrix[y][x] = "#"
            else:
                newMatrix[y][x] = " "

    return newMatrix

if (len(argv) < 4) or (len(argv) > 4):
    print("Please supply the appropriate number of parameters.")
    print("e.g. \"python3 life.py example.dat [num_of_rows] [num_of_cols]\"")
else:
    mat = buildMatrix(argv[1], int(argv[2]), int(argv[3]))
    while True:
        os.system('clear')
        hashedMat = convertBoardToHashmarks(mat)
        printMatrix(hashedMat)
        mat = nextGeneration(mat)
        sleep(0.5)
