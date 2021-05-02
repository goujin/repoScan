"""module on path related core functions"""
import re
import os


def lss(directory):
    """A custom implementation ls following the c style printf."""
    container = FolderContainer(directory)
    print(str(container))


class FolderContainer(object):
    """An container to hold all files contained inside a directory. Files in a sequence will be kept in
    a Sequence object."""

    def __init__(self, directory):
        """Initialize a FolderContainer from the directory.

        :param directory: a path to a directory
        :type directory: str
        """
        if not (os.path.exists(directory) and os.path.isdir(directory)):
            raise ValueError("Path either does not exist or isn't a directory.")

        self.__dir = directory
        self.__contents = self._fetchContentFromFiles(os.listdir(directory))

    def __str__(self):
        """Implementation details to convert self to a string."""
        result = ''
        for each in self.__contents:
            if isinstance(each, Sequence):
                result += str(each) + "\n"
            else:
                result += "1 {}\n".format(each)
        return result

    @property
    def dir(self):
        """returns the directory of the FolderContainer.

        :return: the directory
        :rtype: str
        """
        return self.__dir

    @property
    def contents(self):
        """returns the content of the FolderContainer

        :return: list of content
        :rtype: list
        """
        return self.__contents

    @classmethod
    def _fetchContentFromFiles(cls, listOfFileName):
        """Implementation details to fetch file and Sequence object from a list of file name"""
        listFiles = []
        alreadyDealtWithFiles = []
        for fileName in listOfFileName:
            if fileName in alreadyDealtWithFiles:
                continue
            possibleRegexs = cls._constructPossibleSequenceRegex(fileName)
            maxHit = 1
            bestResult = None
            for regex in possibleRegexs:
                correspondingHits = list(filter(regex.match, listOfFileName))
                if not correspondingHits:
                    continue
                if maxHit < len(correspondingHits):
                    maxHit = len(correspondingHits)
                    bestResult = [regex, correspondingHits]

            # TODO make warning system to communicate possible alternative. Two equal sequence object are possible
            #  this would have to be run post result compilation
            #  ex: file1.1, file2.1, file2.2 This can have multiple right answers
            if bestResult:
                listFiles.append(Sequence.fromRegexAndFiles(*bestResult))
                alreadyDealtWithFiles.extend(bestResult[1])
            else:
                listFiles.append(fileName)

        return listFiles

    @staticmethod
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
    """An object representing files matching a sequence."""

    def __init__(self):
        self.__frames = None
        self.__path = None
        self.__frameRange = None
        pass

    def __str__(self):
        """Implementation details to convert self to a string."""
        return ' '.join([str(len(self.frame)), self.path, self.frameRange])

    @property
    def frame(self):
        """Property to access files associated with the sequence.

        :return: a list of fileName
        :rtype: list
        """
        return self.__frames

    @property
    def path(self):
        """Property to access the path abstraction of the sequence.

        :return: the formated path with the padding represented by a '%d' style format
        :rtype: str
        """
        return self.__path

    @property
    def frameRange(self):
        """Property that returns a string like representation of the frameRange.

        :return: a string representing the frameRange
        :rtype: str
        """
        return self.__frameRange

    @classmethod
    def fromRegexAndFiles(cls, regex, files):  # TODO make it filter it's own files to use
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
        sequence.__frames = files

        groups = [regex.match(name).group(1) for name in files]
        frames = [int(group) for group in groups]
        digitCount = [len(group) for group in groups]
        # assumption is that a padding can be calculated by the lowest frame number of digits
        # ex of no padding at work: 8-9-10-11 ; 1-2-3 and non-valid values: 10-11-12 that's padding 2
        # ex of padding 2 at work: 99-100-101; 10-11-12 and non-valid values: 100-101 that's padding 3
        padding = '%d' if min(digitCount) == 1 else '%{:02}d'.format(min(digitCount))
        delimiter = regex.match(files[0]).regs[1]
        fileName = files[0]
        sequence.__path = fileName[:delimiter[0]] + padding + fileName[delimiter[1]:]
        sequence.__frameRange = cls._figureOutFrameRange(frames)
        return sequence

    @staticmethod
    def _figureOutFrameRange(frameNumbers):
        """
        Implementation details to output a frame range string in this style "40-43 45-49 50 53-54"
        :param frameNumbers: a list of integers.
        :type frameNumbers: list
        :return: str
        """
        previousFrame = None
        sequenceStart = None
        rangeElement = []
        for frame in frameNumbers:
            if not previousFrame:
                previousFrame = frame
                sequenceStart = frame
                continue
            if previousFrame + 1 == frame:
                previousFrame = frame
            else:
                if sequenceStart != previousFrame:
                    rangeElement.append("{}-{}".format(sequenceStart, previousFrame))
                else:
                    rangeElement.append(str(previousFrame))
                previousFrame = frame
                sequenceStart = frame
        else:
            if sequenceStart != previousFrame:
                rangeElement.append("{}-{}".format(sequenceStart, previousFrame))
            else:
                rangeElement.append(str(previousFrame))

        return ' '.join(rangeElement)
