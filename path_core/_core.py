import re
import os
TEST_DIRECTORY = r"F:\dev\repoScan\tests\testDirectory1"
def lss(directory):
    listFiles=[]
    files = os.listdir(directory)
    alreadyDealtWithFiles = []
    for basename in files:
        if basename in alreadyDealtWithFiles:
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
            alreadyDealtWithFiles.extend(bestResult[1])
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
        newRegex = fileName[:delimiter[0]] + r'(\d+)' + fileName[delimiter[1]:]
        regexs.append(re.compile(newRegex))
    return regexs

class Sequence(object):
    def __init__(self):
        self.frames = None
        self.path = None
        self.frameRange = None
        pass

    def __str__(self):
        """Implementation details to convert self to a string."""
        return ' '.join([str(len(self.frames)), self.path, self.frameRange])

    @classmethod
    def fromRegexAndFiles(cls, regex, files):
        """Entry point to generate a Sequence object from a regex if given a regex and list of files.

        :param regex: a compiled regex
        :param files: a list of file name
        :type files: list
        :return: a Sequence object
        :rtype: class:`Sequence`
        """
        if files != list(filter(regex.match, files)):
            raise ValueError("Regex does not match given files.")

        sequence = cls()
        sequence.frames = files

        groups = [regex.match(name).group(1) for name in files]
        frames = [int(group) for group in groups]
        digitCount = [len(group) for group in groups]
        # assumption is that a padding can be calculated by the lowest frame number of digits
        # ex of no padding at work: 8-9-10-11 ; 1-2-3 and non-valid values: 10-11-12 that's padding 2
        # ex of padding 2 at work: 99-100-101; 10-11-12 and non-valid values: 100-101 that's padding 3
        padding = '%d' if min(digitCount) == 1 else '%{:02}d'.format(min(digitCount))
        delimiter = regex.match(files[0]).regs[1]
        fileName = files[0]
        sequence.path = fileName[:delimiter[0]] + padding + fileName[delimiter[1]:]
        sequence.frameRange = cls._figureOutFrameRange(frames)
        return sequence

    @staticmethod
    def _figureOutFrameRange(frameNumbers):
        """
        Implementation details to output a frame range string in this style "40-43 45-49 50 53-54"
        padding which must be removed to
        :param frameNumbers: a list of integers.
        :type frameNumbers: list
        :return: str
        """
        #TODO implement this new design
        # So we make on function that analyses continuous sequence pattern, it extract a list of list of frames
        # from which we can cycle through and write
        # "{}-{}.format(min(listFrames), max(listFrames)) if len(listFrames > 1 else str(listFrames[0]))"
        frameNumbers = list(frameNumbers)
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