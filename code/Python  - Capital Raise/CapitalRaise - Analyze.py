#%%
import pandas as pd
import numpy as np

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"

n = path + "ARdata.parquet"

ARdata = pd.read_parquet(n)


#%%
Data = pd.DataFrame()
Data = Data.append(ARdata)
Data = Data.reset_index(drop=True)
Data["AdjustFactor"] = Data.close_price_Adjusted / Data.UnadjustedPrice
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

gg = Data.groupby(["name", "nEvent"])

Data["ind_stock_account"] = gg.ind_imbalance_volume.cumsum()
Data["ins_stock_account"] = gg.ins_imbalance_volume.cumsum()


#%%
gg = Data.groupby(["name", "nEvent"])


def adjust(g):
    print(g.name)
    l = g.EPeriod.to_list()
    if (len(g) < 20) | (-1 not in l):
        return g

    factor = (
        g[g.EPeriod == 0].AdjustFactor.iloc[0] / g[g.EPeriod == -1].AdjustFactor.iloc[0]
    )
    a = g[g.EPeriod == 0].NetInd.iloc[0]
    change = a * (factor - 1)

    g.loc[g.EPeriod > -1, "ind_stock_account"] = (
        g.loc[g.EPeriod > -1]["ind_stock_account"] + change
    )
    a = g[g.EPeriod == 0].NetIns.iloc[0]
    change = a * (factor - 1)

    g.loc[g.EPeriod > -1, "ins_stock_account"] = (
        g.loc[g.EPeriod > -1]["ins_stock_account"] + change
    )
    return g


# g = gg.get_group(('فولاد',1))
# g[g.EPeriod >-2][['AdjustFactor','name','EPeriod']]

Data = gg.apply(adjust)
#%%

Data["ind_stock_account"] = Data["ind_stock_account"] * Data["UnadjustedPrice"]
Data["ins_stock_account"] = Data["ins_stock_account"] * Data["UnadjustedPrice"]

gg = Data.groupby(["name", "nEvent"])
Data["ind_Cash_account"] = gg.ind_imbalance_value.cumsum()
Data["ins_Cash_account"] = gg.ins_imbalance_value.cumsum()

Data["ind_Cash_account"] = Data["ind_Cash_account"] * (-1)
Data["ins_Cash_account"] = Data["ins_Cash_account"] * (-1)

Data["ind_Nav"] = Data["ind_Cash_account"] + Data["ind_stock_account"]
Data["ins_Nav"] = Data["ins_Cash_account"] + Data["ins_stock_account"]

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
    df["br"] = (df.ind_buy_count + df.ins_buy_count) / (
        df.ind_buy_count + df.ind_sell_count
    )
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


#%%

# %%
df = pd.DataFrame()
df = df.append(Data)
gg = df.groupby(["name", "nEvent"])
df = gg.filter(lambda x: x.shape[0] >= 60)
# df = df.groupby(["date","group_name"]).filter(lambda x: x.shape[0] >= 2)
mlist = [
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
]
values = {}
for i in mlist:
    print(i)
    values[i] = (df[i].quantile(0.99), df[i].quantile(0.01))
for i in values:
    print(i)
    df = df[df[i] <= values[i][0]]
    df = df[df[i] >= values[i][1]]
t = df[df.EPeriod < 21]
print(len(t))
gg = t.groupby(["name", "nEvent"])
t = gg.filter(lambda x: x.shape[0] > 40)
print(len(t))
l = list(t.groupby(["name", "nEvent"]).groups.keys())
def check(g,l):
    if g.name in l:
        return g
    # print(g.name)
print(len(df))
gg = df.groupby(["name", "nEvent"])
df = gg.apply(check,l = l)

df = df[~df.Period.isnull()]
print(len(df))

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
    "br_ins",
    "br_ind",
    "br",
    "firstComponent_ins",
    "firstComponent_ind",
    "firstComponent",
    "HM_ins",
    "HM_ind",
    "HM",
    "year",
]
df[mlist].to_csv(path + "CapitalRaise.csv", index=False)
print("Done")
#%%
df["RaiseType2"] = 0
df.loc[df.RaiseType == "Revaluation", "RaiseType2"] = 1
df = df[df.EPeriod < 21]
gg = df.groupby(["name", "nEvent"])
t = gg.filter(lambda x: x.shape[0] > 40)
t = df

import seaborn as sns

sns.relplot(data=t[t.RaiseType2 == 0], kind="line", x="EPeriod", y="ind_Nav")
#