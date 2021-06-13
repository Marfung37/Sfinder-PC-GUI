from __future__ import with_statement
from utilities import Utility
import re

class Solves(Utility):
    logFile = "resources/output/solvesLastOutput.txt"
    pathPrefix = "resources/output/path.html"

    # @parm type either minimal or unique
    def runSolves(self, pieces, key="minimal"):
        if key == "minimal":
            self.runSfinderPathForSolves(pieces)
            outfile = open(self.sfinderMinimalSolves, "r")
        elif key == "unique":
            self.runSfinderPathForSolves(pieces, "-L 1")
            outfile = open(self.uniqueSolves, "r")
        else:
            raise RuntimeError("Key is not allowed type")

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
            infile.write(tinyLink + "\n\n")
            infile.write(fumenCode + "\n")

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
        self.runSfinder("path", pieces, logFile=self.logFile, options=f"-o {self.pathPrefix} {options}")