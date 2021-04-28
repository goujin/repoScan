import re
import os
TEST_DIRECTORY = r"F:\dev\repoScan\tests\testDirectory1"
def lss(directory):
    listFiles=[]
    alreadyTestedRegex = []
    files = os.listdir(directory)
    baseRegex = re.compile(r"(\d+)")
    for basename in files:
        possibleSequence = []  # (regex, result)
        for match in baseRegex.findall(basename):
            print("testing basename: {}".format(basename))
            # regexComponent = "(\d{" + str(len(match)) + "})"
            newRegex = basename.replace(match, r'(\d+)')
            if newRegex in alreadyTestedRegex:
                continue
            newSearch = re.compile(newRegex)
            matchingFiles = filter(newSearch.search, files)

            possibleSequence.append((newSearch, matchingFiles))
        if possibleSequence:
            maxMatch = 0
            for regex, results in possibleSequence:
                if len(results) == 1:
                    bestResults = None
                elif len(results) > maxMatch:
                    maxMatch = len(results)
                    bestRegex = regex
                    bestResults = results
            if bestResults:
                print "I'm a sequence: {}".format(bestResults)
            else:
                print("I'm a file: {}".format(basename))
        # listFiles.append(Sequence.fromList(bestResults))



    result = filter(regex.match, files)
    print result

def recursiveCheckPatterns(path):
    pass

lss(TEST_DIRECTORY)



class LonelyFile(object):
    # this is probably safe to assume
    pass


class Sequence(object):
    # TODO implement this for bonus point in handling sequences
    def __init__(self):
        self.frames = None
        self.path = None
        self.frameRange = None
        pass

    def figureOutFrameRange(self):
        pass

    @classmethod
    def fromList(cls, frameList):
        sequence = cls()
        sequence.frames = frameList
        # TODO finish implement
        pass
