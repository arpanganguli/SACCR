#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:56:04 2021

@author: arpanganguli
"""

import unittest
import pandas as pd
import time
import glob
import sys
import os
from math import exp, log, sqrt
from scipy.stats import norm
from __init__ import (
    pick_latest_file,
    generate_dataframe, 
    intermediate_replacement_cost, 
    calculate_replacement_cost,
    calculate_market_value,
    calculate_multiplier,
    calculate_supervisory_delta_put,
    calculate_supervisory_delta_call,
    calculate_effective_notional,
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
        
    
if __name__ == "__main__":
    unittest.main()