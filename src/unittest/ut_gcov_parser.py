import unittest
import sys
import os

p = os.path.abspath('.')
sys.path.append(p)

from src.gcov_parser import GCOVParser

class TestGCOVParser(unittest.TestCase):
    
    def test_gcov_parser(self):
        parser = GCOVParser('./src/unittest/test.cpp.gcov')

        print(parser.src)

        print('lines executed')
        print(parser.line_coverage)
        self.assertAlmostEqual(parser.line_coverage, 0.625)

        print('functions executed')
        print(parser.function_coverage)
        self.assertAlmostEqual(parser.function_coverage, 0.6666, 3)

        print('branches executed')
        print(parser.branch_coverage)
        self.assertAlmostEqual(parser.branch_coverage, 0.5)

        
if __name__ == '__main__':
    unittest.main()
