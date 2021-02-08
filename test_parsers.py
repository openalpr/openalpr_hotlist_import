import unittest

from utils.common import get_all_parsers
from parsers import fix_state

class TestParsers(unittest.TestCase):
    def test_results(self):

        parsers = get_all_parsers()

        for parser in parsers:
            print("Testing parser: " + parser.get_parser_name())
            test_cases = parser.get_example_tests()

            for test_case in test_cases:

                alert_config = {'name': 'test'}

                if 'parse_code' in test_case:
                    alert_config['parse_code'] = test_case['parse_code']

                raw_line = test_case['raw_line']

                # bypass any checking for headers in the parser
                parser.line_count = 2

                # parse the actual line
                actual_results = parser.parse_hotlist_line(raw_line, alert_config)

                print(actual_results)
                self.assertEqual(test_case['plate'], actual_results['plate'])
                self.assertEqual(test_case['state'], actual_results['state'])

                if 'description' in test_case:
                    self.assertEqual(test_case['description'], actual_results['description'])

                # Make sure no commas are in the description (this causes import errors)
                self.assertFalse('"' not in actual_results['description'] and "," in actual_results['description'])

                if actual_results['state'] != '':
                    print(fix_state(actual_results['state']))
                    self.assertTrue(len(fix_state(actual_results['state'])) > 3)

if __name__ == '__main__':
    unittest.main()