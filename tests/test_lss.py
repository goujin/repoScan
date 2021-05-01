import re
import sys
sys.path.append(r'F:\dev\repoScan')
import path_core._core
import unittest

class Test_lss(unittest.TestCase):

    def test_constructPossibleSequenceRegex(self):
        test_cases = [
            ['file03.03.rgb', [r'(file)(\d+)(.03.rgb)', r'(file03.)(\d+)(.rgb)']],
            ['file3030.030', [r'(file)(\d+)(.030)', r'(file3030.)(\d+)']],
        ]
        for x, (basename, regexStrings) in enumerate(test_cases):
            with self.subTest(i=x):
                result = path_core._core._constructPossibleSequenceRegex(basename)
                expectedResult = [re.compile(regexString) for regexString in regexStrings]
                self.assertEqual(expectedResult, result)

    def test_lss_standard(self):
        answer = ("1 alpha.txt\n"
                  "4 file01_%04d.rgb 40-43\n"
                  "4 file02_%04d.rgb 44-47\n"
                  "4 file%d.03.rgb 1-4\n"
                  "1 file.info.03.rgb\n")

        testDir = r"F:\dev\repoScan\tests\testDirectory1"  # TODO make relative to python script
        result = path_core._core.lss(testDir)
        self.assertEqual(result, answer)

if __name__ == '__main__':
    unittest.main()
