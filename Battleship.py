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
        self.board = [[(0,0)] * self.cols for i in range(self.rows)]
    
    def drawBoard(self, app):
        for row in range(self.rows):
            for col in range(self.cols):
                cellWidth = self.width // self.cols
                cellHeight = self.height //self.rows
                cellLeft = self.left + cellWidth * col
                cellTop = self.top + cellHeight * row
                drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = None,
                         border = 'blue', borderWidth = self.borderWidth)

################################################################################
#################################    Grid    ###################################
################################################################################

def drawBoard(app):
    pass

def drawCell(app):
    pass

################################################################################
########################    Top (or bottom I guess)    #########################
################################################################################

def onAppStart(app):
    app.width = 1000
    app.height = 600
    app.player1Board = Board(400, 400, 10, 10)
    app.player2Board = Board(400, 400, 10, 10)
    app.player1Board.left = app.width // 4 - app.player1Board.width // 2
    app.player1Board.top = app.height - (400 + 50)
    app.player2Board.left = (3 * app.width) // 4 - app.player2Board.width // 2
    app.player2Board.top = app.height - (400 + 50)

def startGame(app):
    pass

def redrawAll(app):
    app.player1Board.drawBoard(app)
    app.player2Board.drawBoard(app)

def main():
    runApp()

main()