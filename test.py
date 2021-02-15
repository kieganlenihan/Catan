#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:37:01 2021

@author: kieganlenihan
"""
import pandas as pd
import numpy as np
from tabulate import tabulate

d = {"trader": [0],"acceptor": [0], "take_brick": [0], "take_wool": [0], "take_grain": [0], "take_ore": [0], "trade count": [0]}
trade_df = pd.DataFrame(data = d)
trade_df.loc[0, "take_ore"] = 1
trade_df = trade_df.append(trade_df, ignore_index= True)
trade_df = trade_df.append(trade_df, ignore_index= True)
trade_df = trade_df.append(trade_df, ignore_index= True)
trade_df.loc[trade_df['take_ore'] == 1, 'acceptor'] = "gorgon"
print(tabulate(trade_df, headers="keys"))
# trade_df.loc["take_ore" == 1, "acceptor"] = "Gorgon"
# print(tabulate(trade_df, headers="keys"))