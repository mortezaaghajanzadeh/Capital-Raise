#%%
import pandas as pd

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)

# %%
list(Data)
# %%
df = Data[['name','jalaliDate','IndlImbalance',
 'InslImbalance','CAR','t','EPeriod','nEvent']]

mapdf  = df.groupby(['t']).IndlImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index,mapdf['IndlImbalance']))
df['IndNT'] = df.t.map(mapdict)
df['IndNT'] = df.IndlImbalance - df.IndNT


mapdf  = df.groupby(['t']).InslImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index,mapdf['InslImbalance']))
df['InsNT'] = df.t.map(mapdict)
df['InsNT'] = df.InslImbalance - df.IndNT
df
