#%%
import pandas as pd

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)

# %%
list(Data)
# %%
df = Data[['name','jalaliDate','IndlImbalance',
 'InslImbalance','CAR','t','EPeriod']]
df