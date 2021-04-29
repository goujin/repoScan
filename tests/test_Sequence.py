import sys
sys.path.append(r'F:\dev\repoScan')
import re
from path_core._core import Sequence

def test_SequenceFrameRangeString():
    """
    test 2 cases,
    1) a range at the end of the string + standard behavior
    2) a single frame at the end of the string + standard behavior
    """
    data = ["001", "005", "007"] + [str(x) for x in range(9, 15)]
    if Sequence._figureOutFrameRange(data) != '1 5 7 9-14':
        raise ValueError("test_SequenceFrameRangeString does not return the right value.")
    data.append('17')
    if Sequence._figureOutFrameRange(data) != '1 5 7 9-14 17':
        raise ValueError("test_SequenceFrameRangeString does not return the right value.")

def test_SequenceFromRegexAndFiles():
    """
    Tests the whole sequence object from the point of construction: Sequence.fromRegexAndFiles()
    We do this test by checking if the object end formatting is good.
    """
    BASE_FAIL_MSG = "test_SequenceFromRegexAndFiles does not return the right value. This is the test "

    testArgument = [re.compile(r'file(\d+).03.rgb'),
                    ['file1.03.rgb', 'file2.03.rgb', 'file3.03.rgb', 'file4.03.rgb'],
                    ]

    result = Sequence.fromRegexAndFiles(*testArgument)
    if str(result) != r'4 file%d.03.rgb 1-4':
        raise ValueError(BASE_FAIL_MSG + "on sequence with single digit padding.")

    testArgument = [re.compile(r'file1.(\d+).rgb'),
                    ['file1.21.rgb', 'file1.22.rgb', 'file1.23.rgb', 'file1.24.rgb', 'file1.25.rgb'],
                    ]

    result = Sequence.fromRegexAndFiles(*testArgument)
    if str(result) != r'5 file1.%02d.rgb 21-25':
        raise ValueError(BASE_FAIL_MSG + "on sequence with greater than single digit padding.")

    testArgument = [re.compile(r'file1.(\d+).rgb'),
                    ['file1.0021.rgb', 'file1.0022.rgb', 'file1.0023.rgb']
                    ]

    result = Sequence.fromRegexAndFiles(*testArgument)
    if str(result) != r'3 file1.%04d.rgb 21-23':
        raise ValueError(BASE_FAIL_MSG + "on sequence with padding of 4 and more but frames under the 100th.")


test_SequenceFrameRangeString()
test_SequenceFromRegexAndFiles()
