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
        self.board = [[(False, False)] * self.cols for i in range(self.rows)]
        # In which the tuple represents (holds ship, guessed)
    
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
        self.gridShape = [[1] * self.gridWidth] * self.gridHeight
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
        self.image = self.image.rotate(90)
        self.pixelWidth, self.pixelHeight = self.pixelHeight, self.pixelWidth
        self.pixelLeftX = board.left
        self.pixelTopY = board.top - (self.pixelHeight + 50)
        self.gridWidth, self.gridHeight = self.gridHeight, self.gridWidth
        self.gridShape = [[1] * self.Width] * self.gridHeight

################################################################################
############################    User Interaction    ############################
################################################################################

def inRect(pX, pY, x, y, width, height):
    if x <= pX <= x + width and y <= pY <= y + height:
        return True
    return False

def mousePressed(app, mouseX, mouseY):
    pass

def onMouseDrag(app, mouseX, mouseY):
    for ship in app.blueShips:
        if inRect(mouseX, mouseY, ship.pixelLeftX, ship.pixelTopY, ship.pixelWidth,
                  ship.pixelHeight) and (app.heldShip == None or ship == app.heldShip):
            app.heldShip = ship
            app.heldShip.pixelLeftX = mouseX - app.heldShip.pixelWidth // 2
            app.heldShip.pixelTopY = mouseY - app.heldShip.pixelHeight // 2

def onMouseRelease(app, mouseX, mouseY):
    app.heldShip = None

################################################################################
########################    Top (or bottom I guess)    #########################
################################################################################

def onAppStart(app):
    app.width = 1200
    app.height = 700
    app.heldShip = None
    initiateBoard(app)
    initiatePlayerShips(app)
    initiateComputerShips(app)

def initiateBoard(app):
    app.player1Board = Board(400, 400, 10, 10)
    app.player2Board = Board(400, 400, 10, 10)
    app.player1Board.left = app.width // 4 - app.player1Board.width // 2
    app.player1Board.top = app.height // 2 - app.player1Board.height // 2
    app.player2Board.left = (3 * app.width) // 4 - app.player2Board.width // 2
    app.player2Board.top = app.height // 2 - app.player2Board.height // 2

def initiatePlayerShips(app):
    app.blueShips = []
    app.blueShips.append(Ship('assets/A_destroyer_2.png', 2, app.player1Board)) # temp
    app.blueShips.append(Ship('assets/A_cruiser_3.png', 3, app.player1Board))
    app.blueShips.append(Ship('assets/A_carrier_4.png', 4, app.player1Board))
    app.blueShips.append(Ship('assets/A_battleship_5.png', 5, app.player1Board))
    for ship in range(len(app.blueShips)):
        app.blueShips[ship].pixelLeftX += (ship * app.player1Board.cellWidth)

def initiateComputerShips(app):
    app.redShips = []
    app.redShips.append(Ship('assets/B_destroyer_2.png', 2, app.player2Board)) # temp
    app.redShips.append(Ship('assets/B_cruiser_3.png', 3, app.player2Board))
    app.redShips.append(Ship('assets/B_carrier_4.png', 4, app.player2Board))
    app.redShips.append(Ship('assets/B_battleship_5.png', 5, app.player2Board))

def drawPlayerShips(app): 
    for ship in range(len(app.blueShips)):
        app.blueShips[ship].drawShip()

def redrawAll(app):
    app.player1Board.drawBoard()
    app.player2Board.drawBoard()
    drawPlayerShips(app)

def main():
    runApp()

main()