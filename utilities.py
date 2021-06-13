# the parent class of other utilities classes
from os import system
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
        if logFile is None:
            logFile = self.lastOutput
        
        commandStr = f'java -jar {self.sfinder} {cmd} -p {pieces} -fp {self.field} -lp {logFile} {options}'
        system(commandStr)

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

    def takeError(self, errorType, message):
        with open(self.error, "w") as infile:
            infile.write(f'{errorType}: {message}\n')