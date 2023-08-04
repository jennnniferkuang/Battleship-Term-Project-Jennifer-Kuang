from cmu_graphics import *
from PIL import Image

################################################################################
################################    Board    ###################################
################################################################################
   
class Board():
    def __init__(self, width, height, rows, cols):
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.left = None
        self.top = None
        self.borderWidth = 1
        self.cellWidth = self.width // self.cols
        self.cellHeight = self.height //self.rows
        self.board = [[(0, 0)] * self.cols for i in range(self.rows)]
        # In which the tuple represents (holds ship, guessed) and 0 represents
        # false and 1 represents true
    
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

class Ship():
    def __init__(self, image, width, cellWidth, cellHeight):
        self.image = Image.open(image)
        self.width = width
        self.height = 1
        self.imageLength = self.width * cellHeight
        self.imageWidth = self.height * cellWidth
        self.gridShape = [[1] * self.width] * self.height
        self.leftCol = None
        self.topRow = None
    
    def drawShip(self):
        self.image = self.image.resize((50, 200)) # temp literal
        self.image = CMUImage(self.image)
        drawImage(self.image, 200, 400) # temp literal
    
    def rotateShip(self):
        self.gridShape = [[1] * self.height] * self.width
        self.imageLength, self.imageWidth = self.imageWidth, self.imageLength
        self.width, self.height = self.height, self.width

class Plane(Ship):
    def __init__(self, image, width, cellWidth, cellHeight):
        super().__init__(image, width, cellWidth, cellHeight)
        self.height = 3
        

################################################################################
############################    User Interaction    ############################
################################################################################

def mousePressed(app, mouseX, mouseY):
    pass

def mouseDrag(app, mouseX, mouseY):
    pass

def mouseReleased(app, mouseX, mouseY):
    pass

################################################################################
########################    Top (or bottom I guess)    #########################
################################################################################

def onAppStart(app):
    app.width = 1200
    app.height = 700
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
    app.blueShips.append(Ship('assets/A_destroyer_2.png', 2, 40, 40)) # temp
    app.blueShips.append(Ship('assets/A_cruiser_3.png', 3, 40, 40))
    app.blueShips.append(Ship('assets/A_carrier_4.png', 4, 40, 40))
    app.blueShips.append(Ship('assets/A_battleship_5.png', 5, 40, 40))

def initiateComputerShips(app):
    app.redShips = []
    app.redShips.append(Ship('assets/B_destroyer_2.png', 2, 40, 40)) # temp
    app.redShips.append(Ship('assets/B_cruiser_3.png', 3, 40, 40))
    app.redShips.append(Ship('assets/B_carrier_4.png', 4, 40, 40))
    app.redShips.append(Ship('assets/B_battleship_5.png', 5, 40, 40))

def redrawAll(app):
    app.player1Board.drawBoard()
    app.player2Board.drawBoard()

def main():
    runApp()

main()