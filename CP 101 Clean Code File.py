#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing Libraries
import numpy as np
import pandas as pd
import math
import seaborn as sns
import geopandas as gpd
from IPython.display import display


# In[2]:


#Loading in SF Open Data and cleaning null/non important values and non-food-service businesses as well as closures
#prior to 2020
business4map = gpd.read_file("shapefiles")
business4map = business4map.loc[business4map["naic_code_"] == "Food Services"]
business4map = business4map.loc[business4map["city"] == "San Francisco"]
business4map = business4map.loc[(business4map["date_dba_e"].str.contains("None") == True)|(business4map["date_dba_e"].str.contains("2020") == True)|(business4map["date_dba_e"].str.contains("2021") == True)]


# In[3]:


#Converting shapefile to CSV for usage in Carto
business4map.drop("geometry", axis=1)
business4map.to_csv("restaurants.csv")


# In[ ]:





# In[3]:


#Loading in SF Open Data COVID data, and filtering down by census tract for size purposes in Carto
covid_map = gpd.read_file("covid shapefiles")
covid_map = covid_map.loc[covid_map["area_type"] == "Census Tract"]
covid_map.to_csv("CovidMap.csv")
covid_map.to_file("CovidMap.shp")


# In[4]:


#Grouping PPP/ACS data by Census Tract to get loan and demographic averages for the Census Tract 
PPP = pd.read_csv("PPP_ACS_Covid_food_drink.csv")
PPP_Grouped = PPP.groupby("census_tract").mean()
PPP_Grouped.to_csv("PPP_GroupedBy_Tract.csv")


# In[ ]:




