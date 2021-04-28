import sys
sys.path.append(r'F:\dev\repoScan\path_core')
from path_core import lss

TEST_DIR = r"F:\dev\codingTest\tests\testDirectory1"
def test_lss_standard():
    answer = ("1 alpha.txt\n"
              "4 file01_%04d.rgb 40-43\n"
              "4 file02_%04d.rgb 44-47\n"
              "4 file%d.03.rgb 1-4\n"
              "1 file.info.03.rgb\n")

    result = lss(TEST_DIR)
    if not result == answer:
        raise ValueError("{} != {}".format(answer, result))
    print("No issues")


def test_lss_notCompleteSequence():
    pass

test_lss1()