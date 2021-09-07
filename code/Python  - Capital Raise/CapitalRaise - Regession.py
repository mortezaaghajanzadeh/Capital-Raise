#%%
import pandas as pd
import numpy as np

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)
# %%
df = pd.DataFrame()
df = df.append(Data[['name','jalaliDate','IndlImbalance',
 'InslImbalance','CAR_4Factor','t','EPeriod','nEvent']])
df = df.rename(columns = {'CAR_4Factor':'CAR'})

mapdf  = df.groupby(['t']).IndlImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index,mapdf['IndlImbalance']))
df['IndNT'] = df.t.map(mapdict)
df['IndNT'] = df.IndlImbalance - df.IndNT


mapdf  = df.groupby(['t']).InslImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index,mapdf['InslImbalance']))
df['InsNT'] = df.t.map(mapdict)
df['InsNT'] = df.InslImbalance - df.IndNT
df = df.replace(np.nan,0)
t = pd.DataFrame()
t = t.append(df[(df.EPeriod <0)&(df.EPeriod >-11)])
t['InsNT'] = t.groupby(['name','nEvent']).InsNT.cumsum().to_frame()
t['IndNT'] = t.groupby(['name','nEvent']).IndNT.cumsum().to_frame()
t = t[['name','CAR','t','EPeriod','nEvent','InsNT','IndNT']]
t = t[t.EPeriod == -1.0][['name','nEvent','InsNT','IndNT']]
gg = df.groupby(['name','nEvent'])

def CAR(g):
    print(g.name)
    if len(g)<40:
        return 
    a = {}
    
    try:
        b = g.loc[g.EPeriod == 1].CAR.iloc[0] - g.loc[g.EPeriod == -1].CAR.iloc[0]
    except:
        b = np.nan
        
        
    a['0-1'] = b
    
    try:
        b  = g.loc[g.EPeriod == 6].CAR.iloc[0] - g.loc[g.EPeriod == 1].CAR.iloc[0]
    except:
        b = np.nan
    a['2-6'] = b
    try:
        b = g.loc[g.EPeriod == 11].CAR.iloc[0] - g.loc[g.EPeriod == 1].CAR.iloc[0]
    except:
        b = np.nan
    a['2-11'] = b
    try:
        b = g.loc[g.EPeriod == 50].CAR.iloc[0] - g.loc[g.EPeriod == 1].CAR.iloc[0]
    except:
        b = np.nan
    a['2-50'] = b
    try:
        b = g.loc[g.EPeriod == 50].CAR.iloc[0] - g.loc[g.EPeriod == -1].CAR.iloc[0]
    except:
        b = np.nan
    a['0-50'] = b
    return a['0-1'] ,a['2-6'] ,a['2-11'],a['2-50'],a['0-50']

df = gg.apply(CAR).to_frame().reset_index()
df['0-1'], df['2-6'], df['2-11'], df['2-50'], df['0-50']= df[0].str
df = df.drop(columns = [0])
df = df.merge(t,on = ['name','nEvent'])
#%%
def InsNT(g,num):
    g["QuantileInsNT"] = np.nan
    for i in range(1, num+1):
        g.loc[
            g.InsNT >= g.InsNT.quantile((1 / num) * (i - 1)),
            "QuantileInsNT",
        ] = i
    return g

def IndNT(g,num):
    g["QuantileIndNT"] = np.nan
    for i in range(1, num+1):
        g.loc[
            g.IndNT >= g.IndNT.quantile((1 / num) * (i - 1)),
            "QuantileIndNT",
        ] = i
    return g
df = InsNT(df,num = 5)
df = IndNT(df,num = 5)
# %%
df.groupby('QuantileInsNT')[[ '0-1',
 '2-6',
 '2-11',
 '2-50',
 '0-50',"InsNT"]].mean()
# %%
df.groupby('QuantileIndNT')[[ '0-1',
 '2-6',
 '2-11',
 '2-50',
 '0-50',"IndNT"]].mean()
# %%
