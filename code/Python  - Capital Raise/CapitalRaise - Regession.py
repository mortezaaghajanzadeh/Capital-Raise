#%%
import pandas as pd
import numpy as np

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)
# %%
df = pd.DataFrame()
df = df.append(Data[['name','jalaliDate','IndlImbalance',
 'InslImbalance','CAR','t','EPeriod','nEvent']])

mapdf  = df.groupby(['t']).IndlImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index,mapdf['IndlImbalance']))
df['IndNT'] = df.t.map(mapdict)
df['IndNT'] = df.IndlImbalance - df.IndNT


mapdf  = df.groupby(['t']).InslImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index,mapdf['InslImbalance']))
df['InsNT'] = df.t.map(mapdict)
df['InsNT'] = df.InslImbalance - df.IndNT
df = df.replace(np.nan,0)
#%%
t = pd.DataFrame()
t = t.append(df[(df.EPeriod <0)&(df.EPeriod >-11)])
t['InsNT'] = t.groupby(['name','nEvent']).InsNT.cumsum().to_frame()
t['IndNT'] = t.groupby(['name','nEvent']).IndNT.cumsum().to_frame()
t = t[['name','CAR','t','EPeriod','nEvent','InsNT','IndNT']]
t = t[t.EPeriod == -1.0]


# %%
df['0-1'] = 
