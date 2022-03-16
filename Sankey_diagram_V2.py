#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd


# In[8]:


import plotly


# In[9]:


import numpy as np


# In[10]:


import io


# In[11]:


import plotly.graph_objects as go


# In[ ]:


import plotly.express as px


# In[12]:


import csv


# In[13]:


import sys


# In[14]:


from simpledbf import Dbf5


# In[15]:


dbf = Dbf5('lcdb-v41-land-cover-database-version-41-mainland-new-zealand.dbf')


# In[16]:


LUtable = dbf.to_dataframe() #convert dbf to pandas data frame


# In[17]:


LUtable.head() #view table head


# In[18]:


LUtable = LUtable.drop_duplicates(subset='Class_2012', keep="first")


# In[19]:


LUtable.shape


# In[20]:


LUtable = LUtable [["Name_2012", "Class_2012"]]


# In[21]:


LUtable.shape


# In[22]:


df = Dbf5('lndtrwtlnd3.dbf')


# In[23]:


df = df.to_dataframe() #convert dbf to pandas data frame


# In[24]:


df = df.rename(columns={'LNDCVRWR':'Class_2012'})


# In[25]:


df = df[["COUNT","CHANGE_TC", "Class_2012"]]


# In[26]:


sankeydata=pd.merge(df, LUtable, on="Class_2012")


# In[27]:


sankeydata = sankeydata[["COUNT","CHANGE_TC", "Name_2012"]]


# In[28]:


sankeydata = sankeydata.rename(columns={'COUNT': 'Value', 'CHANGE_TC': 'Target', "Name_2012": "Source"})


# In[29]:


sankeydata.shape


# In[30]:


sankeydata = sankeydata.groupby(['Source','Target']).sum().reset_index() ## sum all values of rows of equal source and target. values are counts of number of cells


# In[31]:


sankeydata['Source'] = sankeydata['Source'].replace(['High Producing Exotic Grassland'],'Pastureland')


# In[32]:


sankeydata['Value'] = (sankeydata['Value'] / 
                  sankeydata['Value'].sum()) * 100 #we will want the percentage of area changed


# In[33]:


sankeydata.head()


# In[153]:


sankeydata = sankeydata.sort_values(by='Target', ascending=False) #order by descending order for better visualisation on the graph


# In[151]:


sankeydata = sankeydata.sort_values(by='Source')


# In[154]:


sankeydata.head()


# In[155]:


sk2 = sankeydata[sankeydata['Value'] > 0.1] #we now want percentage values above 0.1 (more significant)


# In[156]:


sk2.head()


# In[127]:


nodes = pd.concat([sk2['Source'],sk2['Target']]).unique() # list unique names of source and targets


# In[128]:


nodes = pd.Series(index=nodes, data=range(len(nodes))) ##create values for each node


# In[157]:


go.Figure(go.Sankey(node = {"label":nodes.index, "color":[
                px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i in nodes
            ],
        },link={"source":nodes.loc[sk2["Source"]], "target": nodes.loc[sk2["Target"]], "value": sk2["Value"], "color": [
                px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i in nodes.loc[sk2["Target"]]]}))


# In[ ]:


#000000 for same number of sources unique names
#00ff00, #008000,#ffff00, #c0c0c0, #00ffff, #0000ff, #800080


# In[135]:


#s=[np.repeat('black',len(pd.unique(sk2['Source'])))]


# In[136]:


#s = np.append(s,['#008000','#ffff00', '#c0c0c0','#00ffff', '#0000ff', '#ff00ff'])

