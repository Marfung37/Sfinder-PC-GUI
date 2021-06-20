# the parent class of other utilities classes
import os
import re

class Utility():
    # file paths
    sfinder = "resources/sfinder.jar"
    # input files for program
    field = "resources/input/field.txt"
    lastOutput = "resources/output/last_output.txt"
    pathFile = "resources/output/path.csv"
    uniqueSolves = "resources/output/path_unique.html"
    sfinderMinimalSolves = "resources/output/path_minimal.html"
    # output file from program
    error = "output/error.txt"
    savePieceOutput = "output/savePieceOutput.txt"
    solvesOutput = "output/solvesOutput.txt"
    percentOutput = "output/percentOutput.txt"

    def runSfinder(self, cmd, pieces, logFile=None, options=""):
        errorNum = self.__getErrorNum()
        if logFile is None:
            logFile = self.lastOutput
    
        commandStr = f'java -jar {self.sfinder} {cmd} -p {pieces} -fp {self.field} -lp {logFile} {options}'
        os.system(commandStr)
        return self.__handleSfinderError(errorNum)

    def getFromLastOutput(self, regex, logFile=None, option=None):
        if logFile is None:
            logFile = self.lastOutput

        # get data from the output of terminal
        try:
            with open(logFile, "r") as outfile:
                if option is not None:
                    data = re.findall(regex, outfile.read(), option)
                    if data:
                        return data
                    return ""
                for line in outfile:
                    data = re.findall(regex, line)
                    if data:
                        return data
        except:
            self.takeError("Regex Error", "Issue while regex might be issue with expression while looking at lastoutput")

    def removeLog(self, fileVar):
        os.remove(fileVar)
    
    def checkFileExist(self, fileVar):
        return os.path.exists(fileVar)
    
    def __getErrorNum(self):
        errorNum = re.findall("Error #: (\d+)", open(self.error, "r").readline())
        if errorNum:
            return int(errorNum[0]) + 1
        # error # is lost somehow so reset to 0
        return 0
    
    def __handleSfinderError(self, errorNum):
        # check if there is an sfinder error
        errorOpen = open(self.error, "r")
        if "# DateTime:" in errorOpen.readline():
            for line in errorOpen:
                if line[0] == "#":
                    continue
                temp = re.findall("  \* (.*) \[", line)
                if temp:
                    errorMsg = temp[0]
                    break
            self.takeError("Sfinder Error", errorMsg, errorNum)
            return True
        return False

    def takeError(self, errorType, message, errorNum=0):
        # update error #
        if not errorNum:
            errorNum = self.__getErrorNum()
        with open(self.error, "w") as infile:
            infile.write(f'Error #: {errorNum}\n')
            infile.write(f'{errorType}: {message}\n')