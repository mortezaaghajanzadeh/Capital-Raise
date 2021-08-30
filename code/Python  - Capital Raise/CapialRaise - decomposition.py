#%%
from AB_Functions import *
from CleaningFunctions import *

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
path1 = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
#%%
pdf = pd.read_parquet(path1 + "Cleaned_Stocks_Prices_1400-04-27.parquet").reset_index(
    drop=True
)
