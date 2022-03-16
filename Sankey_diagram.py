#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import plotly


# In[3]:


import plotly.graph_objects as go


# In[4]:


import plotly.express as px


# In[5]:


import csv


# In[6]:


import sys


# In[7]:


from simpledbf import Dbf5


# In[8]:


dbf = Dbf5('lcdb-v41-land-cover-database-version-41-mainland-new-zealand.dbf')


# In[9]:


LUtable = dbf.to_dataframe() #convert dbf to pandas data frame


# In[10]:


LUtable.head() #view table head


# In[11]:


LUtable = LUtable.drop_duplicates(subset='Class_2012', keep="first")


# In[12]:


LUtable.shape


# In[13]:


LUtable = LUtable [["Name_2012", "Class_2012"]]


# In[14]:


LUtable.shape


# In[15]:


df = Dbf5('lndtrwtlnd3.dbf') #open dbf file


# In[16]:


df = df.to_dataframe() #convert dbf to pandas data frame


# In[17]:


df = df.rename(columns={'LNDCVRWR':'Class_2012'})


# In[18]:


df = df[["COUNT","CHANGE_TC", "Class_2012"]] 


# In[19]:


sankeydata=pd.merge(df, LUtable, on="Class_2012") #merge land use code into dataframe


# In[20]:


sankeydata = sankeydata[["COUNT","CHANGE_TC", "Name_2012"]] 


# In[21]:


sankeydata = sankeydata.rename(columns={'COUNT': 'Value', 'CHANGE_TC': 'Target', "Name_2012": "Source"})


# In[22]:


sankeydata.shape


# In[23]:


sankeydata = sankeydata.groupby(['Source','Target']).sum().reset_index() ## sum all values of rows of equal source and target. Values are counts of number of cells


# In[24]:


sankeydata['Source'] = sankeydata['Source'].replace(['High Producing Exotic Grassland'],'Pastureland') #replace grassland for pastureland


# In[25]:


sankeydata['Value'] = (sankeydata['Value'] / 
                  sankeydata['Value'].sum()) * 100 #we will want the percentage of area changed


# In[26]:


sankeydata.head()


# In[27]:


sankeydata = sankeydata.sort_values(by='Target', ascending=False)


# In[28]:


sankeydata = sankeydata.sort_values(by='Source')


# In[29]:


sankeydata.head()


# In[30]:


sk2 = sankeydata[sankeydata['Value'] > 0.1] #we now want percentage values above 0.1 (more significant)


# In[31]:


sk2.head()


# In[32]:


nodes = pd.concat([sk2['Source'],sk2['Target']]).unique() # list unique names of source and targets


# In[33]:


nodes = pd.Series(index=nodes, data=range(len(nodes))) ##create values for each node


# In[34]:


go.Figure(go.Sankey(node = {"label":nodes.index, "color":[
                px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i in nodes
            ],
        },link={"source":nodes.loc[sk2["Source"]], "target": nodes.loc[sk2["Target"]], "value": sk2["Value"], "color": [
                px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i in nodes.loc[sk2["Target"]]]}))

