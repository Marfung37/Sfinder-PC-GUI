from utilities import Utility
import os
import re

class Saves(Utility):
    # constants
    PIECES = ["T", "I", "L", "J", "S", "Z", "O"]

    logFile = "resources/output/savesLastOutput.txt"

    fumenLabels = "fumenScripts/fumenLabels.js"
    scripts = "fumenScripts/scriptsOutput.txt"
    
    def runSaves(self, wantedSaves, writeFails=True, overPC=False):
        if not self.checkFileExist(self.logFile):
            self.takeError("FileError", "The log file for saves doesn't exist. May be due to sfinder error when running path prior.")
            return

        # store the chance and the total cases of the setup
        chanceData = self.getFromLastOutput("  -> success = (\d+.\d{2}% \(\d+\/\d+\))", self.logFile)[0]
        if overPC:
            totalCases = int(re.findall("\((\d+)/", chanceData)[0])
        else:
            totalCases = int(re.findall("/(\d+)[)]", chanceData)[0])

        # empty savePieceOutput
        infile = open(self.savePieceOutput, "w")
        field = self.getFromLastOutput("[_X]+", self.logFile, re.MULTILINE)
        infile.write("\n".join(field) + "\n")
        pieces = self.getFromLastOutput("  ([TILJSZOp1-7!,\[\]^*]+)", self.logFile)
        if pieces:
            pieces = pieces[0]
        infile.write(pieces + "\n")
        infile.write(chanceData + "\n")

        infile.write("\nBasic Saves:\n")
        basicStats = self.numberOfWantedSaves("T,TT,I,II,L,LL,J,JJ,S,SS,Z,ZZ,O,OO")
        for p in self.PIECES:
            count1 = basicStats[p]
            percent1 = count1 / totalCases * 100
            count2 = basicStats[p*2]
            percent2 = count2 / totalCases * 100
            infile.write(f'{p}: {percent1:.2f}% ({count1}/{totalCases}) ')
            infile.write(f'{p*2}: {percent2:.2f}% ({count2}/{totalCases})\n')

        infile.write("\nWanted Saves:\n")

        wantedOutput = self.numberOfWantedSaves(wantedSaves, writeFile=infile, writeFails=writeFails, totalCases=totalCases)
        
        infile.close()

    # return an dictionary including all the wantedSaves over the path file
    def numberOfWantedSaves(self, wantedSaves, writeFile=None, writeFails=True, totalCases=0):
        countWanted = {}
        wantedSavesFails = {}
        wantedStacks = []
        allBool = False

        for wantedSave in wantedSaves.split(","):
            if wantedSave == "all":
                allBool = True
                countAll = {}
                continue
            countWanted[wantedSave] = 0
            wantedStacks.append(self.__makeStack(wantedSave))

        pieces = self.getFromLastOutput("  ([TILJSZOp1-7!,\[\]^*]+)", self.logFile)[0]
        # from pieces get the pieces given for the possible pieces in the last bag of the pc and it's length
        lastBag, newBagNumUsed = self.__findLastBag(pieces)

        with open(self.pathFile, "r") as outfile:
            outfile.readline()
            for line in outfile:
                line = line.split(",")
                bagSavePieces = lastBag - set(line[0][-newBagNumUsed:])
                savePieces = set(line[3].strip().split(";"))
                if '' in savePieces:
                    savePieces = set()
                
                isSolveable = line[1] != "0"
                if not isSolveable:
                    continue
                allSaves = self.__createAllSavesQ(savePieces, bagSavePieces)
                if allSaves:
                    if allBool:
                        for save in allSaves:
                            if save in countAll:
                                countAll[save] += 1
                            else:
                                countAll[save] = 1

                    for stack, wantedSave in zip(wantedStacks, countWanted):
                        if(self.parseStack(allSaves, stack)):
                            countWanted[wantedSave] += 1
                        else:
                            if writeFails:
                                if wantedSave not in wantedSavesFails:
                                    wantedSavesFails[wantedSave] = [line[0]]
                                else:
                                    wantedSavesFails[wantedSave].append(line[0])

            if writeFile:
                for key, value in countWanted.items():
                    if totalCases:
                        percent = value / totalCases * 100
                        writeFile.write(f'{key}: {percent:.2f}% ({value}/{totalCases})\n')
                    else:
                        writeFile.write(f'{key}: {value}\n')
                    if writeFails and wantedSave in wantedSavesFails:
                        writeFile.write("Fail Queues:\n")
                        writeFile.write(",".join(wantedSavesFails[wantedSave]))
                    writeFile.write("\n")
                if allBool:
                    for key, value in countAll.items():
                        if totalCases:
                            percent = value / totalCases * 100
                            writeFile.write(f'{key}: {percent:.2f}% ({value}/{totalCases})\n')
                        else:
                            writeFile.write(f'{key}: {value}\n')

        if allBool:
            if countWanted:
                return countWanted, countAll
            else:
                return countAll
        return countWanted

    # determine the length of the last bag based on queue
    def __findLastBag(self, pieces):
        if not re.match("[!1-7*]", pieces[-1]):
            self.takeError("Pieces SyntaxError", "The pieces inputted doesn't end with a bag")
        try:
            # what kind of bag is the last part
            lastPartPieces = re.findall("\[?([\^tiljszoTILJSZO*]+)\]?p?[1-7!]?", pieces)[-1]
            # number of pieces used in the next bag
            newBagNumUsed = pieces[-1]
        except:
            self.takeError("Pieces SyntaxError", "The pieces inputted doesn't end with a bag")

        # turn the piece input into data for determining saves
        if lastPartPieces[0] == "*":
                # all pieces used
                lastBag = self.PIECES
        elif lastPartPieces[0] == "^":
                # remove the pieces from the bag
                lastBag = set(self.PIECES) - set([piece.upper() for piece in lastPartPieces[1:]])
        else:
                # only these pieces in the bag
                lastBag = set([piece.upper() for piece in lastPartPieces])

        # determine the number of pieces the last bag has
        if newBagNumUsed.isnumeric():
            newBagNumUsed = int(newBagNumUsed)
        elif newBagNumUsed == "!":
            # it must be !
            newBagNumUsed = len(lastBag)
        else:
            # case without a number or ! (just *)
            newBagNumUsed = 1

        return set(lastBag), newBagNumUsed
    
    # finds all the saves and adds them to a list
    def __createAllSavesQ(self, savePieces, bagSavePieces, solveable=True):
        allSaves = []
        if solveable and not savePieces:
            lstSaves = list(bagSavePieces)
            saves = [self.tetrisSort("".join(lstSaves))]
            return saves
        for p in savePieces:
            lstSaves = list(bagSavePieces)
            lstSaves.append(p)
            saves = self.tetrisSort("".join(lstSaves))
            allSaves.append(saves)
        return allSaves

    # turn the wantedPieces into a multi-depth stack to easily parse through
    def __makeStack(self, wantedPieces, index=0, depth=0):
        stack = []

        queue = ""
        operatorHold = ""
        while index < len(wantedPieces):
            char = wantedPieces[index]

            # finish for normal queue
            if queue and not re.match("[TILJSZO]", char):
                stack.append(self.tetrisSort(queue))
                queue = ""
                
            # regex queue
            if char == "/":
                try:
                    queue = re.findall("(/.*?/)", wantedPieces[index:])[0]
                except:
                    self.takeError("WantedSave SyntaxError", "missing ending '/' in regex queue")
                stack.append(queue)
                index += len(queue) - 1
                queue = ""

            # normal queue
            elif re.match("[TILJSZO]", char):
                queue += char

            # negator
            elif char == "!":
                stack.append("!")
            # avoider
            elif char =="^":
                stack.append("^")

            # operator
            elif char == "&" or char == "|":
                if operatorHold == char:
                    stack.append(operatorHold*2)
                    operatorHold = ""
                elif len(operatorHold) == 1:
                    self.takeError("WantedSave SyntaxError", "Operator inputted incorrectly should be && or ||")
                else:
                    operatorHold += char
                
            # parentheses
            elif char == "(":
                lst, i = self.__makeStack(wantedPieces, index+1, depth+1)
                stack.append(lst)
                index = i
            elif char == ")":
                if depth != 0:
                    return stack, index
                else:
                    self.takeError("WantedSave SyntaxError", "missing opening parentheses")
            # error
            else:
                self.takeError("WantedSave SyntaxError", f"wanted pieces input has unknown character '{char}'")
            index += 1
        
        if queue:
            stack.append(self.tetrisSort(queue))
            queue = ""

        # check if back to the top layer
        if depth == 0:
            return stack
        else:
            self.takeError("WantedSave SyntaxError", "missing closing parentheses")
    
    def __compareQueues(self, allSaves, queue, diff=False):
        # check regex queue
        if re.match("/.*/", queue):
            if not diff:
                for save in allSaves:
                    if re.search(queue[1:-1], save):
                        return True
            else:
                for save in allSaves:
                    if not re.search(queue[1:-1], save):
                        return True
        
        # normal queue
        else:
            for save in allSaves:
                index = 0
                for piece in save:
                    if index == len(queue):
                        break
                    if piece == queue[index]:
                        index += 1
                if diff:
                    if index != len(queue):
                        return True
                elif index == len(queue):
                        return True
        
        return False                

    # returns a list parallel to allSaves with boolen if fits that queue
    def listCompareQueues(self, allSaves, queue):
        pass

    def parseStack(self, allSaves, stack, distributeNOT=False, distributeAvoid=False):
        negate = distributeNOT
        avoid = distributeAvoid
        operator = ""
        currBool = False
        for ele in stack:
            if ele == "!":
                negate = not negate
            elif ele == "^":
                avoid = not avoid

            elif self.isOperator(ele):
                operator = ele
            
            elif self.isQueue(ele) or type(ele) == type([]):
                if self.isQueue(ele):
                    saveable = self.__compareQueues(allSaves, ele, diff=avoid)
                else:
                    saveable = self.parseStack(allSaves, ele, negate, avoid)
                if negate:
                    saveable = not saveable
                negate = distributeNOT
                avoid = distributeAvoid
                if operator:
                    if operator == "&&":
                        if distributeNOT or distributeAvoid:
                            currBool = currBool or saveable
                        else:
                            currBool = currBool and saveable
                    elif operator == "||":
                        if distributeNOT or distributeAvoid:
                            currBool = currBool and saveable
                        else:
                            currBool = currBool or saveable
                    else:
                        self.takeError("WantedParse RuntimeError", "Operator variable got a non-operator (please contact dev)")
                else:
                    currBool = saveable

            else:
                self.takeError("WantedParse RuntimeError", "stack includes string that's not a queue nor operator (please contact dev)")
        return currBool

    # filter the path fumen's for the particular save
    def filterPath(self, wantedSaves):
        headerLine = ""
        pathFileLines = []
        fumenSet = set()
        with open(self.pathFile, "r") as outfile:
            headerLine = outfile.readline()
            for line in outfile:
                line = line.rstrip().split(",")
                pathFileLines.append(line)
                fumens = line[4].split(";")
                fumenSet = fumenSet | set(fumens)
        
        fumenSet = list(fumenSet)
        os.system(f'node {self.fumenLabels} ' + " ".join(fumenSet))
        
        fumenAndQueue = {}
        with open(self.scripts, "r") as outfile:
            for line, fumen in zip(outfile, fumenSet):
                fumenAndQueue[fumen] = line.rstrip()
        
        # main section
        pieces = self.getFromLastOutput("  ([TILJSZOp1-7!,\[\]^*]+)", self.logFile)[0]
        lastBag, newBagNumUsed = self.__findLastBag(pieces)
        stack = self.__makeStack(wantedSaves)
        for line in pathFileLines:
            queue = self.tetrisSort(line[0])
            fumens = line[4].split(";")
            index = len(fumens) - 1
            while index >= 0:
                # X at the end to make sure same length and that last piece must be the difference
                label = self.tetrisSort(fumenAndQueue[fumens[index]]) + "X"
                for pieceL, pieceQ in zip(label, queue):
                    if pieceL != pieceQ:
                        savePiece = pieceQ
                        break
                
                bagSavePieces = lastBag - set(line[0][-newBagNumUsed:])
                allSave = [self.tetrisSort("".join(savePiece) + "".join(bagSavePieces))]
                if not self.parseStack(allSave, stack):
                    fumens.pop(index)
                index -= 1
            line[4] = ";".join(fumens)
            line[1] = str(len(fumens))

        with open(self.pathFile, "w") as infile:
            infile.write(headerLine)
            for line in pathFileLines:
                infile.write(",".join(line) + "\n")
    
    # sorts the pieces inputted
    def tetrisSort(self, queue):
        # order of the pieces TILJSZO
        PIECEORDER = {
            "T":"1", "1":"T",
            "I":"2", "2":"I",
            "L":"3", "3":"L",
            "J":"4", "4":"J",
            "S":"5", "5":"S",
            "Z":"6", "6":"Z",
            "O":"7", "7":"O"
        }

        numQ = ""
        for p in queue:
            numQ += PIECEORDER[p]

        numQ = "".join(sorted(list(numQ)))
        queue = ""

        for c in numQ:
            queue += PIECEORDER[c]

        return queue
    
    def isOperator(self, operator):
        return operator == "&&" or operator == "||"

    def isQueue(self, queue):
        if queue[0] == "/":
            return True
        return re.match("[TILJSZO]+", str(queue))
    
    def runSfinderPathForSaves(self, pieces, options=""):
        if self.runSfinder("path", pieces, logFile=self.logFile, options=f"-k pattern -f csv -o {self.pathFile} {options}"):
            self.removeLog(self.logFile)