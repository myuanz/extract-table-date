import unittest
import timesheet_extracter
from timesheet_extracter import TimesheetExtracter
import bs4
import os


class TestClass(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_timesheet(self):
        for file in os.listdir('html'):
            print(file)
            with open('html/' + file, 'r', encoding='utf-8') as f:
                html, result = f.read().split('-split-')
                result = result.strip()
                self.assertEqual(str(TimesheetExtracter.get_time_sheet(html)), result)


unittest.main()
