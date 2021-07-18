#%%
import pandas as pd

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)

Data["year"] = round(Data["ExtOrdGMDate"] / 10000).astype(int)
print(len(Data))
Data = Data[Data.JustPremium != 1]
print(len(Data))
# Data = Data[Data.year > 1390]
#%%


def Result(g, CAR):
    AAR = (
        g.groupby("EPeriod")
        .AbnormalReturn.mean()
        .to_frame()
        .rename(columns={"AbnormalReturn": "AAR"})
    )
    AAR["CAAR"] = g.groupby("EPeriod")[CAR].mean()
    AAR["CAAR_05"] = g.groupby("EPeriod")[CAR].quantile(0.05)
    AAR["CAAR_95"] = g.groupby("EPeriod")[CAR].quantile(0.95)
    AAR["Size"] = g.groupby("EPeriod").size()

    g = g.merge(AAR.reset_index(), on="EPeriod").sort_values(by=["name", "date"])
    g["std"] = (g["CAR"] - g["CAAR"]) * (g["CAR"] - g["CAAR"]) / (g["Size"] - 1)
    AAR["std"] = (g.groupby("EPeriod")["std"].sum()) ** 0.5
    AAR["t"] = AAR["Size"] ** 0.5 * AAR["CAAR"] / AAR["std"]
    return AAR


gg = Data.groupby("RaiseType")
t1 = gg.apply(Result, CAR="CAR")
t = Result(Data, "CAR").reset_index()
t["RaiseType"] = "Total"
t1 = t1.reset_index()
t1 = t1.append(t).reset_index(drop=True)
CAR = t1

gg = Data.groupby("RaiseType")
t1 = gg.apply(Result, CAR="CAR_4Factor")
t = Result(Data, "CAR_4Factor").reset_index()
t["RaiseType"] = "Total"
t1 = t1.reset_index()
t1 = t1.append(t).reset_index(drop=True)
CAR_4Factor = t1

gg = Data.groupby("RaiseType")
t1 = gg.apply(Result, CAR="CAR_Market")
t = Result(Data, "CAR_Market").reset_index()
t["RaiseType"] = "Total"
t1 = t1.reset_index()
t1 = t1.append(t).reset_index(drop=True)
CAR_Market = t1

gg = Data.groupby("RaiseType")
t1 = gg.apply(Result, CAR="CAR_WithoutAlpha")
t = Result(Data, "CAR_WithoutAlpha").reset_index()
t["RaiseType"] = "Total"
t1 = t1.reset_index()
t1 = t1.append(t).reset_index(drop=True)
CAR_WithoutAlpha = t1


gg = Data.groupby("RaiseType")


def Result(g):
    t = g.groupby("EPeriod").IndlImbalance.mean().to_frame().reset_index()
    t = (
        t.merge(g.groupby("EPeriod").InslImbalance.mean().to_frame().reset_index())
        .merge(g.groupby("EPeriod").Amihud.mean().to_frame().reset_index())
        .merge(g.groupby("EPeriod").volume.mean().to_frame().reset_index())
        .merge(g.groupby("EPeriod").RelVolume.mean().to_frame().reset_index())
    )
    return t


t1 = gg.apply(Result).reset_index().drop(columns=["level_1"])
t = Result(Data).reset_index(drop=True)
t["RaiseType"] = "Total"
t1 = t1.append(t).reset_index(drop=True)
t = Result(Data[Data.Revaluation != 1]).reset_index(drop=True)
t["RaiseType"] = "NoRevaluation"
t1 = t1.append(t).reset_index(drop=True)


n = path + "TradeSumm.xlsx"
t1.to_excel(n, index=False)


n = path + "CAAR.xlsx"
n1 = path + "CAAR_4Factor.xlsx"
n2 = path + "CAAR_Market.xlsx"
n3 = path + "CAAR_WithoutAlpha.xlsx"
CAR.to_excel(n, index=False)
CAR_4Factor.to_excel(n1, index=False)
CAR_Market.to_excel(n2, index=False)
CAR_WithoutAlpha.to_excel(n3, index=False)

#%%

import seaborn as sns
from matplotlib import pyplot as plt


# %%
g = sns.relplot(data=Data, kind="line", x="EPeriod", y="CAR", col="RaiseType")
g = sns.relplot(data=Data, kind="line", x="EPeriod", y="CAR_4Factor", col="RaiseType")
g = sns.relplot(data=Data, kind="line", x="EPeriod", y="InslImbalance")
g = sns.relplot(
    data=Data, kind="line", x="EPeriod", y="CAR_WithoutAlpha", col="RaiseType"
)
g = sns.relplot(data=Data, kind="line", x="EPeriod", y="CAR_Market", col="RaiseType")


#%%


def Result(g, CAR):
    AAR = (
        g.groupby("EPeriod")
        .AbnormalReturn.mean()
        .to_frame()
        .rename(columns={"AbnormalReturn": "AAR"})
    )
    AAR["CAAR"] = g.groupby("EPeriod")[CAR].mean()
    AAR["CAAR_05"] = g.groupby("EPeriod")[CAR].quantile(0.05)
    AAR["CAAR_95"] = g.groupby("EPeriod")[CAR].quantile(0.95)
    AAR["Size"] = g.groupby("EPeriod").size()

    g = g.merge(AAR.reset_index(), on="EPeriod").sort_values(by=["name", "date"])
    g["std"] = (g["CAR"] - g["CAAR"]) * (g["CAR"] - g["CAAR"]) / (g["Size"] - 1)
    AAR["std"] = (g.groupby("EPeriod")["std"].sum()) ** 0.5
    AAR["t"] = AAR["Size"] ** 0.5 * AAR["CAAR"] / AAR["std"]
    return AAR


gg = Data.groupby(["RaiseType", "year"])
t1 = gg.apply(Result, CAR="CAR").reset_index()

gg = Data.groupby(["year"])
t = gg.apply(Result, CAR="CAR").reset_index()
t["RaiseType"] = "Total"


gg = Data[Data.Revaluation != 1].groupby(["year"])
t2 = gg.apply(Result, CAR="CAR").reset_index()
t2["RaiseType"] = "NoRevaluation"

result = (
    t1.append(t2)
    .append(t)
    .sort_values(by=["year", "RaiseType"])
    .dropna()
    .reset_index(drop=True)
)
n = path + "CAAR_year.xlsx"
result.dropna().to_excel(n, index=False)


# %%
