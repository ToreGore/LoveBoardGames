#!/usr/bin/env python
# coding: utf-8

# In[1]:


import BggDbGetter as BDG
import BggDbScraper as BDS


# In[4]:


class BggHelper:
    def __init__(self):
        self._getter = BDG.BggDbGetter()
        self._scraper = BDS.BggDbScraper()
    def bgg_start(self, get=False, scrape=False, get_date="2020-05-23", tf_start=2000, tf_end=2020, to_sample=False, sample_rate=1, final_name="BGG_sampled.csv"):
        if get:
            self._getter.db_write(get_date)
        if scrape:
            self._scraper.db_scrape(get_date, tf_start, tf_end, to_sample, sample_rate, final_name)


# In[ ]:





# In[ ]:




