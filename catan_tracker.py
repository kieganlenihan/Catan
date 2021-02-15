#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 11:07:00 2021

@author: kieganlenihan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 23:18:00 2020

@author: kieganlenihan
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from tabulate import tabulate

class catan:
    def __init__(self):
        self.trade_count = 0
        self.resources = ["lumber", "brick", "wool", "grain", "ore"]
    class watcher:
        def __init__(self, initial_value=[]):
            self._value = initial_value
            self._callbacks = []
        @property
        def value(self):
            return self._value
        @value.setter
        def value(self, new_value):
            old_value = self._value
            self._value = new_value
            self._notify_observers(old_value, new_value)
        def _notify_observers(self, old_value, new_value):
            for callback in self._callbacks:
                callback(old_value, new_value)
        def register_callback(self, callback):
            self._callbacks.append(callback)
    def driver_setup(self):
        DRIVER_PATH = "/Users/kieganlenihan/Downloads/chromedriver" #chromedriver path
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("window-size=1920,1080")
        driver = webdriver.Chrome(executable_path = DRIVER_PATH, options = options)
        return driver
    def game_setup(self, player, text):
        if "turn to place" in text:
            self.players.append(player)
        if "Giving out starting resources" in text:
            self.players = list(set(self.players))
            self.res_df_init()
            self.trades_master_init()
            self.steals_master_init
            self.res_total_init()
    def res_df_init(self):
        lst = [0] * len(self.players)
        d = {"Player": self.players,"lumber": lst, "brick": lst, "wool": lst, "grain": lst, "ore": lst, "Gaurantee": [1] * len(self.players)}
        self.res_df = pd.DataFrame(data = d)
    def trades_master_init(self):
        d = {"t": [], "a": [], "give_lumber": [], "give_brick": [], "give_wool": [], "give_grain": [], "give_ore": [], "take_lumber": [], "take_brick": [], "take_wool": [], "take_grain": [], "take_ore": [], "tc": []}
        self.trades_df = pd.DataFrame(data = d)
        self.trades_master_df = pd.DataFrame(data = d)
    # def steals_master_init(self):
    #     d = {"stealer": [], "victim": [], "lumber": [], "brick": [], "wool": [], "grain": [], "ore": []}
    #     self.steals_master_df = pd.DataFrame(data = d)
    def res_total_init(self):
        d = {"lumber": [0], "brick": [0], "wool": [0], "grain": [0], "ore": [0]}
        self.res_total_df = pd.DataFrame(data = d)
    def looper(self, player, resources, qtys):
       for resource, qty in zip(resources, qtys):
            if any(col in resource for col in self.resources):
                self.res_df.loc[self.res_df.index[self.players.index(player)], resource] += qty
                self.res_total_df.loc[0, resource] += qty
    def printer(self, cnt):
        if "got" in self.log[cnt - 1].get_text():
            print(tabulate(self.res_df, headers="keys"))
            print(tabulate(self.res_total_df, headers="keys"))
    def find_images(self, soup):
        imgs = []
        for img in soup.find_all("img", alt = True):
            imgs.append(img["alt"])
        return imgs
    def trade_process(self, player, giving, wants):
        d = {"t": [0], "a": [0], "give_lumber": [0], "give_brick": [0], "give_wool": [0], "give_grain": [0], "give_ore": [0], "take_lumber": [0], "take_brick": [0], "take_wool": [0], "take_grain": [0], "take_ore": [0], "tc": [0]}
        trade_df = pd.DataFrame(data = d)
        giving_cols = [col for col in list(trade_df.columns) if "give" in col]
        taking_cols = [col for col in list(trade_df.columns) if "take" in col]
        for give in giving:
            if any(give in string for string in giving_cols):
                cor = [col for col in giving_cols if give in col] 
                trade_df.loc[0, cor] += 1
        for take in wants:
            if any(take in string for string in taking_cols):
                cor = [col for col in taking_cols if take in col] 
                trade_df.loc[0, cor] += 1
        trade_df.loc[0, "t"] = player
        trade_df.loc[0, "tc"] = self.trade_count
        return trade_df
    # def mono_res(self, player):
    #     lst = self.res_df.loc[self.res.Player == player, self.resources].values.flatten().tolist()
    #     cnt = np.count_nonzero(lst)
    #     if cnt == 1:
    #         self.res = resources[np.nonzero(lst)[0]]
    #         return True
    #     return False
    def action_manager(self, soup, player, action, cnt):
        imgs = self.find_images(soup)
        if "got" in action:
            self.looper(player, imgs, [1]*len(imgs))
        else: 
            self.printer(cnt)
        if "built" in action:
            if any("settlement" in s for s in imgs):
                self.looper(player, ["lumber", "brick", "grain", "wool"], [-1]*4)
            if any("city" in s for s in imgs):
                self.looper(player, ["grain", "ore"], [-2, -3])
            if any("road" in s for s in imgs):
                self.looper(player, ["lumber", "brick"], [-1, -1])
            if any("ship" in s for s in imgs):
                self.looper(player, ["lumber", "wool"], [-1, -1])
        if "bought" in action:
            self.looper(player, ["grain", "wool", "ore"], [-1]*3)
        if "discarded" in action:
            self.looper(player, imgs, [-1]*len(imgs))
        if "gave bank" in action:
            gave = BeautifulSoup(str(soup).split("took")[0], "html.parser")
            took = BeautifulSoup(str(soup).split("took")[1], "html.parser")
            self.looper(player, self.find_images(gave), [-1]*len(imgs))
            self.looper(player, self.find_images(took), [1]*len(imgs))
        if "used" in action:
            if any("monopoly" in img for img in imgs):
                monopolized_res = next((res for res in self.resources if res in imgs), False)
                self.res_df.loc[:, monopolized_res] = 0
                self.res_df.loc[self.res_df.index[self.players.index(player)], monopolized_res] = self.res_total_df.loc[0, monopolized_res]
        if "took from bank" in action:
            self.looper(player, imgs, [1]*len(imgs))
        if "card" in imgs:
            victim = next((player for player in self.players if player in action), False)
            print("victim", victim)
            # print("checker", self.res_df.loc[self.res_df.index[self.players.index(victim)], "Gaurantee"])
            # if self.res_df.loc[self.res_df.index[self.players.index(victim)], "Gaurantee"] == 1:
            #     if self.mono_res(player) == True:
            #         print("Gaurantee they stole a ", self.res)
            #     else:
            #         print("here")
            #         d = {"stealer": player, "victim": victim, "lumber": [], "brick": [], "wool": [], "grain": [], "ore": []}
            #         steals_df = pd.DataFrame(data = d)
            #         steals_df.loc[0, self.resources] = self.res_df.loc[self.res_df.index[self.players.index(victim)], self.resources]
            #         print("steals", steals_df)
            # else:
            #     self.res_df.loc[self.res_df.index[self.players.index(victim)], "Gaurantee"] == 0
            #     d = {"stealer": player, "victim": victim, "lumber": "unk", "brick": "unk", "wool": "unk", "grain": "unk", "ore": "unk"}
            #     steals_df = pd.DataFrame(data = d)
            # print("out of if")
            # self.steals_master_df = self.steals_master_df.append(steals_df)
            # print(tabulate(self.steals_master_df, headers="keys"))
        if "wants to give" in action:
            giving = self.find_images(BeautifulSoup(str(soup).split("for")[0], "html.parser"))
            wants = self.find_images(BeautifulSoup(str(soup).split("for")[1], "html.parser"))
            trade_df = self.trade_process(player, giving, wants)
            self.trades_df = self.trades_df.append(trade_df, ignore_index= True)
        if "traded with" in action:
            acceptor = next((player for player in self.players if player in str(soup).split("traded with")[1]), False)
            if self.trades_df.shape[0] == 1:
                pass
            # else:
            self.trades_master_df = self.trades_master_df.append(self.trades_df, ignore_index= True)
            self.trades_master_df.loc[self.trades_master_df["tc"] == self.trade_count, "a"] = acceptor
            print("Master trades_ df ->")
            print(tabulate(self.trades_master_df, headers="keys"))
            self.trade_count += 1
            d = {"t": [], "a": [], "give_lumber": [], "give_brick": [], "give_wool": [], "give_grain": [], "give_ore": [], "take_lumber": [], "take_brick": [], "take_wool": [], "take_grain": [], "take_ore": [], "tc": []}
            self.trades_df = pd.DataFrame(data = d)
        ## Check action taken and ask if if this action was possible with the cards we KNOW a player has. If not, check
        ## available trades that have happened, and if one is possible
    def message_added(self, old_value, new_value):
        if new_value != old_value:
            for k in range(len(old_value), len(new_value)):
                new = self.messages[k]
                html = new.get_attribute("innerHTML")
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text()
                self.log.append(soup)
                if text:
                    player = text.split(" ", 1)[0]
                    action = text.split(" ", 1)[1]
                    try:
                        if self.res_df is not None:
                            self.action_manager(soup, player, action, k)
                    except:
                        self.game_setup(player, text)
                else:
                    self.printer(k)
                    d = {"t": [], "a": [], "give_lumber": [], "give_brick": [], "give_wool": [], "give_grain": [], "give_ore": [], "take_lumber": [], "take_brick": [], "take_wool": [], "take_grain": [], "take_ore": [], "tc": []}
                    self.trades_df = pd.DataFrame(data = d)
                    print(text) # Turn incresaed     
    def web_grabber(self, url):
        driver = self.driver_setup()
        driver.get(url)
        message_count = self.watcher()
        message_count.register_callback(self.message_added)
        self.players, self.log = [], []
        while True:
            try:
                self.messages = driver.find_elements_by_class_name("message_post")
                message_count.value = self.messages
            except TimeoutException as e:
                print("Wait timed out")
                print(e)

if __name__ == "__main__":
    bot = catan()
    bot.web_grabber("https://colonist.io/#OZvP")
    
    
    