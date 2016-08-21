import unittest
from weinvest import *


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.dictionary = generate_dictionary('words')

    def test_no_output(self):
        self.assertEqual(find_all_sequences('99999', self.dictionary), [])

    def test_simple(self):
        self.assertEqual(set(find_all_sequences(
            '22559', self.dictionary)), set(['BALKY']))

    def test_long_word(self):
        self.assertEqual(set(find_all_sequences(
            '26868377763828483', self.dictionary)), set(['COUNTERPRODUCTIVE']))

    def test_initial_number(self):
        self.assertEqual(set(find_all_sequences(
            '922559', self.dictionary)), set(['9BALKY', 'WAC5KW']))

    def test_split(self):
        self.assertEqual(set(find_all_sequences('22559.63', self.dictionary)), set(
            ['BALKY-ME', 'BALKY-MD', 'BALKY-ND', 'BALKY-NE', 'BALKY-OF']))

if __name__ == '__main__':
    unittest.main()
