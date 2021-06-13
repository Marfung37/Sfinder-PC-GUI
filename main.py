import os
import re
import tkinter as tk
from tkinter import ttk
from board import Board
from saves import Saves
from solves import Solves
from percent import Percent

class GUI:
    setupFile = "resources/input/field.txt"
    
    # tool outputs
    saveToolOutput = "output/saveToolOutput.txt"

    def __init__(self):
        self.win = tk.Tk()
        self.__saves = Saves()
        self.__solves = Solves()
        self.__percent = Percent()

        # board canvas
        self.__board = Board(self.win)
        self.__board.grid(column=0, row=0, rowspan=5)

        # the tab controler and the different tabs
        self.__tabControl = ttk.Notebook(self.win, width=300, height=160)
        self.__boardTab = tk.Frame(self.__tabControl)
        self.__saveTab = tk.Frame(self.__tabControl)
        self.__solveTab = tk.Frame(self.__tabControl)
        self.__percentTab = tk.Frame(self.__tabControl)

        self.__tabControl.add(self.__boardTab, text="Board")
        self.__tabControl.add(self.__saveTab, text="Save")
        self.__tabControl.add(self.__solveTab, text="Solve")
        self.__tabControl.add(self.__percentTab, text="Percent")

        self.__tabControl.grid(column=1, row=0, columnspan=6,rowspan=4)

        self.__setupBoardTab()
        self.__setupSaveTab()
        self.__setupSolveTab()
        self.__setupPercentTab()

        # universal frame
        self.__universalFrame = tk.Frame(self.win)
        self.__universalFrame.grid(column=1, row=4, columnspan=6)

        self.__getPieces = tk.Entry(self.__universalFrame)
        self.__saveOutButton = tk.Button(self.__universalFrame, text="Save Output", command=self.__saveOutput)

        tk.Label(self.__universalFrame, text="Pieces").grid(column=0, row=0)
        self.__getPieces.grid(column=1, row=0)
        self.__saveOutButton.grid(column=2, row=0)

        # universal output textbox
        self.__output = tk.Text(self.win)
        self.__output.grid(column=0, row=5, columnspan=3)

        self.win.mainloop()

    def __setupBoardTab(self):
        # board tab
        clearButton = tk.Button(self.__boardTab, text="Clear Board", width=10, command=self.__board.clear)
        convertButton = tk.Button(self.__boardTab, text="Convert", width=10, command=self.__putBoardDataIntoInput)
        mirrorButton = tk.Button(self.__boardTab, text="Mirror", command=self.__board.mirrorBoard)
        
        # frame for movement of board
        self.__getHeight = tk.Entry(self.__boardTab, width=2)
        moveBoardFrame = tk.Frame(self.__boardTab)
        upButton = tk.Button(moveBoardFrame, text="^", command=lambda change=(0,1): self.__board.moveBoard(change))
        downButton = tk.Button(moveBoardFrame, text="v", command=lambda change=(0,-1): self.__board.moveBoard(change))
        rightButton = tk.Button(moveBoardFrame, text=">", command=lambda change=(1,0): self.__board.moveBoard(change))
        leftButton = tk.Button(moveBoardFrame, text="<", command=lambda change=(-1,0): self.__board.moveBoard(change))
        upButton.grid(column=1)
        downButton.grid(column=1, row=2)
        rightButton.grid(column=2, row=1)
        leftButton.grid(column=0, row=1)

        self.__getHeight.insert(0, str(self.__board.height))

        tk.Label(self.__boardTab, text="Height").grid(column=0, row=0)
        self.__getHeight.grid(column=1, row=0)
        clearButton.grid(column=5, row=0, padx=(120,0))
        mirrorButton.grid(column=5, row=1, padx=(120,0))
        convertButton.grid(column=5, row=2, padx=(120,0))
        moveBoardFrame.grid(column=0, row=1, columnspan=3, rowspan=3) 

    def __setupSaveTab(self):
        self.__wantedPiecesEntry = tk.Entry(self.__saveTab, width=18)
        runSavePieces = tk.Button(self.__saveTab, text="Count Wanted", command=self.__savePieces)
        runSfinderSaves = tk.Button(self.__saveTab, text="Make Path", command=self.__savePath)

        tk.Label(self.__saveTab, text="Wanted Piece(s)").grid(column=0, row=0)
        self.__wantedPiecesEntry.grid(column=1, row=0, columnspan=4)
        runSavePieces.grid(column=0, row=1)
        runSfinderSaves.grid(column=1,row=4)
    
    def __setupSolveTab(self):
        self.__solveKey = tk.StringVar()
        self.__solveKey.set("minimal")

        minimalRb = tk.Radiobutton(self.__solveTab, text="Minimal", variable=self.__solveKey, value="minimal")
        uniqueRb = tk.Radiobutton(self.__solveTab, text="Unique", variable=self.__solveKey, value="unique")
        runSolves = tk.Button(self.__solveTab, text="Run Solves", command=self.__giveSolves)

        minimalRb.grid(column=0, row=0)
        uniqueRb.grid(column=0, row=1)
        runSolves.grid(column=1, row=2)

    def __setupPercentTab(self):
        runPercent = tk.Button(self.__percentTab, text="Percent", command=self.__givePercent)
        runPercent.grid(column=3, row=2)

    def __putBoardDataIntoInput(self):
        maxHeight = int(self.__getHeight.get())

        readableBoardData = ""
        rawBoardData = self.__board.boardData[self.__board.NUMROW - maxHeight:]
        for row in rawBoardData:
            readableBoardData += "\n"
            for col in row:
                if col:
                    readableBoardData += "X"
                else:
                    readableBoardData += "_"
        
        with open(self.setupFile, "w") as infile:
            infile.write(str(maxHeight))
            infile.write(readableBoardData)

    def __saveOutput(self):
        with open(self.saveToolOutput, "a") as infile:
            with open(self.setupFile, "r") as outfile:
                infile.write("".join(re.findall("\n([X_\n]*)", outfile.read())) + "\n")
            infile.write(self.__saves.getFromLastOutput("  ([TILJSZOp1-7!,\[\]^*]+)")[0] + "\n")
            infile.write(self.__output.get("1.0", "end-1c").rstrip() + "\n")
    
    # make the path file for saves
    def __savePath(self):
        self.__putBoardDataIntoInput()
        self.__output.delete('1.0', tk.END)
         
        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            raise SyntaxError("Pieces is empty")
        self.__saves.runSfinderPathForSaves(pieces)
        self.__output.insert(tk.INSERT, "Finished Making Path") 

    def __savePieces(self):
        try:
            self.__saves.runSaves(self.__wantedPiecesEntry.get())

            # output the data on the gui
            self.__output.delete('1.0', tk.END)
            with open(self.__saves.savePieceOutput, "r") as outfile:
                # skip field and piece data
                for line in outfile:
                    if not line[0].isnumeric():
                        continue
                    else:
                        # chance line
                        self.__output.insert(tk.INSERT, line)
                        break
                # show the basic and wanted saves
                for line in outfile:
                    if line == "Fail Queues:\n":
                        # skip line of fail queues
                        outfile.readline()
                        continue
                    self.__output.insert(tk.INSERT, line)
        except:
            # errors
            self.__output.delete('1.0', tk.END)
            with open(self.__saves.error, "r") as outfile:
                for line in outfile:
                   self.__output.insert(tk.INSERT, line) 
        
    def __giveSolves(self):
        self.__putBoardDataIntoInput()
        self.__output.delete('1.0', tk.END)

        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            raise SyntaxError("Pieces is empty")

        self.__solves.runSolves(pieces, key=self.__solveKey.get())

        with open(self.__solves.solvesOutput, "r") as outfile:
            for line in outfile:
                self.__output.insert(tk.INSERT, line)

    def __givePercent(self):
        self.__putBoardDataIntoInput()
        self.__output.delete('1.0', tk.END)
         
        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            raise SyntaxError("Pieces is empty")

        self.__percent.runPercent(pieces)

        # output the data on the gui
        with open(self.__percent.percentOutput, "r") as outfile:
            self.__output.insert(tk.INSERT, outfile.readline())

GUI()