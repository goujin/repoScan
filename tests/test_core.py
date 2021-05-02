import os
import re
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).parent.parent))  # relative configuration
import path_core._core
import unittest
from unittest.mock import patch
TEST_DIR = pathlib.Path(__file__).parent


class Test_Sequence(unittest.TestCase):
    def test_SequenceFrameRangeString(self):
        """
        test 2 cases,
        1) a range at the end of the string + standard behavior
        2) a single frame at the end of the string + standard behavior
        """

        data = [1, 5, 7] + list(range(9, 15))

        self.assertEqual(path_core._core.Sequence._figureOutFrameRange(data), '1 5 7 9-14')
        data.append(17)
        self.assertEqual(path_core._core.Sequence._figureOutFrameRange(data), '1 5 7 9-14 17')

    def test_SequenceFromRegexAndFiles(self):
        """
        Tests the whole sequence object from the point of construction: Sequence.fromRegexAndFiles()
        We do this test by checking if the object end formatting is good.
        """
        allTestsCases = [[re.compile(r'file(\d+).03.rgb'),
                          ['file03.03.rgb', 'file04.03.rgb', 'file05.03.rgb', 'file06.03.rgb'],
                          r'4 file%02d.03.rgb 3-6',
                          ],  # standard test, but we start with identical numbers on first frame for extra challenge
                         [re.compile(r'file1.(\d+).rgb'),
                          ['file1.9.rgb', 'file1.10.rgb', 'file1.11.rgb', 'file1.12.rgb', 'file1.13.rgb'],
                          r'5 file1.%d.rgb 9-13',
                          ],  # testing single padding through single digit to many digits
                         [re.compile(r'file1.(\d+).rgb'),
                          ['file1.0021.rgb', 'file1.0023.rgb', 'file1.0024.rgb'],
                          r'3 file1.%04d.rgb 21 23-24',
                          ],  # testing skipping files
                         ]

        for x, (regex, files, expectedResult) in enumerate(allTestsCases):
            result = path_core._core.Sequence.fromRegexAndFiles(regex, files)
            with self.subTest(i=x):
                self.assertEqual(expectedResult, str(result))

class Test_FileContainer(unittest.TestCase):

    def test_constructPossibleSequenceRegex(self):
        """Testing if the regex built are standard for use with the Sequence.SequenceFromRegexAndFiles expectation."""
        test_cases = [
            ['file03.03.rgb', [r'file(\d+).03.rgb', r'file03.(\d+).rgb']],
            ['file3030.030', [r'file(\d+).030', r'file3030.(\d+)']],
        ]
        for x, (fileName, regexStrings) in enumerate(test_cases):
            with self.subTest(i=x):
                result = path_core._core.FolderContainer._constructPossibleSequenceRegex(fileName)
                expectedResult = [re.compile(regexString) for regexString in regexStrings]
                self.assertEqual(expectedResult, result)

    def test_containerSerialization(self):
        """Testing the serialization of a container which needs to format to a certain style."""
        answer = ("1 alpha.txt\n"
                  "1 file.info.03.rgb\n"
                  "4 file01_%04d.rgb 40-43\n"
                  "4 file02_%04d.rgb 44-47\n"
                  "4 file%d.03.rgb 1-4\n"
                  )

        testDir = str(TEST_DIR.joinpath('testDirectory1'))
        container = path_core._core.FolderContainer(testDir)
        self.assertEqual(answer, str(container))


    def test_getContainerFromFolder(self):
        """Testing if we can get a FolderContainer and if the properties are working."""
        with self.assertRaises(ValueError):
            path_core._core.FolderContainer('/imaginaryPath/')
        testDir = str(TEST_DIR.joinpath('testDirectory1'))

        listOfFiles = os.listdir(testDir)
        testRegex = [re.compile(r) for r in [r"file01_(\d+).rgb", r"file02_(\d+).rgb", r"file(\d+).03.rgb"]]
        result = {'alpha.txt', 'file.info.03.rgb'}.union({
            path_core._core.Sequence.fromRegexAndFiles(regex, listOfFiles) for regex in testRegex})


        container = path_core._core.FolderContainer(testDir)
        self.assertEqual(testDir, container.dir)
        self.assertEqual(result, set(container.contents))

    def test_getContainerFromFolder2(self):
        """Testing if we can get a FolderContainer and if the properties are working with another good example."""
        sequence = ['sd_fx29.{:04}.rgb'.format(x) for x in range(101, 148)]
        singleFiles = ['elem.info', 'strange.xml']

        result1 = ('1 elem.info\n'
                   '1 strange.xml\n'
                   '47 sd_fx29.%04d.rgb 101-147\n'
                   )

        result2 = ('1 elem.info\n'
                   '1 strange.xml\n'
                   '46 sd_fx29.%04d.rgb 101-121 123-147\n'
                   )
        files = singleFiles + sequence
        with patch("os.listdir", return_value=files) as mockedListDir, \
                patch('os.path.exists', return_value=True) as mockedPathExists, \
                patch('os.path.isdir', return_value=True) as mockedIsDir:
            container = path_core._core.FolderContainer('mockedTest')
            self.assertEqual(result1, str(container))
            mockedListDir.assert_called_once()
            mockedPathExists.assert_called_once()
            mockedIsDir.assert_called_once()

        sequence.pop(21)
        files = singleFiles + sequence
        with patch("os.listdir", return_value=files) as mockedListDir, \
                patch('os.path.exists', return_value=True) as mockedPathExists, \
                patch('os.path.isdir', return_value=True) as mockedIsDir:
            container = path_core._core.FolderContainer('mockedTest')
            self.assertEqual(result2, str(container))
            mockedListDir.assert_called_once()
            mockedPathExists.assert_called_once()
            mockedIsDir.assert_called_once()



if __name__ == '__main__':
    unittest.main()
