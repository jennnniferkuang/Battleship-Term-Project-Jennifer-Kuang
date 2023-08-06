from cmu_graphics import *
from PIL import Image
import random

################################################################################
################################    Board    ###################################
################################################################################
   
class Board():
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.left = None # override after initialization
        self.top = None # override after initialization
        self.borderWidth = 1
        self.cellWidth = self.width // self.cols
        self.cellHeight = self.height //self.rows
        self.board = [[(0, 0)] * self.cols for i in range(self.rows)]
        # In which the tuple represents (guessed, holds ship)
    
    def drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col)
        self.drawBorder()
        self.drawCoordinateLabels()
    
    def drawCoordinateLabels(self):
        # letters on left hand side
        for row in range(self.rows):
            cellTop = self.top + self.cellHeight * row
            drawLabel(chr(ord('A') + row), self.left - 20, 
                      cellTop + self.cellHeight // 2, fill = 'blue')
        # numbers on top
        for col in range(self.cols):
            cellLeft = self.left + self.cellWidth * col
            drawLabel(col + 1, cellLeft + self.cellWidth // 2, self.top - 20,
                      fill = 'blue')
    
    def drawBorder(self):
        drawRect(self.left, self.top, self.width, self.height, fill = None, 
                 border = 'blue', borderWidth = self.borderWidth * 2)
    
    def drawCell(self, row, col):
        cellLeft = self.left + self.cellWidth * col
        cellTop = self.top + self.cellHeight * row
        drawRect(cellLeft, cellTop, self.cellWidth, self.cellHeight, 
                 fill = None, border = 'blue', borderWidth = self.borderWidth)
    
    def drawCrosshair(self, pX, pY):
        # given point x and point y, find row and column and draw a circle in
        # the respective cell.
        row, col = getCell(pX, pY, self)
        pixelMidX = (self.left + self.cellWidth * col) + self.cellWidth // 2
        pixelMidY = (self.top + self.cellHeight * row) + self.cellHeight // 2
        drawCircle(pixelMidX, pixelMidY, self.cellWidth // 3, fill = None,
                   borderWidth = 3, border = 'blue')
        drawLine(pixelMidX, pixelMidY - self.cellHeight, pixelMidX, 
                 pixelMidY + self.cellHeight, fill = 'blue', lineWidth = 3)
        drawLine(pixelMidX - self.cellWidth, pixelMidY, pixelMidX + self.cellWidth, 
                 pixelMidY, fill = 'blue', lineWidth = 3)

################################################################################
###########################    Ships and Planes    #############################
################################################################################

# Image code referenced from kirbleBirdStarter.py (lines 15, 21, 23, 40-41)
# from the Piazza note https://piazza.com/class/li3k33dc9yl37f/post/424

class Ship():
    def __init__(self, image, height, board):
        # grid info
        self.gridWidth = 1 # default
        self.gridHeight = height
        self.gridTopRow = None # override after initialization
        self.gridLeftCol = None # override after initialization
        self.gridShape = [[(0, 1)] * self.gridWidth] * self.gridHeight
        # canvas info
        self.pixelWidth = self.gridWidth * board.cellWidth
        self.pixelHeight = self.gridHeight * board.cellHeight
        self.pixelLeftX = board.left # temp
        self.pixelTopY = board.top
        # image info
        self.image = Image.open(image)
        self.image = self.image.resize((self.pixelWidth, self.pixelHeight))
    
    def drawShip(self):
        currShipImage = CMUImage(self.image)
        drawImage(currShipImage, self.pixelLeftX, self.pixelTopY)

    def rotateShip(self, board):
        # rotate method referenced from official Pillow documentation:
        # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.rotate 
        self.image = self.image.rotate(90, expand = True)
        self.pixelWidth, self.pixelHeight = self.pixelHeight, self.pixelWidth
        self.pixelLeftX = board.left
        self.pixelTopY = board.top - (self.pixelHeight + 50)
        self.gridWidth, self.gridHeight = self.gridHeight, self.gridWidth
        self.gridShape = [[1] * self.gridWidth] * self.gridHeight
        self.image = self.image.resize((self.pixelWidth, self.pixelHeight))

################################################################################
###############################    Buttons    ##################################
################################################################################

class Button():
    def __init__(self, message, midX, midY, width, height):
        self.message = message
        self.midX = midX
        self.midY = midY
        self.width = width
        self.height = height
        self.buttonColour = 'blue'
        self.textColour = 'white'
    
    def drawButton(self):
        drawRect(self.midX, self.midY, self.width, self.height, 
                 align = 'center', fill = self.buttonColour)
        drawLabel(self.message, self.midX, self.midY, 
                  fill = self.textColour, size = 16)

################################################################################
######################    Ship and Board Interaction    ########################
################################################################################

def placeShips(ships, board):
    for ship in ships:
        # get the closest row and col to the top left of the ship. Then, use the
        # ship's grid shape to increment row and col of the initial starting row
        # and col of board and set it to be the same as the ship's cell value
        firstRow, firstCol = getClosestRowCol(ship.pixelLeftX, ship.pixelTopY, board)
        for row in range(len(ship.gridShape)):
            for col in range(len(ship.gridShape[row])):
                board.board[firstRow + row][firstCol + col] = ship.gridShape[row][col]

# gets closest row, col given a point. Used to accomodate for the possibility
# that ship images may be slightly outside of the intended cells
def getClosestRowCol(pX, pY, board):
    closestCol = rounded((pX - board.left) / board.cellWidth)
    closestRow = rounded((pY - board.top) / board.cellHeight)
    return closestRow, closestCol

# gets the exact cell the point is within
def getCell(pX, pY, board):
    row = (pY - board.top) // board.cellHeight
    col = (pX - board.left) // board.cellWidth
    return row, col

################################################################################
###########################    Mouse Interaction    ############################
################################################################################

# checks if point is within a rectangle given leftX, topY, width, and height of 
# the rectangle
def inRect(pX, pY, x, y, width, height):
    if x <= pX <= x + width and y <= pY <= y + height:
        return True
    return False

def onMousePress(app, mouseX, mouseY):
    # if clicked 'confirm placement' button, place all ships and start game
    if inRect(mouseX, mouseY, app.confirmButton.midX - app.confirmButton.width // 2,
              app.confirmButton.midY - app.confirmButton.height // 2, 
              app.confirmButton.width, app.confirmButton.height):
        placeShips(app.blueShips, app.player1Board)
        placeShips(app.redShips, app.player2Board)
        app.gameStarted = True
    # player guesses cell
    elif app.gameStarted and app.playerTurn:
        hitRow, hitCol = getCell(mouseX, mouseY, app.player2Board)
        # if cell has not been guessed and contains ship
        if app.player2Board.board[hitRow][hitCol] == (0, 1):
            app.player2Board.board[hitRow][hitCol] = (1, 1)
            # update computer ship state
        # if cell has not been guessed and does not contain ship
        elif app.player2Board.board[hitRow][hitCol] == (0, 0):
            app.player2Board.board[hitRow][hitCol] = (1, 0)
        # if cell has already been guessed, just ignore
        app.playerTurn = False
        print(app.player2Board.board)

def onMouseDrag(app, mouseX, mouseY):
    if not app.gameStarted:
        # pick up ship is no ship is currently being held and the position is
        # within the new ship
        for ship in app.blueShips:
            if (app.heldShip == None or ship == app.heldShip) and inRect(mouseX, 
                mouseY, ship.pixelLeftX, ship.pixelTopY, ship.pixelWidth, ship.pixelHeight):
                app.heldShip = ship
        # constantly update ship location if a ship is being held
        if app.heldShip != None:
            app.heldShip.pixelLeftX = mouseX - app.heldShip.pixelWidth // 2
            app.heldShip.pixelTopY = mouseY - app.heldShip.pixelHeight // 2

def onMouseRelease(app, mouseX, mouseY):
    # release held ships, can pick up new ship after release
    app.heldShip = None

def onMouseMove(app, mouseX, mouseY):
    # update global app mouse pos variables for use by: aim scope tracking
    app.mousePosX, app.mousePosY = mouseX, mouseY

################################################################################
############################    Initialization    ##############################
################################################################################

def onAppStart(app):
    app.width = 1200
    app.height = 700
    app.heldShip = None
    app.gameStarted = False
    app.playerTurn = True
    app.mousePosX = 0
    app.mousePosY = 0
    app.message = 'BATTLESHIP'
    initiateBoard(app)
    initiatePlayerShips(app)
    initiateComputerShips(app)
    initiateButtons(app)

def initiateBoard(app):
    app.player1Board = Board(400, 400, 10, 10)
    app.player2Board = Board(400, 400, 10, 10)
    # player 1 board aligned to middle of left half and middle of height
    app.player1Board.left = app.width // 4 - app.player1Board.width // 2
    app.player1Board.top = app.height // 2 - app.player1Board.height // 2
    # player 2 board aligned to middle of right half and middle of height
    app.player2Board.left = (3 * app.width) // 4 - app.player2Board.width // 2
    app.player2Board.top = app.height // 2 - app.player2Board.height // 2

def initiatePlayerShips(app):
    app.blueShips = []
    # the following images are illustrated by my friend @gawain_draws on
    # Instagram for a commission. All drawings are paid for and I have explicit 
    # permission from him to use these illustrations for this project.
    app.blueShips.append(Ship('assets/A_destroyer_2.png', 2, app.player1Board)) # temp
    app.blueShips.append(Ship('assets/A_cruiser_3.png', 3, app.player1Board))
    app.blueShips.append(Ship('assets/A_carrier_4.png', 4, app.player1Board))
    app.blueShips.append(Ship('assets/A_battleship_5.png', 5, app.player1Board))
    # initialize stating position (from left to right)
    for ship in range(len(app.blueShips)):
        app.blueShips[ship].pixelLeftX += (ship * app.player1Board.cellWidth)

def initiateComputerShips(app):
    app.redShips = []
    # the following images are illustrated by my friend @gawain_draws on
    # Instagram for a commission. All drawings are paid for and I have explicit 
    # permission from him to use these illustrations for this project.
    app.redShips.append(Ship('assets/B_destroyer_2.png', 2, app.player2Board)) # temp
    app.redShips.append(Ship('assets/B_cruiser_3.png', 3, app.player2Board))
    app.redShips.append(Ship('assets/B_carrier_4.png', 4, app.player2Board))
    app.redShips.append(Ship('assets/B_battleship_5.png', 5, app.player2Board))
    # randomly generate a pixel location for each ship (temp)
    for ship in app.redShips:
        maxX = app.player2Board.left + app.player2Board.width - ship.pixelWidth
        maxY = app.player2Board.top + app.player2Board.height - ship.pixelHeight
        ship.leftX = random.randint(app.player2Board.left, maxX)
        ship.topY = random.randint(app.player2Board.top, maxY)

def initiateButtons(app):
    # 'confirm placement' button
    confirmButtonX = app.player1Board.left + (app.player1Board.width // 2)
    confirmButtonY = app.player1Board.top + app.player1Board.height + 50
    app.confirmButton = Button('confirm placement', confirmButtonX, 
                                confirmButtonY, 200, 50)

################################################################################
##################################    Draw    ##################################
################################################################################

# using the list of player ships, draw them on the board
def drawPlayerShips(app): 
    for ship in range(len(app.blueShips)):
        app.blueShips[ship].drawShip() # temp

def drawMessageBox(app):
    drawRect(app.width // 4, 25, app.width // 2, 75, fill = None, border = 'blue') # temp 25 and 75
    messageBoxMiddleY = 25 + (75 // 2)
    drawLabel(app.message, app.width // 2, messageBoxMiddleY, size = 25, fill = 'blue')

def redrawAll(app):
    # draw player and computer boards
    app.player1Board.drawBoard()
    app.player2Board.drawBoard()
    # draw player ships (computer boards hidden for now)
    drawPlayerShips(app)
    # draw message box
    drawMessageBox(app)
    # if game has not started yet, draw confirm placement button
    if not app.gameStarted:
        app.confirmButton.drawButton()
    # if the game is started and the mouse is within the computer's board,
    # draw the crosshair to select a cell to fire at.
    rightBound = app.player2Board.left + app.player2Board.width
    bottomBound = app.player2Board.top + app.player2Board.height
    if (app.playerTurn and app.gameStarted and app.player2Board.left <= app.mousePosX 
        <= rightBound and app.player2Board.top <= app.mousePosY <= bottomBound):
        app.player2Board.drawCrosshair(app.mousePosX, app.mousePosY)

def main():
    runApp()

main()