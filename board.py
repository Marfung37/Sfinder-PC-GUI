import re
import tkinter as tk

class Board(tk.Canvas):
    NUMCOL = 10
    NUMROW = 12
    SCL = 20
    BGCOLOR = "gray23"
    COLOR = "gray56"

    fieldFile = "resources/input/field.txt"

    def __init__(self, master):
        super().__init__(master, width=self.NUMCOL * self.SCL, height=self.NUMROW * self.SCL, bg=self.BGCOLOR)

        self.boardData = [[False for col in range(self.NUMCOL)] for row in range(self.NUMROW)]
        self.height = 0
        self.__getFromFile()

        self.stateChange = True
        self.color = {
            True: self.COLOR,
            False: self.BGCOLOR
        }

        self.__makeGrid()
        self.redraw()

        self.bind("<Button-1>", self.__getStateMouse)
        self.bind("<B1-Motion>", self.__drawBox)
    
    def __getFromFile(self):
        with open(self.fieldFile, "r") as outfile:
            # look for line with height (usually first line)
            for line in outfile:
                data = re.findall("(^\d+)\n$", line)
                if data:
                    self.height = int(data[0])
                    break

            # read rest of lines into board
            row = 0
            for line in outfile:
                if line[0] == "_" or line[0] == "X":
                    self.boardData[self.NUMROW - self.height + row] = [char == "X" for char in line.rstrip()]
                    row += 1  
    
    def __getStateMouse(self, event):
        if self.__inBoard(event.x, event.y):
            x = event.x // self.SCL
            y = event.y // self.SCL
                
            self.stateChange = not self.boardData[y][x]

            self.boardData[y][x] = self.stateChange

            self.create_rectangle(x * self.SCL, y * self.SCL, (x + 1) * self.SCL, (y + 1) * self.SCL, fill=self.color[self.stateChange])

    def __drawBox(self, event):
        if self.__inBoard(event.x, event.y):
            x = event.x // self.SCL
            y = event.y // self.SCL
            
            self.boardData[y][x] = self.stateChange

            self.create_rectangle(x * self.SCL, y * self.SCL, (x + 1) * self.SCL, (y + 1) * self.SCL, fill=self.color[self.stateChange])

    def __inBoard(self, x, y):
        return 0 < x < self.NUMCOL * self.SCL and 0 < y < self.NUMROW * self.SCL

    def __makeGrid(self):
        for col in range(self.NUMCOL):
            for row in range(self.NUMROW):
                self.create_rectangle(col * self.SCL, row * self.SCL, (col + 1) * self.SCL, (row + 1) * self.SCL, fill=self.BGCOLOR)

    def mirrorBoard(self):
        for rowNum in range(len(self.boardData)):
            self.boardData[rowNum] = self.boardData[rowNum][::-1]
        self.redraw()

    # @param change is tuple with (changeX, changeY)
    def moveBoard(self, change):
        for rowNum in range(len(self.boardData)):
            if change[0] == 1:
                self.boardData[rowNum] = [False] + self.boardData[rowNum][:-change[0]]
            elif change[0] == -1:
                self.boardData[rowNum] = self.boardData[rowNum][-change[0]:] + [False]
            
        if change[1] == 1:
            self.boardData.pop(0)
            self.boardData.append([False for col in range(self.NUMCOL)])
        elif change[1] == -1:
            self.boardData.pop()
            self.boardData.insert(0, [False for col in range(self.NUMCOL)])
        self.redraw()

    def clear(self):
        self.boardData = [[False for j in range(self.NUMCOL)] for i in range(self.NUMROW)]
        self.create_rectangle(0, 0, self.NUMCOL * self.SCL, self.NUMROW * self.SCL, fill=self.BGCOLOR)
        self.redraw()

    def redraw(self):
        for col in range(self.NUMCOL):
            for row in range(self.NUMROW):
                self.create_rectangle(col * self.SCL, row * self.SCL, (col + 1) * self.SCL, (row + 1) * self.SCL, fill=self.color[self.boardData[row][col]])