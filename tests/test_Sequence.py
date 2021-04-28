import sys
sys.path.append(r'F:\dev\repoScan')
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
    data = [r'file02_(\d+).rgb',
            ['file1.03.rgb', 'file2.03.rgb', 'file3.03.rgb', 'file4.03.rgb']
            ]

    result = Sequence.fromRegexAndFiles(data)
    print(result)

test_SequenceFrameRangeString()
# test_SequenceFromRegexAndFiles()
