from __future__ import with_statement
from utilities import Utility
import os
import re
import time

class Solves(Utility):
    logFile = "resources/output/solvesLastOutput.txt"
    pathPrefix = "resources/output/path.html"

    fumenCombine = "fumenScripts/fumenCombine.js"
    scripts = "fumenScripts/scriptsOutput.txt"

    # @parm type either minimal or unique
    def runSolves(self, pieces, key="minimal"):
        option = ""
        if key == "unique":
            option = "-L 1"
        if self.runSfinderPathForSolves(pieces, options=option):
            return
        
        if key == "unique":
            outfile = open(self.uniqueSolves, "r", encoding="utf-8")
        else:
            outfile = open(self.sfinderMinimalSolves, "r", encoding="utf-8")

        # get the all solves link
        line = outfile.readline()
        try:
            link = re.findall("href='(.*)'>All", line)[0]
            fumenCode = re.findall("http://fumen.zui.jp/[?](.*)", link)[0]
            try:
                tinyLink = self.make_tiny(link)
            except:
                tinyLink = "Link is too large to convert to tinyurl"
        except:
            tinyLink = "There is no solves"
            fumenCode = ""

        with open(self.solvesOutput, "w") as infile:
            infile.write(f'Sfinder {key.capitalize()} Solves: \n')
            infile.write(tinyLink + "\n")
            infile.write(fumenCode + "\n")
    
    def uniqueFromPath(self):
        countSolve = {}
        with open(self.pathFile, "r") as outfile:
            outfile.readline()
            for line in outfile:
                fumens = line.rstrip().split(",")[-1]
                for fumen in fumens.split(";"):
                    if fumen not in countSolve:
                        countSolve[fumen] = 1
                    else:
                        countSolve[fumen] += 1
        countSolve = [fumen[0] for fumen in sorted(countSolve.items(), key=lambda x:x[1], reverse=True)]
        os.system(f'node {self.fumenCombine} ' + " ".join(countSolve))

        with open(self.scripts, "r") as outfile:
            line = outfile.readline()
        
        with open(self.solvesOutput, "w") as infile:
            infile.write("Unique Solves Filtered: \n")
            infile.write(self.make_tiny(line) + "\n")
            infile.write(re.search("(v115@[a-zA-Z0-9?/+]*)", line).group(0) + "\n")

    def true_minimal(self):
        os.system(f'sfinder-minimal {self.pathFile}')

        with open("path_minimal_strict.md", "r") as trueMinFile:
            allFumensLine = trueMinFile.readlines()[6]
        fumenLst = re.findall("(v115@[a-zA-Z0-9?/+]*)", allFumensLine)

        os.system(f'node {self.fumenCombine} ' + " ".join(fumenLst))

        with open(self.scripts, "r") as outfile:
            line = outfile.readline()
        
        with open(self.solvesOutput, "w") as infile:
            infile.write("True minimal: \n")
            infile.write(self.make_tiny(line) + "\n")
            infile.write(re.search("(v115@[a-zA-Z0-9?/+]*)", line).group(0) + "\n")


    def make_tiny(self, url): 
        import contextlib 
    
        try: 
            from urllib.parse import urlencode           
        
        except ImportError: 
            from urllib import urlencode 
        from urllib.request import urlopen

        request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))     
        with contextlib.closing(urlopen(request_url)) as response:                       
            return response.read().decode('utf-8 ')
    
    def runSfinderPathForSolves(self, pieces, options=""):
        if self.runSfinder("path", pieces, logFile=self.logFile, options=f"-o {self.pathPrefix} {options}"):
            self.removeLog(self.logFile)
            return True
        return False

if __name__=="__main__":
    a = Solves()
    a.true_minimal()