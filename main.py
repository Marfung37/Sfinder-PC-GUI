import os
import re
import json
import tkinter as tk
from tkinter import ttk
from board import Board
from saves import Saves
from solves import Solves
from percent import Percent

class GUI(tk.Tk):
    setupFile = "resources/input/field.txt"
    imagePath = "resources/output/fig.gif"

    fumenGetPages = "fumenScripts/fumenCountPages.js"
    
    # tool outputs
    saveToolOutput = "output/saveToolOutput.txt"

    # error file
    error = "output/error.txt"

    config = "config.txt"

    # queuing files
    fieldsQueue = "resources/queue/fieldsInQueue.txt"

    wantedPiecesMap = "resources/wantedPiecesMap.json"

    def __init__(self):
        super().__init__()
        self.title("Sfinder PC GUI")
        self.geometry("600x600")
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
        tabControl = ttk.Notebook(self, height=160)
        boardTab = ttk.Frame(tabControl)
        saveTab = ttk.Frame(tabControl)
        solveTab = ttk.Frame(tabControl)
        percentTab = ttk.Frame(tabControl)
        #queueTab = ttk.Frame(tabControl)

        tabControl.add(boardTab, text="Board")
        tabControl.add(saveTab, text="Save")
        tabControl.add(solveTab, text="Solve")
        tabControl.add(percentTab, text="Percent")
        #tabControl.add(queueTab, text="Queue")

        tabControl.grid(column=1, row=0, columnspan=6,rowspan=4)

        self.__setupUniversalFrame(universalFrame)
        self.__setupBoardTab(boardTab)
        self.__setupSaveTab(saveTab)
        self.__setupSolveTab(solveTab)
        self.__setupPercentTab(percentTab)
        #self.__setupQueueTab(queueTab)

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
        self.__overrideVar = tk.BooleanVar()

        self.__wantedPiecesEntry = ttk.Entry(saveTab, width=18)
        self.__pcNumEntry = ttk.Entry(saveTab, width=2)
        overrideDifferentBoard = tk.Checkbutton(saveTab, text="Override", variable=self.__overrideVar)
        runSavePieces = ttk.Button(saveTab, text="Count Wanted", command=self.__savePieces)
        runSfinderSaves = ttk.Button(saveTab, text="Make Path", command=self.__savePath)
        runFilterPath = ttk.Button(saveTab, text="Filter Path", command=self.__filterPath)
        runBestSaves = ttk.Button(saveTab, text="Best Saves", command=self.__getBestSaves)

        ttk.Label(saveTab, text="Wanted Saves").grid(column=0, row=0, sticky="e")
        ttk.Label(saveTab, text="PC Num").grid(column=0, row=1, sticky="e")
        self.__wantedPiecesEntry.grid(column=1, row=0, columnspan=4, sticky="w")
        self.__pcNumEntry.grid(column=1, row=1, sticky="w")
        overrideDifferentBoard.grid(column=2, row=1)
        runSavePieces.grid(column=0, row=2)
        runBestSaves.grid(column=1, row=2)
        runFilterPath.grid(column=2, row=2)
        runSfinderSaves.grid(column=1,row=4)
    
    def __setupSolveTab(self, solveTab):
        self.__solveKey = tk.StringVar()
        self.__solveKey.set("minimal")

        minimalRb = ttk.Radiobutton(solveTab, text="Minimal", variable=self.__solveKey, value="minimal")
        uniqueRb = ttk.Radiobutton(solveTab, text="Unique", variable=self.__solveKey, value="unique")
        runSolves = ttk.Button(solveTab, text="Run Solves", command=self.__giveSolves)
        uniqueSolvesFromPath = ttk.Button(solveTab, text="Solve From Path", command=self.__getPathUnique)
        trueMinimal = ttk.Button(solveTab, text="True Minimal", command=self.__runTrueMinimal)
        preview = ttk.Button(solveTab, text="Preview Solves", command=self.__createGif)

        minimalRb.grid(column=0, row=0)
        uniqueRb.grid(column=1, row=0)
        runSolves.grid(column=2, row=0)
        uniqueSolvesFromPath.grid(column=0, row=1)
        trueMinimal.grid(column=1, row=1)
        preview.grid(column=1, row=2)

    def __setupPercentTab(self, percentTab):
        runPercent = ttk.Button(percentTab, text="Percent", command=self.__givePercent)
        runPercent.grid(column=3, row=2)
    
    def __setupQueueTab(self, queueTab):
        queueButton = ttk.Button(queueTab, text="Queue Board and Pieces", command=self.__createQueuedOperations)
        
        queueButton.grid(column=0, row=0, columnspan=4)

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
        self.__output.insert(tk.INSERT, "Output saved")
    
    def __createQueuedOperations(self):
        self.__output.delete('1.0', tk.END)

        pieces = self.__getPieces.get()
        # pieces has characters in it
        if not pieces:
            self.__output.insert(tk.INSERT, "Pieces is empty") 
            return

        maxHeight = self.__getHeight.get()
        if not maxHeight.isnumeric():
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

        all = str(maxHeight) + readableBoardData + "\n" + pieces + "\n"

        with open(self.fieldsQueue, "a") as infile:
            infile.write(all)

        self.__output.insert(tk.INSERT, "Saved: \n")
        self.__output.insert(tk.INSERT, all)

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
        if not self.__pathRan():
            return

        configs = {
            "General Saves": False,
            "Over PC Cases": False,
            "Save Fraction": False,
            "Write Fails": False
        }
        
        self.__getFromConfig(configs)

        wantedSaves = self.__handleWantedPieces()
        if wantedSaves == "Error":
            return
        self.__saves.runSaves(wantedSaves, configs)

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
        self.__output.delete('1.0', tk.END)
        if not self.__pathRan():
            return

        wantedSaves = self.__handleWantedPieces()
        if wantedSaves == "Error":
            return

        self.__saves.filterPath(wantedSaves)

        if not self.__errorCheck():
            self.__output.insert(tk.INSERT, "Finished filter")

    def __getBestSaves(self):
        if not self.__pathRan():
            return

        configs = {
            "Over PC Cases": False,
        }
        
        self.__getFromConfig(configs)

        self.__saves.runBestSaves(self.__pcNumEntry.get(), configs)

        if not self.__errorCheck():
            self.__output.delete("1.0", tk.END)
            with open(self.__saves.savePieceOutput, "r") as outfile:
                for line in outfile:
                    self.__output.insert(tk.INSERT, line)
    
    def __pathRan(self):
        # a fail safe in case the user accidently try to run wanted pieces without making a path file for the board
        if not self.__overrideVar.get():
            pathBoard = []
            with open(self.__saves.logFile, "r") as outfile:
                outfile.readline()
                for line in outfile:
                    if re.match("[_X]", line):
                        pathBoard.append(line)
                    else:
                        break
            self.__putBoardDataIntoInput()
            with open(self.setupFile, "r") as outfile:
                indexPath = 0
                for line in outfile:
                    if re.match("[_X]", line):
                        if line.rstrip() != pathBoard[indexPath].rstrip():
                            # board doesn't match the board that made the path file
                            self.__output.delete('1.0', tk.END)
                            self.__output.insert(tk.INSERT, "The board doesn't match the board that made the path file. If you want to override this, please check the override checkbox.")
                            return False
                        indexPath += 1
                        if indexPath == len(pathBoard):
                            break
        return True

    def __handleWantedPieces(self):
        usrInput = self.__wantedPiecesEntry.get()
        if not usrInput:
            self.__output.insert(tk.INSERT, "Wanted Saves is empty") 
            return "Error"
        usrInput = usrInput.replace(" ", "")

        kwargs = re.findall("[k]=\[[^\[]*?\]|[k]=[^,]*", usrInput)
        for kwarg in kwargs:
            kwIndex = usrInput.find(kwarg[2:])
            if kwIndex != -1:
                usrInput = usrInput[:kwIndex] + usrInput[kwIndex + len(kwarg[2:]):]
        if re.search("[k]=\[", usrInput):
            # missing closing bracket
            self.__output.insert(tk.INSERT, "Wanted Saves missing closing bracket in key") 
            return "Error"
        if re.search("\],", usrInput):
            # missing opening bracket
            self.__output.insert(tk.INSERT, "Wanted Saves missing opening bracket in key") 
            return "Error"

        usrInput = usrInput.split(",")
        i = 0
        j = 0
        while j < len(kwargs):
            if usrInput[i] == kwargs[j][:2]:
                usrInput[i] = kwargs[j]
                j += 1
            i += 1

        for i, wantedSave in enumerate(usrInput):
            wantedSave = wantedSave.split("=")
        
            if wantedSave[0] == "k":
                allKeys = []
                if wantedSave[1][0] == "[" and wantedSave[1][-1] == "]":
                    allKeys = wantedSave[1][1:-1].split(",")
                else:
                    allKeys.append(wantedSave[1])

                outfile = open(self.wantedPiecesMap)
                wantedMap = json.load(outfile)
                usrInput[i] = ",".join([",".join(wantedMap[key]) for key in allKeys])

                outfile.close()
        
        wantedSaves = ",".join(usrInput)

        return wantedSaves

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

    def __getPathUnique(self):
        if not self.__pathRan():
            return
        
        self.__solves.uniqueFromPath()

        self.__output.delete('1.0', tk.END)
        with open(self.__solves.solvesOutput, "r") as outfile:
            self.__output.insert(tk.INSERT, outfile.read())

    def __runTrueMinimal(self):
        if not self.__pathRan():
            return

        self.__solves.true_minimal()

        self.__output.delete('1.0', tk.END)
        with open(self.__solves.solvesOutput, "r") as outfile:
            self.__output.insert(tk.INSERT, outfile.read())

    def __createGif(self):
        gifWin = tk.Toplevel()
        gifWin.title("Preview")

        gifLabel = tk.Label(gifWin)

        with open(self.__solves.solvesOutput, "r") as outfile:
            fumenCode = outfile.readlines()[2].rstrip()
        
        os.system(f'java -jar {self.__solves.sfinder} util fig -t {fumenCode} -c four -f no -o {self.imagePath} -lp resources/output/last_output.txt')
        
        os.system(f'node {self.fumenGetPages} {fumenCode}')

        with open(self.__solves.scripts, "r") as outfile:
            numPages = int(outfile.read().rstrip())

        imageFrames = [tk.PhotoImage(file=self.imagePath, format="gif -index %i"%(i)) for i in range(numPages)]
        
        def update(index):
            frame = imageFrames[index]
            index += 1
            if index == numPages:
                index = 0
            gifLabel.configure(image=frame)
            gifWin.after(500, update, index)
        
        gifLabel.pack()
        gifWin.after(0, update, 0)
        gifWin.mainloop()

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
                for line in outfile:
                    if re.match("[TILJSZO]+\n", line):
                        break
                    self.__output.insert(tk.INSERT, line)

    def __getFromConfig(self, keys):
        with open(self.config, "r") as outfile:
            for line in outfile:
                if line[0] != "#" and line != "\n":
                    key = re.match("(.+) =", line).groups()[0]
                    if key in keys:
                        keys[key] = bool(re.search("= True #", line))

if __name__ == "__main__":
    GUI()
