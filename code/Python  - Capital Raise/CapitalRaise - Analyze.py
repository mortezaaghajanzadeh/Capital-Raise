# %%
from AB_Functions import *
from CleaningFunctions import *
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
path1 = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
#%%
pdf = pd.read_parquet(path1 + "Cleaned_Stocks_Prices_1400-04-27.parquet").reset_index(drop = True)


#%%
indexes = pd.read_csv(path1 + "IndustryIndexes_1400-04-27.csv").reset_index(drop = True)
for i in ['industry_index','industry_size']:
    mapdict = dict(zip(indexes.set_index(['group_id','date']).index,indexes[i]))
    pdf[i] = pdf.set_index(['group_id','date']).index.map(mapdict)
    
#%%
gg = pdf.groupby(['date','group_id'])
pdf = pdf.set_index(['date','group_id'])
pdf['Weight'] = gg.MarketCap.sum()
pdf['Weight'] = pdf.MarketCap / pdf.Weight
pdf = pdf.reset_index().sort_values(by = ['name','date'])


#%%

df2 = pd.read_csv(path + "Stock_price_trade_1387_1400" + ".csv")
mlist = ['stock_id','date',
    'ind_buy_volume',
 'ins_buy_volume',
 'ind_buy_value',
 'ins_buy_value',
 'ins_buy_count',
 'ind_buy_count',
 'ind_sell_volume',
 'ins_sell_volume',
 'ind_sell_value',
 'ins_sell_value',
 'ins_sell_count',
 'ind_sell_count'
]
print(len(pdf), len(df2))

i = 'stock_id'
df2[i] = df2[i].astype(str)
pdf = pdf.merge(df2[mlist], on=["stock_id", "date"], how="left").drop_duplicates()
print(len(pdf))
pdf = pdf.rename(columns = {'close_price' : "UnadjustedPrice",
                            "AdjustedPrice":"close_price"})    
    
#%%
df = pd.read_excel(path + "Capital Rise - 71-99.xlsx")
df = df[df.CapAfter != df.CapBefore]
df = df[~df.Symbol.isnull()].rename(columns={"Symbol": "name"})
df = df[
    [
        "name",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "Revaluation",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "JustRevaluation",
        "Hybrid",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
    ]
]


df["CapBefore2"] = (df["CapBefore"] / 10).round(0)
df["CapAfter2"] = (df["CapAfter"] / 10).round(0)
df["ExtOrdGMDate2"] = (df["ExtOrdGMDate"] / 10).round(0)

df = df.drop_duplicates(subset=["name", "CapAfter2", "CapBefore2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate2", "CapBefore2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate2", "CapAfter2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate", "CapBefore2"], keep="first")
df = df.drop_duplicates(subset=["ExtOrdGMDate", "CapAfter2"], keep="first")

df = df[df.CapBefore != 0]
df["Percent"] = ((df["CapAfter"] - df["CapBefore"]) / df["CapBefore"]) * 100
df["Percent"] = df["Percent"].round(2)
df = df[df.Percent > 0]

df = df[
    [
        "name",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "Revaluation",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "JustRevaluation",
        "Hybrid",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
    ]
]
df = df.drop_duplicates(subset=["name", "year", "CapBefore"], keep="first")
df = df.drop_duplicates(subset=["name", "year", "CapAfter"], keep="first")

df = df.drop_duplicates(subset=["ExtOrdGMDate", "name"], keep="first")


df = df.sort_values(by=["name", "ExtOrdGMDate"])
df = df[
    [
        "name",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "Revaluation",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "JustRevaluation",
        "Hybrid",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
    ]
]
df = df[(df.year > 1382) & (df.year < 1399)]
df.head()

# %%


# %%
mdf = pd.DataFrame()
mdf = mdf.append(pdf)
mdf = mdf[mdf.volume != 0]
JalaliDates = list(set(mdf.jalaliDate))
JalaliDates.sort()
t = list(range(len(JalaliDates)))
mapingdict = dict(zip(JalaliDates, t))
mdf["t"] = mdf["jalaliDate"].map(mapingdict)
mapingdict = dict(zip(JalaliDates, t))

df["t"] = df["ExtOrdGMDate"].map(mapingdict)
tIndex = pd.DataFrame(list(mapingdict.keys()), columns=[0])
for i in set(df[df.t.isnull()].ExtOrdGMDate):
    mapingdict[i] = tIndex[tIndex[0] >= i].index[0]
df["t"] = df["ExtOrdGMDate"].map(mapingdict)


# %%
data = pd.DataFrame()
ndf = pd.DataFrame()
NotCapitalData = []
gg = mdf.groupby("name")
for symbol in list(gg.groups.keys()):
    print(symbol)
    d = gg.get_group(symbol)
    if len(d) < 30:
        continue
    t = df[df.name == symbol]
    if len(t) == 0:
        NotCapitalData.append(symbol)
        continue
    g = pd.DataFrame()
    g = g.append(d)
    g["CapBefore"] = np.nan
    g["CapAfter"] = np.nan
    g["ExtOrdGMDate"] = np.nan
    g["Event"] = np.nan
    g["JustRO"] = np.nan
    g["JustSaving"] = np.nan
    g["JustPremium"] = np.nan
    g["Hybrid"] = np.nan
    g["Revaluation"] = np.nan
    nEvent = 0
    for date in t.ExtOrdGMDate:

        Day = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].ExtOrdGMDate.iloc[0]
        CapBefore = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].CapBefore.iloc[
            0
        ]
        CapAfter = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].CapAfter.iloc[0]
        JustRO = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].JustRO.iloc[0]
        JustSaving = df[
            (df.name == symbol) & (df.ExtOrdGMDate == date)
        ].JustSaving.iloc[0]
        JustPremium = df[
            (df.name == symbol) & (df.ExtOrdGMDate == date)
        ].JustPremium.iloc[0]
        Hybrid = df[(df.name == symbol) & (df.ExtOrdGMDate == date)].Hybrid.iloc[0]
        Revaluation = df[
            (df.name == symbol) & (df.ExtOrdGMDate == date)
        ].Revaluation.iloc[0]
        mark = 0
        #         print(g.jalaliDate.iloc[0],date)
        if (date >= g.jalaliDate.iloc[0]) and (date < g.jalaliDate.iloc[-1]):
            nEvent += 1
            mark = 1
            g.loc[g.jalaliDate >= date, "ExtOrdGMDate"] = Day
            g.loc[g.jalaliDate >= date, "CapBefore"] = CapBefore
            g.loc[g.jalaliDate >= date, "CapAfter"] = CapAfter
            g.loc[g.jalaliDate >= date, "Event"] = g.loc[g.jalaliDate >= date].t.iloc[0]
            g.loc[g.jalaliDate >= date, "JustRO"] = JustRO
            g.loc[g.jalaliDate >= date, "JustSaving"] = JustSaving
            g.loc[g.jalaliDate >= date, "JustPremium"] = JustPremium
            g.loc[g.jalaliDate >= date, "Hybrid"] = Hybrid
            g.loc[g.jalaliDate >= date, "Revaluation"] = Revaluation
            if nEvent == 1:
                g.loc[g.jalaliDate < date, "ExtOrdGMDate"] = Day
                g.loc[g.jalaliDate < date, "CapBefore"] = CapBefore
                g.loc[g.jalaliDate < date, "CapAfter"] = CapAfter
                g.loc[g.jalaliDate < date, "Event"] = g.loc[
                    g.jalaliDate >= date
                ].t.iloc[0]
                g.loc[g.jalaliDate < date, "JustRO"] = JustRO
                g.loc[g.jalaliDate < date, "JustSaving"] = JustSaving
                g.loc[g.jalaliDate < date, "JustPremium"] = JustPremium
                g.loc[g.jalaliDate < date, "Hybrid"] = Hybrid
                g.loc[g.jalaliDate < date, "Revaluation"] = Revaluation

        if mark == 1:
            ndf = ndf.append(df[(df.name == symbol) & (df.ExtOrdGMDate == date)])
    if mark == 1:
        data = data.append(g)

ndf.to_excel(path + "SDate.xlsx", index=False)

#%%


# %%
#
data2 = data.sort_values(by=["name", "t"], ascending=False).reset_index(drop=True)
gg = data2.groupby("name")
data2["Event"] = gg["Event"].fillna(method="ffill")


# %%
data = data2.sort_values(by=["name", "t"])
# data['Period'] = data['t'] - data['Event']


# %%

index = pd.read_excel(path + "IRX6XTPI0009.xls")[["<COL14>", "<CLOSE>"]].rename(
    columns={"<COL14>": "jalaliDate", "<CLOSE>": "Index"}
)

pdf.jalaliDate = pdf.jalaliDate.astype(int)
index = index[index.jalaliDate >= pdf.jalaliDate.min()]
n = path + "RiskFree rate.xlsx"
rf = pd.read_excel(n)
rf = rf.rename(columns={"Unnamed: 2": "Year"})
rf["YM"] = rf["YM"].astype(str)
rf["YM"] = rf["YM"] + "00"
rf["YM"] = rf["YM"].astype(int)
index["RiskFree"] = np.nan
index["jalaliDate"] = index["jalaliDate"].astype(int)
for i in rf.YM:
    index.loc[index.jalaliDate >= i, "RiskFree"] = (
        rf.loc[rf["YM"] == i].iloc[0, 1] / 356
    )
data = data.merge(index, on="jalaliDate")

# %%
data = data.sort_values(by=["name", "t"]).reset_index(drop=True)
gg = data.groupby("name")
data["Market_return"] = gg["Index"].pct_change(periods=1) * 100
data["industry_return"] = gg["industry_index"].pct_change(periods=1) * 100
data = data[~data.Market_return.isnull()]
#%%
def divide_to_mean(g):
    print(g.name, end="\r", flush=True)
    g = g / g.rolling(60, 1).mean()
    return g


gg = data.groupby("name")
data["RelVolume"] = gg.volume.apply(divide_to_mean)

#%%
path1 = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
df = pd.read_excel(path1 + "Factors-Daily" + ".xlsx")
for t in ["SMB", "HML", "Winner_Loser"]:
    print(t)
    df[t + "Index"] = df[t] / 100 + 1
    df[t + "Index"] = df[t + "Index"].rolling(len(df), 1).apply(np.prod)

for t in ["SMB", "HML", "Winner_Loser"]:
    print(t)
    mapingdict = dict(zip(df.date, df[t + "Index"]))
    data[t] = data.date.map(mapingdict)
    gg = data.groupby("name")
    data[t] = gg[t].pct_change(periods=1) * 100

#%%
data.isnull().sum().to_frame()
data = data.dropna()

n = path + "RawDataBeforeAb2.parquet"

data.to_parquet(n)


#%%
data = pd.read_parquet(path + "RawDataBeforeAb2.parquet")

# %%

#%%

ARdata = pd.DataFrame()
ARdata = ARdata.append(data)
ARdata["Return"] = ARdata['return']
ARdata["ER"] = ARdata["Return"] - ARdata["RiskFree"]
ARdata["EMR"] = ARdata["Market_return"] - ARdata["RiskFree"]
ARdata["Industry_return"] = (
    ARdata["industry_return"] - ARdata["Weight"] * ARdata["Return"]
) / (1 - ARdata["Weight"])
ARdata["EIR"] = ARdata["Industry_return"] - ARdata["RiskFree"]
ARdata.loc[ARdata.Weight == 1.0, "Industry_return"] = np.nan
ARdata.loc[ARdata.Weight == 1.0, "EIR"] = np.nan
gg = ARdata.groupby("name")
# g = gg.get_group("فولاد")
# dddd = ABnormal(g, 20)
## Lag

ARdata = gg.apply(ABnormal, Rlag=20).reset_index(drop=True)
ARdata = ARdata.sort_values(by=["name", "t"])
ARdata.isnull().sum()


#%%
Data = pd.DataFrame()
Data = Data.append(ARdata)
Data = Data.reset_index(drop=True)
Data = Data.rename(columns={"ER": "EReturn"})
Data["Amihud"] = abs(Data["Return"]) / Data["volume"]
Data = Data.loc[(Data.EPeriod >= -20) & (Data.EPeriod <= 50)]

#%%

Data["NetInd"] = Data["ind_buy_volume"] - Data["ind_sell_volume"]
Data["TotalInd"] = Data["ind_buy_volume"] + Data["ind_sell_volume"]
Data["NetIns"] = Data["ins_buy_volume"] - Data["ins_sell_volume"]
Data["TotalIns"] = Data["ins_buy_volume"] + Data["ins_sell_volume"]

Data["IndlImbalance"] = Data["NetInd"].divide(Data["TotalInd"])
Data["InslImbalance"] = Data["NetIns"].divide(Data["TotalIns"])

for i in ["count", "volume", "value"]:
    Data["ind_imbalance_" + i] = Data["ind_buy_" + i] - Data["ind_sell_" + i]
    Data["ins_imbalance_" + i] = Data["ins_buy_" + i] - Data["ins_sell_" + i]
    
gg = Data.groupby(['name','nEvent'])

Data['ind_stock_account'] = gg.ind_imbalance_volume.cumsum()
Data['ins_stock_account'] = gg.ins_imbalance_volume.cumsum()

Data['ind_stock_account'] = Data['ind_stock_account'] * Data['close_price']
Data['ins_stock_account'] = Data['ins_stock_account'] * Data['close_price']

gg = Data.groupby(['name'])
Data['ind_Cash_account'] = gg.ind_imbalance_value.cumsum()
Data['ins_Cash_account'] = gg.ins_imbalance_value.cumsum()

Data['ind_Cash_account'] = Data['ind_Cash_account'] * (-1)
Data['ins_Cash_account'] = Data['ins_Cash_account'] * (-1)

Data['ind_Nav'] = Data["ind_Cash_account"] + Data["ind_stock_account"]
Data['ins_Nav'] = Data["ins_Cash_account"] + Data["ins_stock_account"]

gg = Data.groupby(["name", "nEvent"])
Data["CAR"] = gg["AbnormalReturn"].cumsum()
Data["CAR_Market"] = gg["AbnormalReturn_Market"].cumsum()
Data["CAR_WithoutAlpha"] = gg["AbnormalReturn_WithoutAlpha"].cumsum()
Data["CAR_4Factor"] = gg["AbnormalReturn_4Factor"].cumsum()

Data["CAR_Industry"] = gg["AbnormalReturn_Industry"].cumsum()
Data["CAR_WithoutAlpha_Industry"] = gg["AbnormalReturn_WithoutAlpha_Industry"].cumsum()
Data["CAR_MarketIndustry"] = gg["AbnormalReturn_MarketIndustry"].cumsum()
Data["CAR_MarketModel"] = gg["AbnormalReturn_MarketModel"].cumsum()
Data["CAR_WithoutAlpha_MarketModel"] = gg[
    "AbnormalReturn_WithoutAlpha_MarketModel"
].cumsum()
Data["CAR_MarketModel_Industry"] = gg["AbnormalReturn_MarketModel_Industry"].cumsum()
Data["CAR_WithoutAlpha_MarketModel_Industry"] = gg[
    "AbnormalReturn_WithoutAlpha_MarketModel_Industry"
].cumsum()

Data["CAR_AbnormalReturn2"] = gg["AbnormalReturn2"].cumsum()
Data["CAR_AbnormalReturn_Market2"] = gg["AbnormalReturn_Market2"].cumsum()
Data["CAR_AbnormalReturn_WithoutAlpha2"] = gg["AbnormalReturn_WithoutAlpha2"].cumsum()
Data["CAR_AbnormalReturn_Industry2"] = gg["AbnormalReturn_Industry2"].cumsum()
Data["CAR_AbnormalReturn_WithoutAlpha_Industry2"] = gg[
    "AbnormalReturn_WithoutAlpha_Industry2"
].cumsum()
Data["CAR_AbnormalReturn_MarketIndustry2"] = gg[
    "AbnormalReturn_MarketIndustry2"
].cumsum()
Data["CAR_AbnormalReturn_MarketModel2"] = gg["AbnormalReturn_MarketModel2"].cumsum()
Data["CAR_AbnormalReturn_WithoutAlpha_MarketModel2"] = gg[
    "AbnormalReturn_WithoutAlpha_MarketModel2"
].cumsum()
Data["CAR_AbnormalReturn_MarketModel_Industry2"] = gg[
    "AbnormalReturn_MarketModel_Industry2"
].cumsum()
Data["CAR_AbnormalReturn_WithoutAlpha_MarketMOdel_Industry2"] = gg[
    "AbnormalReturn_WithoutAlpha_MarketMOdel_Industry2"
].cumsum()
Data["RaiseType"] = np.nan
Data.loc[Data.JustRO == 1, "RaiseType"] = "JustRO"
Data.loc[Data.JustSaving == 1, "RaiseType"] = "JustSaving"
Data.loc[Data.JustPremium == 1, "RaiseType"] = "JustPremium"
Data.loc[Data.Hybrid == 1, "RaiseType"] = "Hybrid"
Data.loc[Data.Revaluation == 1, "RaiseType"] = "Revaluation"
#%%
def firstComponent(col):
    return abs(col - col.mean())


def periodMean(col):
    return col - col.mean()


def HMCalculation(df):
    df["br_ins"] = df.ins_buy_count / (df.ins_buy_count + df.ins_sell_count)
    df["br_ind"] = df.ind_buy_count / (df.ind_buy_count + df.ind_sell_count)
    df["br"] = (df.ind_buy_count +  df.ins_buy_count) / (df.ind_buy_count + df.ind_sell_count)
    gg = df.groupby(["date"])
    df["firstComponent_ins"] = gg["br_ins"].apply(firstComponent)
    df["firstComponent_ind"] = gg["br_ind"].apply(firstComponent)
    df["firstComponent"] = gg["br"].apply(firstComponent)
    gg = df.groupby(["date"])
    df["HM_ins"] = gg["firstComponent_ins"].apply(periodMean)
    df["HM_ind"] = gg["firstComponent_ind"].apply(periodMean)
    df["HM"] = gg["firstComponent_ind"].apply(periodMean)
    return df

Data = HMCalculation(Data)

# %%
df = pd.DataFrame()
df = df.append(Data)

df = df.groupby(["name"]).filter(lambda x: x.shape[0] >= 40)
df = df.groupby(["date","group_name"]).filter(lambda x: x.shape[0] >= 2)
mlist = ['CAR_4Factor',
         'CAR_Industry', 
         'CAR_WithoutAlpha_Industry',
         'CAR_MarketIndustry', 
         'CAR_MarketModel', 
         'CAR_WithoutAlpha_MarketModel',
         'CAR_MarketModel_Industry',
         'CAR_WithoutAlpha_MarketModel_Industry',
         'CAR_AbnormalReturn2', 
         'CAR_AbnormalReturn_Market2',
         'CAR_AbnormalReturn_WithoutAlpha2',
         'CAR_AbnormalReturn_Industry2',
         'CAR_AbnormalReturn_WithoutAlpha_Industry2', 
         'CAR_AbnormalReturn_MarketIndustry2',
         'CAR_AbnormalReturn_MarketModel2',
         'CAR_AbnormalReturn_WithoutAlpha_MarketModel2',
         'CAR_AbnormalReturn_MarketModel_Industry2', 
         'CAR_AbnormalReturn_WithoutAlpha_MarketMOdel_Industry2'
         ]
values = {}
for i in mlist:
    print(i)
    values[i] = (df[i].quantile(0.99),df[i].quantile(0.01))
for i in values:
    print(i)
    df = df[df[i]<=  values[i][0]]
    df = df[df[i]>=  values[i][1]]

#%%
d = path + "CapitalRaise.parquet"
df.to_parquet(d)

# %%
# d = path + "CapitalRaise.parquet"
# Data = pd.read_parquet(d)
df["year"] = round(df["ExtOrdGMDate"] / 10000).astype(int)
print(len(df))
df = df[df.JustPremium != 1]
print(len(df))
mlist = [
    "name",
    "EPeriod",
    "jalaliDate",
    "date",
    "title",
    "stock_id",
    "group_name",
    "group_id",
    "baseVol",
    "value",
    "quantity",
    "volume",
    "t",
    "CapBefore",
    "CapAfter",
    "ExtOrdGMDate",
    "Event",
    "JustRO",
    "JustSaving",
    "JustPremium",
    "Hybrid",
    "Revaluation",
    "Index",
    "RiskFree",
    "Market_return",
    "RelVolume",
    "SMB",
    "HML",
    "Winner_Loser",
    "industry_index",
    "Industry_return",
    "MarketCap",
    "Weight",
    "Amihud",
    "NetInd",
    "TotalInd",
    "NetIns",
    "TotalIns",
    "IndlImbalance",
    "InslImbalance",
    "ind_imbalance_count",
    "ins_imbalance_count",
    "ind_imbalance_volume",
    "ins_imbalance_volume",
    "ind_imbalance_value",
    "ins_imbalance_value",
    "ind_Nav",
    "ins_Nav",
    "CAR",
    "CAR_Market",
    "CAR_WithoutAlpha",
    "CAR_4Factor",
    "CAR_Industry",
    "CAR_WithoutAlpha_Industry",
    "CAR_MarketIndustry",
    "CAR_MarketModel",
    "CAR_WithoutAlpha_MarketModel",
    "CAR_MarketModel_Industry",
    "CAR_WithoutAlpha_MarketModel_Industry",
    "CAR_AbnormalReturn2",
    "CAR_AbnormalReturn_Market2",
    "CAR_AbnormalReturn_WithoutAlpha2",
    "CAR_AbnormalReturn_Industry2",
    "CAR_AbnormalReturn_WithoutAlpha_Industry2",
    "CAR_AbnormalReturn_MarketIndustry2",
    "CAR_AbnormalReturn_MarketModel2",
    "CAR_AbnormalReturn_WithoutAlpha_MarketModel2",
    "CAR_AbnormalReturn_MarketModel_Industry2",
    "CAR_AbnormalReturn_WithoutAlpha_MarketMOdel_Industry2",
    "RaiseType",
    'br_ins',
    'br_ind',
    'br',
    'firstComponent_ins',
    'firstComponent_ind',
    'firstComponent',
    'HM_ins',
    'HM_ind',
    'HM',
    "year",
]
df[mlist].to_csv(path + "CapitalRaise.csv", index=False)
print('Done')
# %%
df['under'] = 1/(1-df.Weight)
df[df.under >2][['name','date','Weight','under']].drop_duplicates(
    subset = ['name'])






# %%
