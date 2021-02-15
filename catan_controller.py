#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 11:25:27 2020

@author: kieganlenihan
"""
import bs4
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from tabulate import tabulate


def resource_table_init(players):
    lst = [0] * len(players)
    d = {"Player": players,"lumber": lst, "brick": lst, "wool": lst, "grain": lst, "ore":lst, "mystery": lst}
    df = pd.DataFrame(data = d)
    return df
def message_action(df, player, action, message):
    print("MESSAGE", message)
    if "got:" in action:
        for img in item.find_all('img', alt = True):
            if any(col in img['alt'] for col in cols):
                df.loc[df.index[players.index(player)], img['alt']] += 1
    if "built" in action:
        for img in item.find_all('img', alt = True):
            if "settlement" in img['alt']:
                df.loc[df.index[players.index(player)], 'lumber'] -= 1
                df.loc[df.index[players.index(player)], 'brick'] -= 1
                df.loc[df.index[players.index(player)], 'grain'] -= 1
                df.loc[df.index[players.index(player)], 'wool'] -= 1
            if "city" in img['alt']:
                df.loc[df.index[players.index(player)], 'grain'] -= 2
                df.loc[df.index[players.index(player)], 'ore'] -= 3
            if "road" in img['alt']:
                df.loc[df.index[players.index(player)], 'lumber'] -= 1
                df.loc[df.index[players.index(player)], 'brick'] -= 1
            if "ship" in img['alt']:
                df.loc[df.index[players.index(player)], 'lumber'] -= 1
                df.loc[df.index[players.index(player)], 'wool'] -= 1
    return df

DRIVER_PATH = '/Users/kieganlenihan/Downloads/chromedriver' #chromedriver path
options = webdriver.ChromeOptions()
# options.add_argument('headless')
driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
url = "https://colonist.io/#4Zej"

pause = 30
players = []
gameStart = False
while True:
    driver.get(url)
    time.sleep(pause)
    html = driver.page_source
    soup = bs4.BeautifulSoup(html, 'lxml')
    result = soup.find_all('div', class_ = "message_post")
    for item in result:
        if gameStart:
            if any(player in item.text for player in players):
                player = item.text.split(" ", 1)[0]
                action = item.text.split(" ", 1)[1]
                
                # How do we remove duplicate action?
                # Ex: Gorgon got lumber
                #     Gorgon got lumber
                #
                res_table = message_action(res_table, player, action, item)
                
                
            if "rolled" in item.text:
                print(tabulate(res_table, headers='keys'))
        else:
            if "turn to place" in item.text:
                players.append(item.text.split(" ", 1)[0])
            if "Giving out starting resources" in item.text:
                gameStart = True
                players = list(set(players))
                res_table = resource_table_init(players)
                cols = list(res_table.columns)
                pause = 10
            
                
                
                
                
            # if gameStart:
            #     if any(player in item.text for player in players):
            #         ## action (got, stole, rolled, wants to give, traded with, built, bought, gave bank)
            #         ## used (knight, year of plenty, road builder, monopoly)
            #         ## got __resource__
            #         ## rolled __dice__
            #         ## has __ needs to discard __
            #         ## discarded
            #         ## stole all of __
            #         ## won the game
            #         ## received (longest road)
                    
            #     print(item.text)
            #     for img in item.find_all('img', alt=True):
            #         print(img['alt'])
                
        