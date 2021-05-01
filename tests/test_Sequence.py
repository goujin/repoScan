import sys
sys.path.append(r'F:\dev\repoScan')
import re
from path_core._core import Sequence
import unittest

class TestSequence(unittest.TestCase):
    def test_SequenceFrameRangeString(self):
        """
        test 2 cases,
        1) a range at the end of the string + standard behavior
        2) a single frame at the end of the string + standard behavior
        """


        data = ["001", "005", "007"] + [str(x) for x in range(9, 15)]

        self.assertEqual(Sequence._figureOutFrameRange(data), '1 5 7 9-14')
        data.append('17')
        self.assertEqual(Sequence._figureOutFrameRange(data), '1 5 7 9-14 17')

    def test_SequenceFromRegexAndFiles(self):
        """
        Tests the whole sequence object from the point of construction: Sequence.fromRegexAndFiles()
        We do this test by checking if the object end formatting is good.
        """
        allTestsCases = [[re.compile(r'file(\d+).03.rgb'),
                          ['file03.03.rgb', 'file04.03.rgb', 'file05.03.rgb', 'file06.03.rgb'],
                          r'4 file%d.03.rgb 3-6',
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
            result = Sequence.fromRegexAndFiles(regex, files)
            with self.subTest(i=x):
                self.assertEqual(expectedResult, str(result))

if __name__ == '__main__':
    unittest.main()
