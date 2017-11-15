#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import numpy as np
import string
import pandas as pd
import numpy as np
import re 
from datetime import datetime, timedelta

df = pd.read_csv("./Trump_ALL.csv")
df['text'] = df['text'].str.replace('http\S+|www.\S+', '', case=False)
for k in range(0,len(df)):
     row = df.loc[k,'text']
     clean=re.sub(r'\http.+\n','',row)
     clean = clean.replace('➡️', '')
     clean = clean.replace('“', '')
     clean = clean.replace('”', '')
     clean = clean.replace('"', '')
     clean = clean.replace('.', '')
     clean = clean.replace(',', '')
     clean = clean.replace(':', '')
     clean = clean.replace(';', '')
#     clean = clean.replace('-', '')
     clean = clean.replace('(', '')
     clean = clean.replace(')', '')
     clean = clean.replace("’", "")
     clean = clean.replace("'", "")
     clean = clean.replace('President O ','President Obama')
     clean = clean.replace('president O ','president Obama')
     clean = clean.replace('noko','north korea')
     clean = clean.replace('NoKo','North Korea')
#     clean = clean.replace(' r ','republican')
#     clean = clean.replace(' R ','republican')
     clean = clean.replace("&amp", "and")
#     clean = clean.replace('#', ' ')
     clean = re.sub('[^0-9a-zA-Z%.]+', ' ', clean)
        
     df.loc[k,'text']=clean

d = datetime.today() - timedelta(days=7)
print(d)
for k in range(150):
    startdate=str((datetime.today()- timedelta(days=2))-timedelta(days=7)*(k+1))
    enddate=str((datetime.today()- timedelta(days=2))-timedelta(days=7)*k)
    mask = (pd.to_datetime(df['created_at']) > startdate) & (pd.to_datetime(df['created_at']) <= enddate)
    df0=df.loc[mask]
    df0.to_csv('./week'+str(k+1)+'.csv')
