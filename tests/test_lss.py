import sys
sys.path.append(r'F:\dev\repoScan')
from path_core import lss
import unittest

class Test_lss(unittest.TestCase):
    def test_lss_standard(self):
        answer = ("1 alpha.txt\n"
                  "4 file01_%04d.rgb 40-43\n"
                  "4 file02_%04d.rgb 44-47\n"
                  "4 file%d.03.rgb 1-4\n"
                  "1 file.info.03.rgb\n")

        testDir = r"F:\dev\repoScan\tests\testDirectory1"  # TODO make relative to python script
        result = lss(testDir)
        self.assertEqual(result, answer)

if __name__ == '__main__':
    unittest.main()
