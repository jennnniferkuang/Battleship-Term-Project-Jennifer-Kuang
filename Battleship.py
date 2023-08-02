from cmu_graphics import *

################################################################################
###############################    Classes    ##################################
################################################################################

class Ship():
    def __init__(self):
        pass
    
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
        self.board = [[(0,0)] * self.cols for i in range(self.rows)]
    
    def drawBoard(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.drawCell(row, col)
        self.drawBorder()
        self.drawCoordinateLabels()
    
    def drawCoordinateLabels(self):
        for row in range(self.rows):
            cellTop = self.top + self.cellHeight * row
            drawLabel(chr(ord('A') + row), self.left - 20, 
                      cellTop + self.cellHeight // 2, fill = 'blue')
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
    app.player1Board = Board(400, 400, 10, 10)
    app.player2Board = Board(400, 400, 10, 10)
    app.player1Board.left = app.width // 4 - app.player1Board.width // 2
    app.player1Board.top = app.height - (400 + 50)
    app.player2Board.left = (3 * app.width) // 4 - app.player2Board.width // 2
    app.player2Board.top = app.height - (400 + 50)

def startGame(app):
    pass

def redrawAll(app):
    app.player1Board.drawBoard()
    app.player2Board.drawBoard()

def main():
    runApp()

main()