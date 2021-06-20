from utilities import Utility
import re
class Percent(Utility):
    logFile = "resources/output/percentLastOutput.txt"

    def runPercent(self, pieces):
        if self.runSfinderPercent(pieces):
            return

        with open(self.percentOutput, "w") as infile:
            chance = self.getFromLastOutput("success = (.*)", self.logFile)[0]
            shortQueueChance = self.getFromLastOutput("([\w*] -> .*)\n\n-", self.logFile, re.DOTALL)[0]

            # getting and formating 
            noSolveQueues = self.getFromLastOutput("Fail pattern [(]all[)]\n(.*)\n\n#", self.logFile, re.DOTALL)[0]
            if noSolveQueues != "nothing":
                noSolveQueues = "\n".join(["".join(q.split(", ")) for q in noSolveQueues[1:-1].split("]\n[")])
            
            infile.write(chance + "\n")
            infile.write(shortQueueChance + "\n")
            infile.write(noSolveQueues + "\n")

    def runSfinderPercent(self, pieces, options=""):
        if self.runSfinder("percent", pieces, logFile=self.logFile, options=f'-fc -1 {options}'):
            self.removeLog(self.logFile)
            return True
        return False