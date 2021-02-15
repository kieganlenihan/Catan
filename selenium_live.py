#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 10:01:27 2020

@author: kieganlenihan
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

def resource_table_init(players):
    lst = [0] * len(players)
    d = {"Player": players,"lumber": lst, "brick": lst, "wool": lst, "grain": lst, "ore":lst, "mystery +": lst, "mystery -": lst}
    df = pd.DataFrame(data = d)
    return df
def message_action(df, player, action, message, cols, players, trade_flag, got_flag):
    html = message.get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    print(action)
    print(html)
    if "got" in action:
        for img in soup.find_all("img", alt = True):
            if any(col in img["alt"] for col in cols):
                df.loc[df.index[players.index(player)], img["alt"]] += 1
                got_flag = True
    if "built" in action:
        for img in soup.find_all("img", alt = True):
            if "settlement" in img["alt"]:
                df.loc[df.index[players.index(player)], "lumber"] -= 1
                df.loc[df.index[players.index(player)], "brick"] -= 1
                df.loc[df.index[players.index(player)], "grain"] -= 1
                df.loc[df.index[players.index(player)], "wool"] -= 1
            if "city" in img["alt"]:
                df.loc[df.index[players.index(player)], "grain"] -= 2
                df.loc[df.index[players.index(player)], "ore"] -= 3
            if "road" in img["alt"]:
                df.loc[df.index[players.index(player)], "lumber"] -= 1
                df.loc[df.index[players.index(player)], "brick"] -= 1
            if "ship" in img["alt"]:
                df.loc[df.index[players.index(player)], "lumber"] -= 1
                df.loc[df.index[players.index(player)], "wool"] -= 1
    if "bought" in action:
        df.loc[df.index[players.index(player)], "grain"] -= 1
        df.loc[df.index[players.index(player)], "wool"] -= 1
        df.loc[df.index[players.index(player)], "ore"] -= 1
    if "stole from" in action:
        victim = action.split(": ", 1)[1]
        df.loc[df.index[players.index(player)], "mystery +"] += 1
        df.loc[df.index[players.index(victim)], "mystery -"] -= 1
    if "discarded" in action:
        for img in soup.find_all("img", alt = True):
            if any(col in img["alt"] for col in cols):
                df.loc[df.index[players.index(player)], img["alt"]] -= 1
    if "took from the bank": # year of plenty
        for img in soup.find_all("img", alt = True):
            if any(col in img["alt"] for col in cols):
                df.loc[df.index[players.index(player)], img["alt"]] += 1
    if "gave bank" in action:
        giving = html.split("took", 1)[0]
        giving_soup = BeautifulSoup(giving, "html.parser")
        for img in giving_soup.find_all("img", alt = True):
            if any(col in img["alt"] for col in cols):
                df.loc[df.index[players.index(player)], img["alt"]] -= 1
        taking = html.split("took", 1)[1]
        taking_soup = BeautifulSoup(taking, "html.parser")
        for img in taking_soup.find_all("img", alt = True):
            if any(col in img["alt"] for col in cols):
                df.loc[df.index[players.index(player)], img["alt"]] += 1
    if "stole all" in action:
        pass
    if "wants to give" in action:
        trade_flag += 1
        # print(soup)
        ## store possible trade
    if "traded with" in action:
        if trade_flag == 1:
            trader = action.split(": ", 1)[1]
    return df, trade_flag, got_flag
def test(url):
    DRIVER_PATH = "/Users/kieganlenihan/Downloads/chromedriver" #chromedriver path
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
    wait_for_element = 5  # wait timeout in seconds
    driver.get(url)
    
    num_ = 0
    initializing = True
    players = []
    tf = 0
    gf = False
    roller = "No one"
    while True:
        try:
            messages = driver.find_elements_by_class_name("message_post")
            num = len(messages)
            if num != num_: # message has been added
                for k in range(num_, num):
                    if initializing:
                        if "turn to place" in messages[k].text:
                            players.append(messages[k].text.split(" ", 1)[0])
                        if "Giving out starting resources" in messages[k].text:
                            initializing = False
                            players = list(set(players))
                            res_table = resource_table_init(players)
                            cols = list(res_table.columns)
                    else: # game has started
                        if any(player in messages[k].text for player in players):
                            player = messages[k].text.split(" ", 1)[0]
                            action = messages[k].text.split(" ", 1)[1]
                            if "got" not in action and gf:
                                print(roller)
                                print(tabulate(res_table, headers="keys"))
                                gf = False
                            res_table, tf, gf = message_action(res_table, player, action, messages[k], cols, players, tf, gf)
                        if "rolled" in messages[k].text:
                            roller = messages[k].text.split(" ", 1)[0]
                            gf = 0
            time.sleep(wait_for_element)
            num_ = num
        except TimeoutException as e:
            print("Wait Timed out")
            print(e)

if __name__ == "__main__":
    test("https://colonist.io/#Ama0")
    
    
    
    
    
    
    
    
    
    
    