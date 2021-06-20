import os
import re
import tkinter as tk
from tkinter import ttk
from board import Board
from saves import Saves
from solves import Solves
from percent import Percent

class GUI(tk.Tk):
    setupFile = "resources/input/field.txt"
    
    # tool outputs
    saveToolOutput = "output/saveToolOutput.txt"

    # error file
    error = "output/error.txt"

    def __init__(self):
        super().__init__()
        self.title("Sfinder PC GUI")
        self.style = ttk.Style(self)

        self.__saves = Saves()
        self.__solves = Solves()
        self.__percent = Percent()

        self.errorNum = self.__getErrorNum()
        
        # board canvas
        self.__board = Board(self)
        self.__board.grid(column=0, row=0, rowspan=5)

        # universal frame
        universalFrame = ttk.Frame(self)
        universalFrame.grid(column=1, row=4, columnspan=6)

        # the tab controler and the different tabs
        tabControl = ttk.Notebook(self, width=300, height=160)
        boardTab = ttk.Frame(tabControl)
        saveTab = ttk.Frame(tabControl)
        solveTab = ttk.Frame(tabControl)
        percentTab = ttk.Frame(tabControl)

        tabControl.add(boardTab, text="Board")
        tabControl.add(saveTab, text="Save")
        tabControl.add(solveTab, text="Solve")
        tabControl.add(percentTab, text="Percent")

        tabControl.grid(column=1, row=0, columnspan=6,rowspan=4)

        self.__setupUniversalFrame(universalFrame)
        self.__setupBoardTab(boardTab)
        self.__setupSaveTab(saveTab)
        self.__setupSolveTab(solveTab)
        self.__setupPercentTab(percentTab)

        self.__setStyling()

        self.mainloop()
    
    def __setStyling(self):
        pass

    def __setupUniversalFrame(self, frame):
        self.__getPieces = ttk.Entry(frame)
        saveOutButton = ttk.Button(frame, text="Save Output", command=self.__saveOutput)

        ttk.Label(frame, text="Pieces").grid(column=0, row=0)
        self.__getPieces.grid(column=1, row=0)
        saveOutButton.grid(column=2, row=0)

        # universal output textbox
        self.__output = tk.Text(self)
        self.__output.grid(column=0, row=5, columnspan=3)

    def __setupBoardTab(self, boardTab):
        # board tab
        clearButton = ttk.Button(boardTab, text="Clear Board", width=10, command=self.__board.clear)
        convertButton = ttk.Button(boardTab, text="Convert", width=10, command=self.__putBoardDataIntoInput)
        mirrorButton = ttk.Button(boardTab, text="Mirror", command=self.__board.mirrorBoard)
        
        # frame for movement of board
        self.__getHeight = ttk.Entry(boardTab, width=2)
        moveBoardFrame = tk.Frame(boardTab, bg="gray92")
        upButton = tk.Button(moveBoardFrame, text="^", command=lambda change=(0,1): self.__board.moveBoard(change))
        downButton = tk.Button(moveBoardFrame, text="v", command=lambda change=(0,-1): self.__board.moveBoard(change))
        rightButton = tk.Button(moveBoardFrame, text=">", command=lambda change=(1,0): self.__board.moveBoard(change))
        leftButton = tk.Button(moveBoardFrame, text="<", command=lambda change=(-1,0): self.__board.moveBoard(change))
        upButton.grid(column=1)
        downButton.grid(column=1, row=2)
        rightButton.grid(column=2, row=1)
        leftButton.grid(column=0, row=1)

        self.__getHeight.insert(0, str(self.__board.height))

        ttk.Label(boardTab, text="Height").grid(column=0, row=0)
        self.__getHeight.grid(column=1, row=0)
        clearButton.grid(column=5, row=0, padx=(120,0))
        mirrorButton.grid(column=5, row=1, padx=(120,0))
        convertButton.grid(column=5, row=2, padx=(120,0))
        moveBoardFrame.grid(column=0, row=1, columnspan=3, rowspan=3, sticky=tk.W) 

    def __setupSaveTab(self, saveTab):
        self.__wantedPiecesEntry = ttk.Entry(saveTab, width=18)
        runSavePieces = ttk.Button(saveTab, text="Count Wanted", command=self.__savePieces)
        runSfinderSaves = ttk.Button(saveTab, text="Make Path", command=self.__savePath)
        runFilterPath = ttk.Button(saveTab, text="Filter Path", command=self.__filterPath)

        ttk.Label(saveTab, text="Wanted Saves").grid(column=0, row=0)
        self.__wantedPiecesEntry.grid(column=1, row=0, columnspan=4)
        runSavePieces.grid(column=0, row=1)
        runSfinderSaves.grid(column=1,row=4)
        runFilterPath.grid(column=1, row=1)
    
    def __setupSolveTab(self, solveTab):
        self.__solveKey = tk.StringVar()
        self.__solveKey.set("minimal")

        minimalRb = ttk.Radiobutton(solveTab, text="Minimal", variable=self.__solveKey, value="minimal")
        uniqueRb = ttk.Radiobutton(solveTab, text="Unique", variable=self.__solveKey, value="unique")
        runSolves = ttk.Button(solveTab, text="Run Solves", command=self.__giveSolves)
        trueMinimal = ttk.Button(solveTab, text="True Minimal", command=self.__runTrueMinimal)

        minimalRb.grid(column=0, row=0)
        uniqueRb.grid(column=1, row=0)
        runSolves.grid(column=2, row=0)
        trueMinimal.grid(column=0, row=1)

    def __setupPercentTab(self, percentTab):
        runPercent = ttk.Button(percentTab, text="Percent", command=self.__givePercent)
        runPercent.grid(column=3, row=2)

    def __putBoardDataIntoInput(self):
        maxHeight = self.__getHeight.get()
        if not maxHeight.isnumeric():
            self.__output.delete('1.0', tk.END)
            self.__output.insert(tk.INSERT, "Height should be a number")
            return
        maxHeight = int(maxHeight)

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
    
    def __getErrorNum(self):
        errorNum = re.findall("Error #: (\d+)", open(self.error, "r").readline())
        if errorNum:
            return int(errorNum[0])

    def __errorCheck(self):
        currErrorNum = self.__getErrorNum()
        if self.errorNum != currErrorNum:
            self.errorNum = currErrorNum

            self.__output.delete('1.0', tk.END)
            with open(self.__percent.error, "r") as outfile:
                outfile.readline()
                for line in outfile:
                   self.__output.insert(tk.INSERT, line) 
            return True
        return False

    def __saveOutput(self):
        pieces = self.__getPieces.get()
        if not pieces:
            self.__output.delete('1.0', tk.END)
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            return

        with open(self.saveToolOutput, "a") as infile:
            with open(self.setupFile, "r") as outfile:
                infile.write("".join(re.findall("\n([X_\n]*)", outfile.read())) + "\n")
            infile.write(pieces + "\n")
            infile.write(self.__output.get("1.0", "end-1c").rstrip() + "\n")
        
        # tell user it has been saved
        self.__output.insert(tk.INSEART, "Output saved")
    
    # make the path file for saves
    def __savePath(self):
        self.__putBoardDataIntoInput()
        self.__output.delete('1.0', tk.END)
         
        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            return
        self.__saves.runSfinderPathForSaves(pieces)
        if not self.__errorCheck():
            self.__output.insert(tk.INSERT, "Finished Making Path")

    def __savePieces(self):
        self.__saves.runSaves(self.__wantedPiecesEntry.get(), overPC=True)

        if not self.__errorCheck():
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
    
    def __filterPath(self):
        self.__saves.filterPath(self.__wantedPiecesEntry.get())

        if not self.__errorCheck():
            self.__output.delete('1.0', tk.END)
            self.__output.insert(tk.INSERT, "Finished filter")

    def __giveSolves(self):
        self.__putBoardDataIntoInput()
        self.__output.delete('1.0', tk.END)

        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            raise SyntaxError("Pieces is empty")

        self.__solves.runSolves(pieces, key=self.__solveKey.get())
        
        if not self.__errorCheck():
            with open(self.__solves.solvesOutput, "r") as outfile:
                for line in outfile:
                    self.__output.insert(tk.INSERT, line)

    def __runTrueMinimal(self):
        self.__solves.true_minimal()

        self.__output.delete('1.0', tk.END)
        with open(self.__solves.solvesOutput, "r") as outfile:
            self.__output.insert(tk.INSERT, outfile.read())

    def __givePercent(self):
        self.__putBoardDataIntoInput()
        self.__output.delete('1.0', tk.END)
        
        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            return

        self.__percent.runPercent(pieces)

        # output the data on the gui
        if not self.__errorCheck():
            with open(self.__percent.percentOutput, "r") as outfile:
                self.__output.insert(tk.INSERT, outfile.readline())

if __name__ == "__main__":
    GUI()