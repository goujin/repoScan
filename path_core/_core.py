import re
import os
TEST_DIRECTORY = r"F:\dev\repoScan\tests\testDirectory1"
def lss(directory):
    listFiles=[]
    alreadyTestedRegex = []
    files = os.listdir(directory)
    dealtWithFile = []
    baseRegex = re.compile(r"(\d+)") # TODO I think I need to stop using groups
    for basename in files:
        if basename in dealtWithFile:
            continue
        possibleSequence = []  # (regex, result)
        for match in baseRegex.findall(basename):   # TODO check compiledRegex.finditer() instead
            print("testing basename: {}".format(basename))
            # regexComponent = "(\d{" + str(len(match)) + "})"
            # TODO make new regex use string.split(match) and then build a regex string like this # (file.)(\d +)(.03.rgb) if we use that we avoid issues later on and we can easily replace stuff
            newRegex = basename.replace(match, r'(\d+)')  # FIXME this is a major flaw. file03.03.rg replace 03, we just broke it
            if newRegex in alreadyTestedRegex:
                continue
            newSearch = re.compile(newRegex)
            matchingFiles = filter(newSearch.search, files)

            possibleSequence.append((newSearch, matchingFiles))
        if possibleSequence:
            maxMatch = 0
            for regex, results in possibleSequence:
                if len(results) == 1 and maxMatch == 0:
                    bestResults = None
                elif len(results) > maxMatch:
                    maxMatch = len(results)
                    bestRegex = regex
                    bestResults = results
            if bestResults:
                print bestRegex.pattern
                listFiles.append(Sequence.fromRegexAndFiles(bestRegex, bestResults))
                dealtWithFile.extend(bestResults)
                print "I'm a sequence: {}".format(bestResults)
            else:
                listFiles.append(basename)
                print("I'm a file: {}".format(basename))
    print(listFiles)
    result = ''
    for each in listFiles:
        if isinstance(each, Sequence):
            result += str(each) + "\n"
        else:
            result += "1 {}\n".format(each)
    print result


class Sequence(object):
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
        padding = '%d' if len(max(match)) == 1 else '%{:02}d'.format(len(max(match)))
        # (file)(\d +)(.03.rgb)
        # et puis remplacer avec ceci
        # g<1>test\g<3>
        sequence.path = files[0].replace(match[0], padding) # FIXME this is a major flaw. file03.03.rg replace 03, we just broke it
        sequence.frameRange = cls._figureOutFrameRange(match)
        return sequence

    @staticmethod
    def _figureOutFrameRange(frameNumbers):
        """
        Implementation details to output a frame range string in this style "40-43 45-49 50 53-54"
        It will takes in comatch[0]nsideration that the frames might come with padding and it will remove it by using
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