#!/usr/bin/env python
# coding: utf-8

# In[9]:


import matplotlib
import boardgamegeek as bgg
import os
import requests
import pandas as pnd
"""Retrieval of BGG DB
A specific date can be given, else gets always the csv from 2020/05/03"""
class BggDbGetter:
    def __init__(self):
        self._github_link = "https://raw.githubusercontent.com/beefsack/bgg-ranking-historicals/705e64381e3ccb16d8b725baabb9f2bd4bcb98d3/"
    def db_write(self, date = "2020-05-23"):
        git_link = self._github_link + date + ".csv"
        response = requests.get(git_link)
        with open(os.path.join(".", "BGG_latest.csv"), "wb") as f:
            f.write(response.content)
        return True

