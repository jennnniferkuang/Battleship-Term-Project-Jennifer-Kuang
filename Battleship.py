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
        self.board = [[[0, 0] for i in range(self.cols)] for j in range(self.rows)]
        # In which the 3rd list represents [guessed, holds ship]
    
    def drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col)
                if self.board[row][col][0] == 1 and self.board[row][col][1] != 1:
                    self.drawStatus(row, col)
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
    
    def drawStatus(self, row, col):
        pX = self.left + self.cellWidth * col + self.cellWidth // 2
        pY = self.top + self.cellHeight * row + self.cellHeight // 2
        drawCircle(pX, pY, self.cellWidth // 4, fill = 'blue') # temp colour
    
    def drawCrosshair(self, pX, pY):
        # given point x and point y, find row and column and draw a circle in
        # the respective cell.
        row, col = pixelToRowCol(pX, pY, self)
        pixelX, pixelY = rowColToPixel(row, col, self)
        pixelX += self.cellWidth // 2
        pixelY += self.cellHeight // 2
        drawCircle(pixelX, pixelY, self.cellWidth // 3, fill = None,
                   borderWidth = 3, border = 'blue')
        drawLine(pixelX, pixelY - self.cellHeight, pixelX, 
                 pixelY + self.cellHeight, fill = 'blue', lineWidth = 3)
        drawLine(pixelX - self.cellWidth, pixelY, pixelX + self.cellWidth, 
                 pixelY, fill = 'blue', lineWidth = 3)

    def reset(self):
        self.board = [[[0, 0] for i in range(self.cols)] for j in range(self.rows)]

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
        self.gridShape = [[[0, 1]] for i in range(self.gridWidth) for j in range(self.gridHeight)]
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

    def rotateShip(self):
        # rotate method referenced from official Pillow documentation:
        # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.rotate 
        self.image = self.image.rotate(90, expand = True)
        self.pixelWidth, self.pixelHeight = self.pixelHeight, self.pixelWidth
        # self.pixelLeftX = board.left
        # self.pixelTopY = board.top - (self.pixelHeight + 50)
        self.gridWidth, self.gridHeight = self.gridHeight, self.gridWidth
        self.gridShape = [[[0, 1] for i in range(self.gridWidth)] for j in range (self.gridHeight)]
        self.image = self.image.resize((self.pixelWidth, self.pixelHeight))
    
    def placeShip(self, board):
        # get the closest row and col to the top left of the ship. Then, use the
        # ship's grid shape to increment row and col of the initial starting row
        # and col of board and set it to be the same as the ship's cell value
        firstRow, firstCol = pixelToRowCol(self.pixelLeftX, self.pixelTopY, board)
        for row in range(len(self.gridShape)):
            for col in range(len(self.gridShape[row])):
                board.board[firstRow + row][firstCol + col] = self.gridShape[row][col]

    def snapToClosestRowCol(self, board):
        closestRow, closestCol = pixelToRowCol(self.pixelLeftX, self.pixelTopY, board)
        self.pixelLeftX = board.left + closestCol * board.cellWidth
        self.pixelTopY = board.top + closestRow * board.cellHeight

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

def pixelToRowCol(pX, pY, board, getClosest = False):
    # get closest to accomodate for ships being placed slightly outside the 
    # intended cell
    if getClosest == True:
        closestCol = rounded((pX - board.left) / board.cellWidth)
        closestRow = rounded((pY - board.top) / board.cellHeight)
        return closestRow, closestCol
    # if no need for accomodation, strictly get the cell the point is within
    row = (pY - board.top) // board.cellHeight
    col = (pX - board.left) // board.cellWidth
    return row, col

def rowColToPixel(row, col, board):
    pixelX = board.left + (col * board.cellWidth)
    pixelY = board.top + (row * board.cellHeight)
    return pixelX, pixelY

def isLegal(firstRow, firstCol, shipShape, board):
    for row in range(len(shipShape)):
            for col in range(len(shipShape[row])):
                if (firstRow + row >= len(board.board) or firstCol + col >=
                    len(board.board[row])):
                    return False
                if board.board[firstRow + row][firstCol + col][1] == 1:
                    return False
    return True

def checkForSunkShips(app, ships, sunkShips):
    for ship in ships:
        sunk = True
        for row in ship.gridShape:
            if [0, 1] in row:
                sunk = False
        if sunk:
            sunkShips.add(ship)
    if len(sunkShips) == 4:
        app.gameOver = True
        if ships == app.redShips:
            app.winner = 'Player'
        else:
            app.winner = 'Computer'
        app.message = f'GAME OVER! Winner: {app.winner}'

################################################################################
###########################    Computer Player    ##############################
################################################################################

def computerPlaceShips(app):
    # for each ship, randomize whether to rotate or not. Randomize a row, col
    # and check if the whole ship a) fits on the board and b) is not overlapping
    # with another ship. If legal, place on board and set the pixel location.
    for ship in app.redShips:
        rotate = random.randint(0, 1)
        if rotate == 1:
            ship.rotateShip()
        ship.gridTopRow = random.randint(0, 9) # temp
        ship.gridLeftCol = random.randint(0, 9)
        while not isLegal(ship.gridTopRow, ship.gridLeftCol, 
                               ship.gridShape, app.computerBoard):
            ship.gridTopRow = random.randint(0, 9) # temp
            ship.gridLeftCol = random.randint(0, 9)
        ship.pixelLeftX, ship.pixelTopY = rowColToPixel(ship.gridTopRow,
                                                            ship.gridLeftCol,
                                                            app.computerBoard)
        ship.placeShip(app.computerBoard)

# app.direction
# app.prevHit
# app.initialHit
# what if there are ships side by side check if ship in that shape is sunk
# app.currHitShipShape
# app.sunkShips1
# app.sunkShips2
def computerGuess(app):
    guessRow = random.randint(0, 9) # temp
    guessCol = random.randint(0, 9)
    while app.playerBoard.board[guessRow][guessCol][0] == 1:
        guessRow = random.randint(0, 9) # temp
        guessCol = random.randint(0, 9)
    app.playerBoard.board[guessRow][guessCol][0] = 1
    # check if all cells of ship are guessed. If so, add to set of hit ships
    checkForSunkShips(app, app.blueShips, app.playerSunkShips)
    app.playerTurn = True

################################################################################
#######################   Helper Mouse Interaction    ##########################
################################################################################

# if clicked 'confirm placement' button, place all ships and start game
def pressedConfirm(app, mouseX, mouseY):
    if inRect(mouseX, mouseY, app.confirmButton.midX - app.confirmButton.width // 2,
              app.confirmButton.midY - app.confirmButton.height // 2, 
              app.confirmButton.width, app.confirmButton.height):
        legalPlacement = True
        for ship in app.blueShips:
            ship.gridTopRow, ship.gridLeftCol = pixelToRowCol(ship.pixelLeftX, ship.pixelTopY,
                                                              app.playerBoard, True)
            if isLegal(ship.gridTopRow, ship.gridLeftCol, ship.gridShape, app.playerBoard):
                ship.placeShip(app.playerBoard)
            else:
                app.message = 'ILLEGAL PLACEMENT'
                legalPlacement = False
        if legalPlacement:
            computerPlaceShips(app)
            app.gameStarted = True
            app.message = 'YOUR TURN'
        else:
            app.playerBoard.reset()
    # player guesses cell

def pressedRotate(app, mouseX, mouseY):
    if (inRect(mouseX, mouseY, app.rotateButton.midX - app.rotateButton.width // 2,
               app.rotateButton.midY - app.rotateButton.height // 2, app.rotateButton.width, 
               app.rotateButton.height) and app.prevHeldShip != None):
        app.prevHeldShip.rotateShip()

def playerGuess(app, mouseX, mouseY):
    if (app.playerTurn and inRect(mouseX, mouseY, app.computerBoard.left, 
        app.computerBoard.top, app.computerBoard.width, app.computerBoard.height)):
        hitRow, hitCol = pixelToRowCol(mouseX, mouseY, app.computerBoard)
        # set first value of status list to 1
        if app.computerBoard.board[hitRow][hitCol][0] != 1:
            app.computerBoard.board[hitRow][hitCol][0] = 1
            app.playerTurn = False
            # check if all cells of ship are guessed. If so, add to set of hit ships
            checkForSunkShips(app, app.redShips, app.computerSunkShips)
            computerGuess(app) # temp, make longer wait time

def shipDrag(app, mouseX, mouseY):
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

# checks if point is within a rectangle given leftX, topY, width, and height of 
# the rectangle
def inRect(pX, pY, x, y, width, height):
    if x <= pX <= x + width and y <= pY <= y + height:
        return True
    return False

################################################################################
#########################   Top Mouse Interaction    ###########################
################################################################################

def onMouseDrag(app, mouseX, mouseY):
    if not app.gameStarted:
        shipDrag(app, mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if not app.gameStarted:
            pressedConfirm(app, mouseX, mouseY)
            pressedRotate(app, mouseX, mouseY)
        if app.gameStarted:
            playerGuess(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if not app.gameOver:
        # release held ships, can pick up new ship after release
        if app.heldShip != None:
            app.prevHeldShip = app.heldShip
            app.heldShip.snapToClosestRowCol(app.playerBoard)
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
    app.prevHeldShip = None
    app.gameStarted = False
    app.gameOver = False
    app.playerTurn = True
    app.mousePosX = 0
    app.mousePosY = 0
    app.message = 'BATTLESHIP'
    app.playerSunkShips = set()
    app.computerSunkShips = set()
    initializeBoard(app)
    initializePlayerShips(app)
    initializeComputerShips(app)
    initializeButtons(app)
    initializeHitShipImage(app)

def initializeBoard(app):
    app.playerBoard = Board(400, 400, 10, 10)
    app.computerBoard = Board(400, 400, 10, 10)
    # player 1 board aligned to middle of left half and middle of height
    app.playerBoard.left = app.width // 4 - app.playerBoard.width // 2
    app.playerBoard.top = app.height // 2 - app.playerBoard.height // 2
    # player 2 board aligned to middle of right half and middle of height
    app.computerBoard.left = (3 * app.width) // 4 - app.computerBoard.width // 2
    app.computerBoard.top = app.height // 2 - app.computerBoard.height // 2

def initializePlayerShips(app):
    app.blueShips = []
    # the following images are illustrated by my friend @gawain_draws on
    # Instagram for my commission. All drawings are paid for and I have explicit 
    # permission from him to use these illustrations for this project.
    app.blueShips.append(Ship('assets/A_destroyer_2.png', 2, app.playerBoard)) # temp
    app.blueShips.append(Ship('assets/A_cruiser_3.png', 3, app.playerBoard))
    app.blueShips.append(Ship('assets/A_carrier_4.png', 4, app.playerBoard))
    app.blueShips.append(Ship('assets/A_battleship_5.png', 5, app.playerBoard))
    # initialize stating position (from left to right)
    for ship in range(len(app.blueShips)):
        app.blueShips[ship].pixelLeftX += (ship * app.playerBoard.cellWidth)

def initializeComputerShips(app):
    app.redShips = []
    # the following images are illustrated by my friend @gawain_draws on
    # Instagram for my commission. All drawings are paid for and I have explicit 
    # permission from him to use these illustrations for this project.
    app.redShips.append(Ship('assets/B_destroyer_2.png', 2, app.computerBoard)) # temp
    app.redShips.append(Ship('assets/B_cruiser_3.png', 3, app.computerBoard))
    app.redShips.append(Ship('assets/B_carrier_4.png', 4, app.computerBoard))
    app.redShips.append(Ship('assets/B_battleship_5.png', 5, app.computerBoard))

def initializeHitShipImage(app):
    # image is the collision symbol emoji from Apple. I typed it in on my Ipad's
    # drawing application and exported the transparent background png.
    app.hitShip = Image.open('assets/hit-ship.png')
    app.hitShip = app.hitShip.resize((app.playerBoard.cellWidth, app.playerBoard.cellHeight))
    app.hitShip = CMUImage(app.hitShip)

def initializeButtons(app):
    # 'confirm placement' button
    confirmButtonX = app.playerBoard.left + (app.playerBoard.width // 2)
    confirmButtonY = app.playerBoard.top + app.playerBoard.height + 45
    app.confirmButton = Button('confirm placement', confirmButtonX, 
                                confirmButtonY, 200, 50)
    # 'rotate ship' button
    app.rotateButton = Button('rotate ship', confirmButtonX, confirmButtonY + 65,
                              200, 50)

################################################################################
##################################    Draw    ##################################
################################################################################

# using the list of player ships, draw them on the board
def drawShips(ships): 
    for ship in ships:
        ship.drawShip() # temp

def drawHitCells(app, board):
    for row in range(board.rows):
        for col in range(board.cols):
            if board.board[row][col] == [1, 1]:
                pixelX, pixelY = rowColToPixel(row, col, board)
                drawImage(app.hitShip, pixelX, pixelY)

def drawSunkComputerShips(app):
    for ship in app.computerSunkShips:
        ship.drawShip()

# draw message/status box in top middle of board
def drawMessageBox(app):
    drawRect(app.width // 4, 25, app.width // 2, 75, fill = None, border = 'blue') # temp 25 and 75
    messageBoxMiddleY = 25 + (75 // 2)
    drawLabel(app.message, app.width // 2, messageBoxMiddleY, size = 25, fill = 'blue')

def drawCrosshair(app):
    # the mouse is within the computer's board, draw the crosshair to select a 
    # cell to fire at.
    rightBound = app.computerBoard.left + app.computerBoard.width
    bottomBound = app.computerBoard.top + app.computerBoard.height
    if (app.computerBoard.left <= app.mousePosX <= rightBound and 
        app.computerBoard.top <= app.mousePosY <= bottomBound):
        app.computerBoard.drawCrosshair(app.mousePosX, app.mousePosY)

################################################################################
######################   Tippity Toppest Top Level   ###########################
################################################################################

def redrawAll(app):
    app.playerBoard.drawBoard()
    app.computerBoard.drawBoard()
    drawShips(app.blueShips)
    drawSunkComputerShips(app)
    drawHitCells(app, app.playerBoard)
    drawHitCells(app, app.computerBoard)
    drawMessageBox(app)
    # if game has not started yet
    if not app.gameStarted:
        app.confirmButton.drawButton()
        app.rotateButton.drawButton()
    # if the game is started
    if app.playerTurn and app.gameStarted and not app.gameOver:
        drawCrosshair(app)

def main():
    runApp()

main()