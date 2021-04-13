#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:56:04 2021

@author: arpanganguli
"""

import unittest
import os
import pandas as pd
from init_dir import (
    pick_latest_file,
    calculate_supervisory_delta_put,
    calculate_supervisory_delta_call,
    calculate_multiplier,
    FILES_DIR,
    FILES_LIST
    )

class TestSum(unittest.TestCase):
    
    def test_pick_latest_file(self):
        """
        Checks if the function picks up the latest file.

        """
        max = FILES_LIST[0]
        for f in FILES_LIST:
            if os.path.getctime(os.path.join(FILES_DIR, f)) > os.path.getctime(os.path.join(FILES_DIR, max)):
                max = f
        
        max = FILES_DIR + max
        latest = pick_latest_file()
        
        self.assertEqual(max, latest)
        
    def test_calculate_supervisory_delta_call(self):
        """
        Checks if the function returns the right (constant) value.

        """
        SDC = calculate_supervisory_delta_call()
        
        self.assertEqual(SDC, 0.73)

    def test_calculate_supervisory_delta_put(self):
        """
        Checks if the function returns the right (constant) value.

        """
        SDP = calculate_supervisory_delta_put()
        
        self.assertEqual(SDP, -0.27)
        
    def test_calculate_multiplier(self):
        """
        Checks if the multiplier is returning relevant values.

        """
        RC = 5
        value = pd.DataFrame([1, 2, 3])
        aggregate_add_on = 1.4
        
        mult = calculate_multiplier(aggregate_add_on=aggregate_add_on, value=value, RC=RC)
        
        self.assertEqual(mult, 1)
    
if __name__ == "__main__":
    unittest.main()