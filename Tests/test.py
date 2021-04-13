#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:56:04 2021

@author: arpanganguli
"""

import unittest
import pandas as pd
import glob
import sys
import os
from math import exp, log, sqrt
from scipy.stats import norm
from main_dir import (
    generate_dataframe, 
    intermediate_replacement_cost, 
    calculate_replacement_cost,
    calculate_market_value,
    calculate_multiplier,
    calculate_supervisory_delta_put,
    calculate_supervisory_delta_call,
    calculate_effective_notional,
    FILES_LIST,
    FILES_DIR,
    FILE_NAMES
    )

class TestSum(unittest.TestCase):
    
    def generate_dataframe(self):
        """
        Checks if the function picks up the latest file.

        """
        print(FILES_LIST)
            
if __name__ == "__main__":
    unittest.main()