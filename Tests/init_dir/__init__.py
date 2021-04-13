#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:55:11 2021

@author: arpanganguli
"""
import pandas as pd
import os
from math import exp, log, sqrt
from scipy.stats import norm

HOME = os.path.dirname(os.getcwd())
FILES_DIR = os.path.join(HOME, "Database/")
print(FILES_DIR)

_, _, filenames = next(os.walk(FILES_DIR), (None, None, []))
FILES_LIST = [f for f in filenames if f.endswith(".json")]


# develop functions

def pick_latest_file():
    TESTDIR= [FILES_DIR + f for f in FILES_LIST]
    latest_file = max(TESTDIR, key=os.path.getctime)
    return latest_file

def generate_dataframe():
    """
    Returns
    -------
    Reads the latest JSON file from the Database directory and generate resulting dataframe.

    """
    latest_file = pick_latest_file()
    
    file = pd.read_json(latest_file)
    df = pd.json_normalize(file["data"])
    
    return(df)

def intermediate_replacement_cost(func):
    """
    Provides interim steps to calculate Replacement Cost (RC) component of Exposure at Default (EAD).

    Returns
    -------
    Wrapper object.

    """
    def wrapper(*args, **kwargs):
        if func(*args, **kwargs) > 0:
            return func(*args, **kwargs) + 2
        else:
            return 0
    
    return wrapper

@intermediate_replacement_cost
def calculate_replacement_cost(market_value):
    """
    Calculates the replacement cost component of EAD.

    Parameters
    ----------
    V : Calculates Replacement Cost (RC) component of Exposure at Default (EAD)

    Returns
    -------
    Replacement Cost (RC).

    """
    return market_value.sum()


def calculate_market_value(value):
    """
    Calculates the replacement cost component of EAD.

    Parameters
    ----------
    V : Current market value of the derivatives at the reference date.

    Returns
    -------
    Replacement Cost (RC).

    """
    market_value = value.sum()
    
    return market_value

def calculate_multiplier(aggregate_add_on, value, RC):
    """
    Calculates multiplier depending on Replacement Cost (RC).

    Returns
    -------
    Multiplier.

    """
    market_value = calculate_market_value(value)
    if RC > 0:
        multiplier = 1
        return multiplier
    else:
        floor = 0.05
        multiplier = floor + (1 - floor) * exp(market_value / (2 * (1 - floor) * aggregate_add_on))
        if multiplier > 1:
            return 1
        else:
            return multiplier

def calculate_supervisory_delta_put(vol=0.5, price=0.06, strike=0.05, time=1):
    """
    Calculates supervisory delta for swaptions that are short in the primary risk factor.

    Parameters
    ----------
    vol : Supervisory option volatility.
        DESCRIPTION. The default is 50%.
    price : Underlying  price  (the appropriate  forward  swap  rate)
        DESCRIPTION. The default is 6%.
    strike : Strike  price  (the  swaption’s  fixed  rate) 
        DESCRIPTION. The default is 5%.
    time : The option exercise date.
        DESCRIPTION. The default is 1.

    Returns
    -------
    delta : Supervisory delta
        DESCRIPTION. Assigned to each trade in accordance with paragraph 159of Annex 4

    """
    num = log(price/strike) + 0.5 * pow(vol,2) * time
    denom = vol * sqrt(time)           
    delta = -1 * round(norm.cdf(-1*(num/denom)), 2)
    return delta

def calculate_supervisory_delta_call(vol=0.5, price=0.06, strike=0.05, time=1):
    """
    Calculates supervisory delta for swaptions that are long in the primary risk factor.

    Parameters
    ----------
    vol : Supervisory option volatility.
        DESCRIPTION. The default is 50%.
    price : Underlying  price  (the appropriate  forward  swap  rate)
        DESCRIPTION. The default is 6%.
    strike : Strike  price  (the  swaption’s  fixed  rate) 
        DESCRIPTION. The default is 5%.
    time : The option exercise date.
        DESCRIPTION. The default is 1.

    Returns
    -------
    delta : Supervisory delta
        DESCRIPTION. Assigned to each trade in accordance with paragraph 159of Annex 4

    """
    num = log(price/strike) + 0.5* pow(vol,2) * time
    denom = vol * sqrt(time)           
    delta = round(norm.cdf(num/denom), 2)
    return delta

def calculate_effective_notional(first_value, second_value):
    """
    Calculates effective notional amount for each hedging set

    Parameters
    ----------
    first_value : The square of sum of individual hedging currencies.
        DESCRIPTION. Individual hedging currencies are squared and then summed up for the first component.
    second_value : The sum of individual hedging currencies.
        DESCRIPTION. Individual hedging currencies are summed up and then multiplied by 1.4 for the second component.

    Returns
    -------
    Effective notional amount.

    """
    first_component = first_value.sum()
    second_component = 1.4*sum(a * b for a, b in zip(second_value, second_value[1:]))
    effective_notional = first_component + second_component
    
    return effective_notional 