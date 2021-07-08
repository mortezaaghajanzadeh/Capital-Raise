#%%
import pandas as pd
import re
import numpy as np

path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)


def Qarter(df):
    df["Month"] = df.jalaliDate.astype(str).str[-4:-2].astype(int)
    df["Year"] = df.jalaliDate.astype(str).str[:4].astype(int)
    df["Qarter"] = df["Month"] % 3
    df.loc[df["Qarter"] != 0, "Qarter"] = (
        df.loc[df["Qarter"] != 0]["Month"] / 3
    ).astype(int) + 1
    df.loc[df["Qarter"] == 0, "Qarter"] = (
        df.loc[df["Qarter"] == 0]["Month"] / 3
    ).astype(int)
    df["YearQarter"] = df["Year"].astype(str) + df["Qarter"].astype(str)
    return df


def big(g):
    g["QuantileSize"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.MarketCap >= g.MarketCap.quantile((1 / 3) * (i - 1)), "QuantileSize"
        ] = i
    return g


def convert_ar_characters(input_str):

    mapping = {
        "ك": "ک",
        "گ": "گ",
        "دِ": "د",
        "بِ": "ب",
        "زِ": "ز",
        "ذِ": "ذ",
        "شِ": "ش",
        "سِ": "س",
        "ى": "ی",
        "ي": "ی",
    }
    return _multiple_replace(mapping, input_str)


def _multiple_replace(mapping, text):
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))


def vv5(row):
    X = row.split("/")
    return X[0]


def vv(row):
    X = row.split("-")
    return int(X[0] + X[1] + X[2])


def BM(g):
    g["QuantileBM"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.BookToMarket >= g.BookToMarket.quantile((1 / 3) * (i - 1)),
            "QuantileBM",
        ] = i
    return g


def PE(g):
    g["QuantilePE"] = np.nan
    t = g
    g = t[~t["P/E"].isnull()]
    for i in range(1, 4):
        g.loc[
            g["P/E"] >= g["P/E"].quantile((1 / 3) * (i - 1)),
            "QuantilePE",
        ] = i
    mapdict = dict(zip(g["name"], g.QuantilePE))
    t["QuantilePE"] = t["name"].map(mapdict)
    return t


def Float(g):
    g["QuantileFreeFloat"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.freeFloat >= g.freeFloat.quantile((1 / 3) * (i - 1)),
            "QuantileFreeFloat",
        ] = i
    return g


def FloatCap(g):
    g["QuantileFreeFloatCap"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.freeMarketCap >= g.freeMarketCap.quantile((1 / 3) * (i - 1)),
            "QuantileFreeFloatCap",
        ] = i
    return g


def volatility(g):
    g["QuantileVolatility"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.volatility >= g.volatility.quantile((1 / 3) * (i - 1)),
            "QuantileVolatility",
        ] = i
    return g


def Debt(g):
    g["QuantileDebtRatio"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.DebtRatio >= g.DebtRatio.quantile((1 / 3) * (i - 1)),
            "QuantileDebtRatio",
        ] = i
    return g


def Leverage(g):
    g["QuantileLeverageRatio"] = np.nan
    for i in range(1, 4):
        g.loc[
            g.LeverageRatio >= g.LeverageRatio.quantile((1 / 3) * (i - 1)),
            "QuantileLeverageRatio",
        ] = i
    return g


#%%
Data.columns

Data[
    [
        "Beta_CAPM",
        "Alpha_CAPM",
        "betaM_FOUR",
        "betaS_FOUR",
        "betaH_FOUR",
        "betaW_FOUR",
        "Alpha_FOUR",
    ]
].describe().T


# %%
df = Data[Data.EPeriod == 0]
df = df[
    [
        "jalaliDate",
        "date",
        "name",
        "group_name",
        "close_price",
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
        "AbnormalReturn",
        "AbnormalReturn_4Factor",
        "RaiseType",
    ]
]
df["MarketCap"] = df.close_price * df.CapBefore
df = Qarter(df)
print(len(df))


# %%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
n2 = path + "\\Rahavard Novin - 70-97" + ".parquet"
df2 = pd.read_parquet(n2)
t = (
    df2[["تاریخ", "نماد", "P/E"]]
    .rename(columns={"نماد": "name", "تاریخ": "jalaliDate"})
    .dropna()
)
col = "name"
t[col] = t[col].apply(lambda x: convert_ar_characters(x))
t["Year"] = t["jalaliDate"].apply(vv5).astype(int)
t = t.drop(columns=["jalaliDate"])
t = t.drop_duplicates(subset=["name", "Year"], keep="last")

df = df.merge(t, on=["name", "Year"], how="left")
# df = df[~(df["P/E"].isnull())]


# %%
index = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\IRX6XTPI0009.xls"
index = pd.read_excel(index)[["<CLOSE>", "<COL14>"]].rename(
    columns={"<COL14>": "jalaliDate", "<CLOSE>": "index"}
)
index = Qarter(index)
Qindex = index.groupby("YearQarter").last()
Qindex["QRet"] = (
    index.groupby("YearQarter").last()["index"]
    - index.groupby("YearQarter").first()["index"]
)
Qindex["QRet"] = Qindex["QRet"] / Qindex["index"]
Qindex["Good"] = 0
Qindex.loc[Qindex["QRet"] > 0, "Good"] = 1
Qindex["Bad"] = 0
Qindex.loc[Qindex["Good"] == 0, "Bad"] = 1
Qindex = Qindex.reset_index()
mapdict = dict(zip(Qindex.YearQarter, Qindex.Good))
df["Good"] = df.YearQarter.map(mapdict)
mapdict = dict(zip(Qindex.YearQarter, Qindex.Bad))
df["Bad"] = df.YearQarter.map(mapdict)


# %%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"

n2 = path + "\\balance sheet - 9811" + ".xlsx"
df2 = pd.read_excel(n2)
df2 = df2.iloc[:, [0, 4, 13, 16, 18]]
df2.rename(
    columns={
        df2.columns[0]: "symbol",
        df2.columns[1]: "date",
        df2.columns[2]: "BookValue",
        df2.columns[3]: "Debt",
        df2.columns[4]: "Capital",
    },
    inplace=True,
)
df2["year"] = df2["date"].apply(vv5).astype(int)
col = "symbol"
df2[col] = df2[col].apply(lambda x: convert_ar_characters(x))

df2["DebtRatio"] = df2.Debt / df2.BookValue
df2["LeverageRatio"] = df2.Debt / df2.Capital

fkey = zip(df2.symbol, df2.year)
mapdict = dict(zip(fkey, df2.BookValue))
df["BookValue"] = df.set_index(["name", "Year"]).index.map(mapdict)
df["BookValue"] = df["BookValue"].fillna(method="ffill")
df["BookToMarket"] = (df["MarketCap"] / df["BookValue"]) / 1e6

fkey = zip(df2.symbol, df2.year)
mapdict = dict(zip(fkey, df2.DebtRatio))
df["DebtRatio"] = df.set_index(["name", "Year"]).index.map(mapdict)

fkey = zip(df2.symbol, df2.year)
mapdict = dict(zip(fkey, df2.LeverageRatio))
df["LeverageRatio"] = df.set_index(["name", "Year"]).index.map(mapdict)

#%%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
df2 = pd.read_csv(path + "BlockHolders - 800308-990528 - Annual" + ".csv")
a = df2.groupby(["symbol", "year"]).Percent.sum()
df2 = df2.groupby(["symbol", "year"]).first()
df2 = df2[["stock_id"]]
df2["free"] = 100 - a
df2 = df2.reset_index()
fkey = zip(df2.symbol, df2.year)
mapdict = dict(zip(fkey, df2.free))
df["freeFloat"] = df.set_index(["name", "Year"]).index.map(mapdict)
df["freeMarketCap"] = df["freeFloat"] * df["MarketCap"] / 100
#%%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\\"
df2 = pd.read_csv(path + "Stocks_Prices_1399-09-24.csv")
id = df2[["name", "stock_id"]].drop_duplicates()
col = "name"
id[col] = id[col].apply(lambda x: convert_ar_characters(x))
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
df2 = pd.read_csv(path + "adjPrices_1399-11-06.csv")
df2.Date = df2.Date.apply(vv)
df2 = df2.drop(columns="Unnamed: 0").rename(columns={"ID": "stock_id", "Date": "date"})
mapdict = dict(zip(id.stock_id, id.name))
df2["name"] = df2.stock_id.map(mapdict)
gg = df2.groupby("name")


def vol(g):
    return g.rolling(250).std()


df2["volatility"] = gg["close"].apply(vol)
fkey = zip(df2.date, df2.name)
mapdict = dict(zip(fkey, df2.volatility))
df["volatility"] = df.set_index(["date", "name"]).index.map(mapdict)

#%%
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(BM)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(PE)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(big)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(Float)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(FloatCap)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(volatility)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(Debt)
gg = df.groupby(["Year", "Revaluation"])
df = gg.apply(Leverage)


#%%
path = r"H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise_Analyze.xlsx"
df.to_excel(d, index=False)

#%%


# %%
t = df.groupby("QuantilePE").AbnormalReturn.describe()
t["Cluster"] = "P/E"
m = df.groupby("QuantileBM").AbnormalReturn.describe()
m["Cluster"] = "B/M"
t = t.append(m)

m = df.groupby("QuantileSize").AbnormalReturn.describe()
m["Cluster"] = "Size"
t = t.append(m)

m = df.groupby("QuantileFreeFloat").AbnormalReturn.describe()
m["Cluster"] = "FreeFloat"
t = t.append(m)

m = df.groupby("QuantileFreeFloatCap").AbnormalReturn.describe()
m["Cluster"] = "FreeFloatCap"
t = t.append(m)

m = df.groupby("QuantileVolatility").AbnormalReturn.describe()
m["Cluster"] = "Volatility"
t = t.append(m)
m = df.groupby("QuantileDebtRatio").AbnormalReturn.describe()
m["Cluster"] = "DebtRatio"
t = t.append(m)

m = df.groupby("QuantileLeverageRatio").AbnormalReturn.describe()
m["Cluster"] = "LeverageRatio"
t = t.append(m)

m = df.groupby("Bad").AbnormalReturn.describe()
m["Cluster"] = "Bad"
t = t.append(m)
t_f = t.reset_index(drop=True)

t = df.groupby("QuantilePE").AbnormalReturn_4Factor.describe()
t["Cluster"] = "P/E"
m = df.groupby("QuantileBM").AbnormalReturn_4Factor.describe()
m["Cluster"] = "B/M"
t = t.append(m)

m = df.groupby("QuantileSize").AbnormalReturn_4Factor.describe()
m["Cluster"] = "Size"
t = t.append(m)

m = df.groupby("QuantileFreeFloat").AbnormalReturn_4Factor.describe()
m["Cluster"] = "FreeFloat"
t = t.append(m)

m = df.groupby("QuantileFreeFloatCap").AbnormalReturn_4Factor.describe()
m["Cluster"] = "FreeFloatCap"
t = t.append(m)

m = df.groupby("QuantileVolatility").AbnormalReturn_4Factor.describe()
m["Cluster"] = "Volatility"
t = t.append(m)

m = df.groupby("QuantileDebtRatio").AbnormalReturn_4Factor.describe()
m["Cluster"] = "DebtRatio"
t = t.append(m)

m = df.groupby("QuantileLeverageRatio").AbnormalReturn_4Factor.describe()
m["Cluster"] = "LeverageRatio"
t = t.append(m)
m = df.groupby("Bad").AbnormalReturn_4Factor.describe()
m["Cluster"] = "Bad"
t = t.append(m)
t.reset_index(drop=True)

# %%

# %%
