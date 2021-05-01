import re
import os
TEST_DIRECTORY = r"F:\dev\repoScan\tests\testDirectory1"
def lss(directory):
    listFiles=[]
    files = os.listdir(directory)
    dealtWithFile = []
    for basename in files:
        if basename in dealtWithFile:
            continue
        possibleRegexs = _constructPossibleSequenceRegex(basename)
        maxHit = 1
        bestResult = None
        for regex in possibleRegexs:
            correspondingHits = filter(regex.match, files)
            if not correspondingHits:
                continue
            if maxHit < len(correspondingHits):
                maxHit = len(correspondingHits)
                bestResult = [regex, correspondingHits]

        # TODO make warning system to communicate possible alternative. Two equal sequence object are possible
        #  this would have to be run post result compilation
        if bestResult:
            listFiles.append(Sequence.fromRegexAndFiles(*bestResult))
        else:
            listFiles.append(basename)

    print(listFiles)
    result = ''
    for each in listFiles:
        if isinstance(each, Sequence):
            result += str(each) + "\n"
        else:
            result += "1 {}\n".format(each)
    print(result)

def _constructPossibleSequenceRegex(fileName):
    """Implementation details on how to build a useful list of regex based on possible padding inside a fileName.

    :param fileName: a file name
    :type fileName: str
    :return: a list of possible regex
    :rtype: list
    """
    regexs = []
    for match in re.finditer(r'\d+', fileName):
        delimiter = match.span()
        newRegex = '({})({})'.format(fileName[:delimiter[0]], r'\d+')
        if fileName[delimiter[1]:]:
            newRegex += '({})'.format(fileName[delimiter[1]:])
        regexs.append(re.compile(newRegex))
    return regexs

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