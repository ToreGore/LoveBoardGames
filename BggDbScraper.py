#!/usr/bin/env python
# coding: utf-8


import os
import time
import random
import pandas as pnd
import BggDbGetter as BDG
from tqdm.notebook import tqdm
from boardgamegeek import BoardGameGeek
from boardgamegeek.exceptions import BoardGameGeekAPIError
from boardgamegeek.exceptions import BoardGameGeekAPIRetryError


# ### How does it work?
# This class scrapes the pages found in BGG_latest.csv via the official API implemented into boardgamegeek library. <br>
# It then proceeds to save them into another csv file called by default BGG_sampled.csv. <br>
# The name of the csv to be created, the year range and the sampling rate can be specified.
# 


class BggDbScraper:
    def __init__(self):
        self._csv = "BGG_latest.csv"
        self._bgg = BoardGameGeek()
        self._errors = []
    def db_scrape(self, date="2020-05-23", timeframe_start=2000, timeframe_end=2020, to_be_sampled=False, sampling_rate=1, final_name="BGG_sampled.csv"):
        if BDG.BggDbGetter().db_write(date):
            #BGG_latest.csv Dataframe reading and eventual sampling
            df = pnd.read_csv("BGG_latest.csv")
            df = df.loc[df["Year"].isin(range(timeframe_start, timeframe_end))]
            if to_be_sampled:
                df = df.sample(frac=sampling_rate).reset_index(drop=True)
            g = self._bgg.game(name=None, game_id=df.iloc[0]["ID"])
            
            cols = list(g.__dict__["_data"])
            new_df = pnd.DataFrame(columns = cols)
            new_df = new_df.drop(["thumbnail", "image", "expansion", "implementations", "expansions", "expands",                                  "alternative_names", "trading", "wanting", "wishing", "numcomments"], axis=1)            
            for row in tqdm(list(df.iterrows())):
                row_id = row[1]["ID"]
                new_row = {}
                try:
                    g = self._bgg.game(name=None, game_id=row_id)
                    for k, v in g.__dict__["_data"].items():
                        if k in new_df.columns:
                            new_row[k] = v                            
                    new_df = new_df.append(new_row, ignore_index=True)
                except (BoardGameGeekAPIError, BoardGameGeekAPIRetryError) as e:
                    print("Error, sleeping!")
                    time.sleep(0.5)
                    print("Error on ID: {0}".format(row_id))
                    self._errors.append(row_id)
                    while len(self._errors) > 0:
                        print("I am in while!")
                        err = self._errors.pop(0)
                        print("Err ID: ", err)
                        try:
                            print("I am in try n°2")
                            g = self._bgg.game(name=None, game_id=err)
                            for k, v in g.__dict__["_data"].items():
                                if k in new_df.columns:
                                    new_row[k] = v
                                new_df = new_df.append(new_row, ignore_index=True)
                        except (BoardGameGeekAPIError, BoardGameGeekAPIRetryError) as e2:
                            self._errors.append(err)
                            pass
                    pass
            new_df.to_csv(final_name)
        else:
            raise Exception("Error in BGG DB retrieval. Maybe you passed a non-existent date?")
