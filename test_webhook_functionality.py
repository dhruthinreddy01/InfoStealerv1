# InfoSnare Test: Check if data is dumped to stolen_data/
import os
import glob

def test_data_dump():
    data_files = glob.glob(os.path.join('stolen_data', 'dump_*.json'))
    if data_files:
        print('[PASS] Data dump file(s) found:', data_files)
    else:
        print('[FAIL] No data dump files found in stolen_data/.')

if __name__ == '__main__':
    test_data_dump()
