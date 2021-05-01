import re
import sys
sys.path.append(r'F:\dev\repoScan')
import path_core._core
import unittest

class Test_lss(unittest.TestCase):

    def test_constructPossibleSequenceRegex(self):
        test_cases = [
            ['file03.03.rgb', [r'file(\d+).03.rgb', r'file03.(\d+).rgb']],
            ['file3030.030', [r'file(\d+).030', r'file3030.(\d+)']],
        ]
        for x, (basename, regexStrings) in enumerate(test_cases):
            with self.subTest(i=x):
                result = path_core._core._constructPossibleSequenceRegex(basename)
                expectedResult = [re.compile(regexString) for regexString in regexStrings]
                self.assertEqual(expectedResult, result)

    def test_lss_standard(self):
        answer = ("1 alpha.txt\n"
                  "1 file.info.03.rgb\n"
                  "4 file01_%04d.rgb 40-43\n"
                  "4 file02_%04d.rgb 44-47\n"
                  "4 file%d.03.rgb 1-4\n"
                  )

        testDir = r"F:\dev\repoScan\tests\testDirectory1"  # TODO make relative to python script
        result = path_core._core.lss(testDir)
        self.assertEqual(answer, result)

class TestSequence(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()