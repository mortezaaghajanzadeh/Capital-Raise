#%%
import pandas as pd
import numpy as np


def to_latex_file(df, path, name):
    with open(path + name + ".tex", "w") as tf:
        tf.write(df.to_latex())


path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
d = path + "CapitalRaise.parquet"
Data = pd.read_parquet(d)
path2 = r"D:\Dropbox\Capital Raise\Capital-Raise\Report\Output\\"
Data["year"] = round(Data["ExtOrdGMDate"] / 10000).astype(int)
# %%
df = pd.DataFrame()
df = df.append(
    Data[
        [
            "name",
            "jalaliDate",
            "IndlImbalance",
            "InslImbalance",
            "CAR_4Factor",
            "t",
            "EPeriod",
            "nEvent",
            "HM_ins",
            "HM_ind",
            "year",
        ]
    ]
)
df = df.rename(columns={"CAR_4Factor": "CAR"})

# Average of daily Individual Imbalance
mapdf = df.groupby(["t"]).IndlImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index, mapdf["IndlImbalance"]))
df["IndNT_Im"] = df.t.map(mapdict)
df["IndNT_Im"] = df.IndlImbalance - df.IndNT_Im
# Average of daily Institutional Imbalance
mapdf = df.groupby(["t"]).InslImbalance.mean().to_frame()
mapdict = dict(zip(mapdf.index, mapdf["InslImbalance"]))
df["InsNT_Im"] = df.t.map(mapdict)
df["InsNT_Im"] = df.InslImbalance - df.IndNT_Im
# Average of daily Institutional Herd
mapdf = df.groupby(["t"]).HM_ins.mean().to_frame()
mapdict = dict(zip(mapdf.index, mapdf["HM_ins"]))
df["InsNT_Hm"] = df.t.map(mapdict)
df["InsNT_Hm"] = df.HM_ins - df.InsNT_Hm

# Average of daily Individual Herd
mapdf = df.groupby(["t"]).HM_ind.mean().to_frame()
mapdict = dict(zip(mapdf.index, mapdf["HM_ind"]))
df["IndNT_Hm"] = df.t.map(mapdict)
df["IndNT_Hm"] = df.HM_ind - df.IndNT_Hm


df = df.replace(np.nan, 0)
t = pd.DataFrame()
t = t.append(df[(df.EPeriod < 0) & (df.EPeriod > -11)])
t["InsNT_Im"] = t.groupby(["name", "nEvent"]).InsNT_Im.cumsum().to_frame()
t["IndNT_Im"] = t.groupby(["name", "nEvent"]).IndNT_Im.cumsum().to_frame()
t["InsNT_Hm"] = t.groupby(["name", "nEvent"]).InsNT_Hm.cumsum().to_frame()
t["IndNT_Hm"] = t.groupby(["name", "nEvent"]).IndNT_Hm.cumsum().to_frame()


t = t[
    [
        "name",
        "EPeriod",
        "nEvent",
        "InsNT_Im",
        "IndNT_Im",
        "InsNT_Hm",
        "IndNT_Hm",
        "year",
    ]
]
t = t[t.EPeriod == -1.0][
    ["name", "nEvent", "InsNT_Im", "IndNT_Im", "InsNT_Hm", "IndNT_Hm", "year"]
]
gg = df.groupby(["name", "nEvent"])


def CAR(g):
    print(g.name)
    if len(g) < 40:
        return
    a = {}

    try:
        b = g.loc[g.EPeriod == -1].CAR.iloc[0] - g.loc[g.EPeriod == -10].CAR.iloc[0]
    except:
        b = np.nan

    a["(-10)-(-1)"] = b
    try:
        b = g.loc[g.EPeriod == 1].CAR.iloc[0] - g.loc[g.EPeriod == -1].CAR.iloc[0]
    except:
        b = np.nan

    a["0-1"] = b

    try:
        b = g.loc[g.EPeriod == 6].CAR.iloc[0] - g.loc[g.EPeriod == 1].CAR.iloc[0]
    except:
        b = np.nan
    a["2-6"] = b
    try:
        b = g.loc[g.EPeriod == 11].CAR.iloc[0] - g.loc[g.EPeriod == 1].CAR.iloc[0]
    except:
        b = np.nan
    a["2-11"] = b
    try:
        b = g.loc[g.EPeriod == 50].CAR.iloc[0] - g.loc[g.EPeriod == 1].CAR.iloc[0]
    except:
        b = np.nan
    a["2-50"] = b
    try:
        b = g.loc[g.EPeriod == 50].CAR.iloc[0] - g.loc[g.EPeriod == -1].CAR.iloc[0]
    except:
        b = np.nan
    a["0-50"] = b
    return a["(-10)-(-1)"], a["0-1"], a["2-6"], a["2-11"], a["2-50"], a["0-50"]


df = gg.apply(CAR).to_frame().reset_index()
df["(-10)-(-1)"], df["0-1"], df["2-6"], df["2-11"], df["2-50"], df["0-50"] = df[0].str
df = df.drop(columns=[0])
df = df.merge(t, on=["name", "nEvent"])
# %%
def BG(df):
    pathBG = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Control Right - Cash Flow Right\\"
    # pathBG = r"C:\Users\RA\Desktop\RA_Aghajanzadeh\Data\\"
    n = pathBG + "Grouping_CT.xlsx"
    BG = pd.read_excel(n)
    BGroup = set(BG["uo"])
    names = sorted(BGroup)
    ids = range(len(names))
    mapingdict = dict(zip(names, ids))
    BG["BGId"] = BG["uo"].map(mapingdict)

    BG = BG.groupby(["uo", "year"]).filter(lambda x: x.shape[0] >= 3)
    for i in ["uo", "cfr", "cr"]:
        print(i)
        fkey = zip(list(BG.symbol), list(BG.year))
        mapingdict = dict(zip(fkey, BG[i]))
        df[i] = df.set_index(["name", "year"]).index.map(mapingdict)
    return df


df = BG(df)
df["Grouped"] = 0
df.loc[~df.uo.isnull(), "Grouped"] = 1
df["Excess"] = df.cr - df.cfr
#%%
def Quantiling(g, num, name):
    g["Quantile" + name] = np.nan
    for i in range(1, num + 1):
        g.loc[
            g[name] >= g[name].quantile((1 / num) * (i - 1)),
            "Quantile" + name,
        ] = i
    return g


for i in ["InsNT_Im", "IndNT_Im", "InsNT_Hm", "IndNT_Hm", "Excess"]:
    print(i)
    df = Quantiling(df, 3, i)

df = CAR(df, num=3)


#%%
for i in ["InsNT_Im", "IndNT_Im", "InsNT_Hm", "IndNT_Hm", "Excess"]:
    i = "Quantile" + i
    print(i[8:])
    t = df.groupby(i)[["0-1", "2-6", "2-11", "2-50", "0-50"]].mean()
    t.index.names = [i[8:]]
    to_latex_file(t.round(2), path2, i)

# %%
name = "table1"
t = pd.crosstab(
    df.QuantileInsNT_Im, df["CAR(-10,-1)"], values=df["0-50"], aggfunc="mean"
)
t.index.names = ["InsNT_Im"]
to_latex_file(t.round(2), path2, name)
t
# %%
name = "table2"
t = pd.crosstab(
    df.QuantileIndNT_Im, df["CAR(-10,-1)"], values=df["0-50"], aggfunc="mean"
)
t.index.names = ["IndNT_Im"]
to_latex_file(t.round(2), path2, name)
t
#%%

#%%
t = df.groupby("Grouped")[["0-1", "2-6", "2-11", "2-50", "0-50"]].mean()
to_latex_file(t.round(2), path2, "Grouped")
#%%


#%%
d = path + "CapitalRaise_Analyze.csv"
df.to_csv(d, index=False)
