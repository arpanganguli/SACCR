#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 22:53:54 2021

@author: arpanganguli
"""

import unittest

class test_functions(unittest.TestCase):
    
    def calculate_market_value(value):
        market_value = value.sum()
        return market_value