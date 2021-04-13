#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:56:04 2021

@author: arpanganguli
"""

import unittest
from main_dir import sum

class TestSum(unittest.TestCase):
    
    def check_sum(self):
        """
        Checks sum

        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)
        

if __name__ == "__main__":
    unittest.main()