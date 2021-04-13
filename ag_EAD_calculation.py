#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 20:58:18 2021

@author: arpanganguli
"""
# import packages
import ag_list_of_functions as LOF
from math import exp
import pandas as pd
import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df = LOF.generate_dataframe()
df_working = df.copy(deep=True) # create deep copy of the original dataframe so as not to disturb the original dataframe should we need it later

# add new columns for calculating hedging set
df_working["id"] = df_working["id"].astype(int)
df_working[["start_date", "end_date", "trade_date"]] = df_working[["start_date", "end_date", "trade_date"]].apply(pd.to_datetime)

df_working["s_i"] = 0.0
df_working["e_i"] = 0.0
df_working["adjusted_notional_amount"] = 0.0
df_working["supervisory_delta"] = 0.0
df_working["position"] = "long"
df_working["duration"] = 0
df_working["hedging_set"] = "USD"
df_working["supervisory_delta"] = 0.0
df_working["effective_notional"] = 0.0
MF = 1.0 # MF is 1 for all the trades(since they are unmarginedand have remaining maturities in excess of one year)

# dataframe preparation
# calculate start date, s_i and end date, e_i
for i in df_working["id"]:
    if df_working["asset_class"].iloc[i] == "vanilla_swap":
        df_working["s_i"].iloc[i] = 0.0
        df_working["e_i"].iloc[i] = round((df_working["end_date"].iloc[i].date() - datetime.date.today()).days/365, 0)
    else:
        df_working["s_i"].iloc[i] = round((datetime.date.today() - df_working["start_date"].iloc[i].date()).days/365, 0)
        df_working["e_i"].iloc[i]= round((df_working["end_date"].iloc[i].date() - df_working["start_date"].iloc[i].date()).days/365, 0)

# calculate duration of each derivative item and hedging set based on currency code
for i in df_working["id"]:
    num = exp(-0.05 * df_working["s_i"].iloc[i]) - exp(-0.05 * df_working["e_i"].iloc[i])
    df_working["adjusted_notional_amount"].iloc[i] = df_working["notional_amount"].iloc[i] * (num / 0.05)
    df_working["duration"].iloc[i] = round((df_working["end_date"].iloc[i].date() - df_working["start_date"].iloc[i].date()).days/365, 0)
    df_working["hedging_set"].iloc[i] = df_working["currency_code"].iloc[i]

# put duration of of each derivative item into bins
df_working["time_bucket"] = pd.cut(df_working["duration"], bins=[0., 15, 30, 45, 60, np.inf], labels=[1, 2, 3, 4, 5])

# calculate whether the derivative item is long or short      
for i in df_working["id"]:
    if (df_working["payment_type"].iloc[i] == "floating" and df_working["receive_type"].iloc[i] == "fixed") or (df_working["payment_type"].iloc[i] == "fixed" and df_working["receive_type"].iloc[i] == "fixed") :
        df_working["position"].iloc[i] = "short"

# calculate supervisory delta for each derivative item
for i in df_working["id"]:
    if (df_working["asset_class"].iloc[i] == "vanilla_swap" and df_working["position"].iloc[i] == "long"):
        df_working["supervisory_delta"].iloc[i] = 1.0
    elif (df_working["asset_class"].iloc[i] == "vanilla_swap" and df_working["position"].iloc[i] == "short"):
        df_working["supervisory_delta"].iloc[i] = -1.0
    elif (df_working["asset_class"].iloc[i] == "swaption" and df_working["position"].iloc[i] == "long"):
        df_working["supervisory_delta"].iloc[i] = LOF.calculate_supervisory_delta_call()
    else:
        df_working["supervisory_delta"].iloc[i] = LOF.calculate_supervisory_delta_put() 

# calculate effective notion for each derivative item
for i in df_working["id"]:
    df_working["effective_notional"].iloc[i] = df_working["supervisory_delta"].iloc[i] * df_working["adjusted_notional_amount"].iloc[i] * MF

# Calculate the effective notional of each maturity bucket of each hedging set
df_hedging_set = df_working.groupby(["time_bucket", "hedging_set"]).agg({'effective_notional': ['sum']})
df_hedging_set.reset_index(inplace=True)
df_hedging_set.columns = ["time_bucket", "hedging_set", "sum"]
df_hedging_set = df_hedging_set[df_hedging_set["sum"] != 0.0]
df_hedging_set["sum^2"] = pow(df_hedging_set["sum"], 2)

df_hedging_set_USD = df_hedging_set[df_hedging_set["hedging_set"] == "USD"]
df_hedging_set_GBP = df_hedging_set[df_hedging_set["hedging_set"] == "GBP"]

effective_notional_USD = LOF.calculate_effective_notional(df_hedging_set_USD["sum^2"], df_hedging_set_USD["sum"])
effective_notional_GBP = LOF.calculate_effective_notional(df_hedging_set_GBP["sum^2"], df_hedging_set_GBP["sum"])

# calculate add-on
add_on = (0.005 * effective_notional_USD) + (0.005 * effective_notional_GBP)

# calculate Replacement Cost (RC)
RC = LOF.calculate_replacement_cost(df_working["mtm_dirty"])

# calculate Exposure at Default (EAD)
if __name__ == '__main__':
    mutiplier = LOF.calculate_multiplier(add_on, df_working["mtm_dirty"], RC)
    EAD =   1.4 * (RC + 1 * add_on)
    print("The Exposure at Default (EAD) is: {:,.2f}".format(EAD))