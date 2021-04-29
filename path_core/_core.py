import re
import os
TEST_DIRECTORY = r"F:\dev\repoScan\tests\testDirectory1"
def lss(directory):
    listFiles=[]
    alreadyTestedRegex = []
    files = os.listdir(directory)
    baseRegex = re.compile(r"(\d+)") # TODO I think I need to stop using groups
    for basename in files:
        possibleSequence = []  # (regex, result)
        for match in baseRegex.findall(basename):   # TODO check compiledRegex.finditer() instead
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

                print bestRegex.pattern
                print "I'm a sequence: {}".format(bestResults)
            else:
                print("I'm a file: {}".format(basename))
        # listFiles.append(Sequence.fromList(bestResults))



    result = filter(regex.match, files)
    print result

def recursiveCheckPatterns(path):
    pass

# lss(TEST_DIRECTORY)



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

    def __str__(self):
        return ' '.join([str(len(self.frames)), self.path, self.frameRange])

    @classmethod
    def fromRegexAndFiles(cls, regex, files):
        sequence = cls()
        sequence.frames = files

        match = [regex.match(name).group(1) for name in files]
        padding = '%d' if len(match[0]) == 1 else '%{:02}d'.format(len(max(match)))
        sequence.path = files[0].replace(match[0], padding)
        sequence.frameRange = cls._figureOutFrameRange(match)
        return sequence

    @staticmethod
    def _figureOutFrameRange(frameNumbers):
        """
        Implementation details to output a frame range string in this style "40-43 45-49 50 53-54"
        It will takes in consideration that the frames might come with padding and it will remove it by using
        `str(int(n))`.
        padding which must be removed to
        :param frameNumbers: a list of strings representing frames.
        :type frameNumbers: list
        :return: str
        """
        #TODO implement this new design
        # So we make on function that analyses continuous sequence pattern, it extract a list of list of frames
        # from which we can cycle through and write
        # "{}-{}.format(min(listFrames), max(listFrames)) if len(listFrames > 1 else str(listFrames[0]))"
        frameNumbers = [int(x) for x in frameNumbers]
        frameNumbers.sort()
        maxPoint = max(frameNumbers)
        frameString = ''
        previous = None
        isFollowup = None
        for frame in frameNumbers:
            if not previous:
                frameString += str(frame)
                previous = frame
                continue
            if previous+1 != frame and not isFollowup:
                frameString += ' {}'.format(frame)
                previous = frame
                continue
            if previous+1 != frame and isFollowup:
                frameString += '-{} {}'.format(previous, frame)
                isFollowup = False
                previous = frame
                continue
            isFollowup = True
            previous = frame
        else:
            if isFollowup:
                frameString += '-{}'.format(frame)

        return frameString