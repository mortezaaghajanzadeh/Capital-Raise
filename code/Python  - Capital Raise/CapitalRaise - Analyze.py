# %%
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import finance_byu.rolling as rolling
import requests
import pandas as pd
from bs4 import BeautifulSoup
import math


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


def vv(row):
    X = row.split("-")
    return int(X[0] + X[1] + X[2])


def vv2(row):
    X = row.split("/")
    return int(X[0] + X[1] + X[2])

def addDash(row):
    row = str(row)
    X = [1, 1, 1]
    X[0] = row[0:4]
    X[1] = row[4:6]
    X[2] = row[6:8]
    return X[0] + "-" + X[1] + "-" + X[2]


def removeSlash(row):
    X = row.split("/")
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return int(X[0] + X[1] + X[2])

def removeSlash2(row):
    X = row.split("/")
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[0]) < 2:
        X[0] = "0" + X[0]
        
    return int(X[2] + X[0] + X[1])
def removeDash(row):
    X = row.split("-")
    if len(X[1]) < 2:
        X[1] = "0" + X[1]
    if len(X[2]) < 2:
        X[2] = "0" + X[2]
    return int(X[0] + X[1] + X[2])

path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
#%%
def group_id():
    r = requests.get(
        "http://www.tsetmc.com/Loader.aspx?ParTree=111C1213"
    )  # This URL contains all sector groups.
    soup = BeautifulSoup(r.text, "html.parser")
    header = soup.find_all("table")[0].find("tr")
    list_header = []
    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
    data = []
    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)
    df = pd.DataFrame(data=data, columns=list_header).rename(
        columns = {
            'گروه های صنعت':'group_name',
            "کد گروه های صنعت":"group_id"
        }
    )
    return df                  
groupnameid = group_id()
# %%
df2 = pd.read_csv(path + "adjPrices_1399-11-06.csv")
df2.Date = df2.Date.apply(vv)
df2 = df2.drop(columns="Unnamed: 0").rename(
    columns={"ID": "stock_id", "Date": "date"})
pdf = pd.read_parquet(path + "Stocks_Prices_1400-04-27.parquet")
mapdict = dict(zip(groupnameid.group_name,groupnameid.group_id))
pdf['group_id'] = pdf.group_name.map(mapdict)
pdf.loc[pdf.name.str[-1] == " ", "name"] = pdf.loc[pdf.name.str[-1] == " "].name.str[
    :-1
]
pdf.loc[pdf.name.str[0] == " ", "name"] = pdf.loc[pdf.name.str[0] == " "].name.str[1:]
pdf["name"] = pdf["name"].apply(lambda x: convert_ar_characters(x))
pdf.jalaliDate = pdf.jalaliDate.apply(vv)
pdf = pdf.sort_values(by=["name", "date"])
pdf = pdf[~((pdf.title.str.startswith("ح")) & (pdf.name.str.endswith("ح")))]
pdf = pdf[~(pdf.name.str.endswith("پذيره"))]

pdf = pdf[~(pdf.group_name == "صندوق سرمايه گذاري قابل معامله")]
# pdf = pdf[
#     [
#         "jalaliDate",
#         "date",
#         "name",
#         "title",
#         "stock_id",
#         "group_name",
#         "group_id",
#         "baseVol",
#         "value",
#         "volume",
#         "quantity",
#     ]
# ]
col = "name"
pdf[col] = pdf[col].apply(lambda x: convert_ar_characters(x))
adData = pd.read_csv(path + "DataAdjustedEvent.csv")
adData = adData.rename(columns = {
    'قبل از تعدیل' : 'Before',
    "تعدیل شده":"After",
    "تاریخ":"jalaliDate"
}).sort_values(by = ['stock_id','jalaliDate'])
#%%
gg = adData.groupby('stock_id')

def clean(g):
    g.loc[g.After == 1,"After"] = np.nan
    g.loc[g.Before == 1,"Before"] = np.nan
    g["After"] = g["After"].fillna(method="bfill")
    g["Before"] = g["Before"].fillna(method="ffill")
    return g
adData = gg.apply(clean)
adData['AdjustFactor'] = adData.After / adData.Before

i = 'stock_id'
pdf[i] = pdf[i].astype(str)
adData[i] = adData[i].astype(str)
i = 'jalaliDate'
pdf[i] = pdf[i].astype(int)
adData[i] = adData[i].astype(int)

pdf = pdf.merge(adData[['jalaliDate','stock_id','AdjustFactor']]
          ,on = ['jalaliDate','stock_id'],how = 'outer')
gg = pdf.groupby('stock_id')
pdf["AdjustFactor"] = gg["AdjustFactor"].fillna(method="ffill")
pdf = pdf[~pdf.date.isnull()]
pdf['AdjustFactor'] = pdf.AdjustFactor.fillna(1)
shrout = pd.read_csv(path + "shrout.csv")
mapdict = dict(zip(shrout.set_index(['name','date']).index,shrout.shrout))
i = 'date'
pdf[i] = pdf[i].astype(int)

pdf['shrout'] = pdf.set_index(['name','date']).index.map(mapdict)
i = 'stock_id'
shrout[i] = shrout[i].astype(str)
mapdict = dict(zip(shrout.set_index(['stock_id','date']).index,shrout.shrout))
pdf['shrout2'] = pdf.set_index(['stock_id','date']).index.map(mapdict)
pdf.loc[pdf.shrout.isnull(),'shrout'] = pdf.loc[pdf.shrout.isnull()]['shrout2']
pdf = pdf.drop(columns = ['shrout2'])
gg = pdf.groupby('name')
pdf["shrout"] = gg["shrout"].fillna(method="ffill")
i = 'volume'
pdf[i] = pdf[i].astype(float)
# d = pdf[pdf.volume>0]
d = pd.DataFrame()
d = d.append(pdf)
gg = d.groupby('name')
d["shrout"] = gg["shrout"].fillna(method="bfill")
#%%
pdf = pd.DataFrame()
pdf = pdf.append(d[~d.shrout.isnull()])
pdf = pdf[pdf.jalaliDate<13990000]
pdf = pdf[pdf.jalaliDate>13900000]
#%%
gg = pdf.groupby('name')



#%%
i = 'group_id'
pdf[i] = pdf[i].astype(float)
i = 'close_price'
pdf[i] = pdf[i].astype(float)

pdf.head()
pdf['close'] = pdf.close_price /pdf.AdjustFactor
gg = pdf.groupby(["name"])
pdf['return'] = gg.close.pct_change()*100
pdf['MarketCap'] = pdf.close_price * pdf.shrout


gg = pdf.groupby(["date", "group_id"])

def marketCapAndWeight(g):
    # print(g.name[0], end="\r", flush=True)
    if len(g) < 3:
        return
    g["Weight"] = g.MarketCap / (g.MarketCap.sum())
    g['industry_return'] = (g['return'] * g["Weight"]).sum()
    return g
data2 = gg.apply(marketCapAndWeight)
#%%
pdf2 = pd.DataFrame()
pdf2 = pdf2.append(data2).reset_index(drop = True).sort_values(by = [
    'name','date'
])
pdf2.isnull().sum()
pdf2['industry_index'] = 1
first = pdf2.groupby(['group_id','date']).first()[
    [
        'group_name',
        'industry_return',
        'industry_index'
    ]
].reset_index()


    

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

# pdf['Firm'] = ''
# pdf.loc[pdf.title.str.contains("\("),'Firm'] = pdf[pdf.title.str.contains("\(")]['title'].str.split("\(", n = 1, expand = True)[0]
# firmsymbol = pdf[['name','Firm']].drop_duplicates()


# %%
gg = pdf.groupby(["name"])
pdf["close"] = gg["close"].fillna(method="ffill")
pdf["High"] = gg["High"].fillna(method="ffill")
pdf["Low"] = gg["Low"].fillna(method="ffill")
pdf["Open"] = gg["Open"].fillna(method="ffill")
pdf["Last"] = gg["Last"].fillna(method="ffill")
pdf.loc[pdf.volume == 0, "Volume"] = 0

#%%
df2 = pd.read_csv(path + "InsInd_1399-05-09" + ".csv")
# df2["Name"] = df2["Name"].apply(lambda x: convert_ar_characters(x))
df2.Date = df2.Date.apply(vv)
df2 = df2.rename(columns={"ID": "stock_id", "Date": "date"}).drop(
    columns=["Unnamed: 0", "Name"]
)
print(len(pdf), len(df2))

pdf = pdf.merge(df2, on=["stock_id", "date"], how="left")
print(len(pdf))


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
data = data[~data.High.isnull()]
gg = data.groupby("name")
data["Market_return"] = gg["Index"].pct_change(periods=1) * 100
data = data[~data.Market_return.isnull()]
data = data.rename(columns={"close": "close_price"})
# %%

# %%


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

n = path + "RawDataBeforeAb.parquet"

data.to_parquet(n)


#%%
data = pd.read_parquet(path + "RawDataBeforeAb.parquet")

# %%
def ABnormal(g, Rlag):
    lag = 121 + Rlag
    print(g.name)
    a = pd.DataFrame()
    a = a.append(g)
    a = a.dropna()
    a = a.reset_index(drop=True).reset_index().rename(columns={"index": "Period"})
    a["Period"] = a["Period"].astype(int)
    a["AbnormalReturn"] = np.nan
    a["AbnormalReturn_Market"] = np.nan
    a["AbnormalReturn_WithoutAlpha"] = np.nan
    a["AbnormalReturn_4Factor"] = np.nan

    a["EPeriod"] = np.nan
    a["nEvent"] = np.nan
    a["Beta_CAPM"] = np.nan
    a["Alpha_CAPM"] = np.nan

    a["Beta_CAPMIndustry"] = np.nan
    a["Alpha_CAPMIndustry"] = np.nan
    a["BetaI_CAPMIndustry"] = np.nan

    a["Beta_Market"] = np.nan
    a["Alpha_Market"] = np.nan
    a["Beta_MarketIndustry"] = np.nan
    a["Alpha_MarketIndustry"] = np.nan
    a["BetaI_MarketIndustry"] = np.nan

    a["AbnormalReturn_Industry"] = np.nan
    a["AbnormalReturn_WithoutAlpha_Industry"] = np.nan
    a["AbnormalReturn_MarketIndustry"] = np.nan
    a["AbnormalReturn_MarketModel"] = np.nan
    a["AbnormalReturn_WithoutAlpha_MarketModel"] = np.nan
    a["AbnormalReturn_MarketModel_Industry"] = np.nan
    a["AbnormalReturn_WithoutAlpha_MarketModel_Industry"] = np.nan

    a["betaM_FOUR"] = np.nan
    a["betaS_FOUR"] = np.nan
    a["betaH_FOUR"] = np.nan
    a["betaW_FOUR"] = np.nan
    a["Alpha_FOUR"] = np.nan

    a["AbnormalReturn2"] = np.nan
    a["AbnormalReturn_Market2"] = np.nan
    a["AbnormalReturn_WithoutAlpha2"] = np.nan

    a["Beta_CAPM2"] = np.nan
    a["Alpha_CAPM2"] = np.nan

    a["Beta_CAPMIndustry2"] = np.nan
    a["Alpha_CAPMIndustry2"] = np.nan
    a["BetaI_CAPMIndustry2"] = np.nan

    a["Beta_Market2"] = np.nan
    a["Alpha_Market2"] = np.nan
    a["Beta_MarketIndustry2"] = np.nan
    a["Alpha_MarketIndustry2"] = np.nan
    a["BetaI_MarketIndustry2"] = np.nan

    nEvent = 0
    for i in a[a.Event == a.t]["Period"]:
        nEvent += 1
        tempt = pd.DataFrame()
        tempt = a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag))]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "EPeriod"] = (
            tempt["Period"] - i
        )
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "nEvent"] = nEvent

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "JustRO"] = a[
            a.Period == i
        ]["JustRO"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "JustSaving"] = a[
            a.Period == i
        ]["JustSaving"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "JustPremium"] = a[
            a.Period == i
        ]["JustPremium"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Hybrid"] = a[
            a.Period == i
        ]["Hybrid"].iloc[0]
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Revaluation"] = a[
            a.Period == i
        ]["Revaluation"].iloc[0]

        estimation_window = a.loc[a.EPeriod < -1 * Rlag]
        if len(estimation_window) < 30:
            continue

        # CAPM
        alpha, beta = ols(estimation_window)

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn"
        ] = tempt["Return"] - (tempt["RiskFree"] + alpha + beta * tempt["EMR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha",
        ] = tempt["Return"] - (tempt["RiskFree"] + beta * tempt["EMR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn_Market"
        ] = tempt["Return"] - (tempt["RiskFree"] + tempt["EMR"])

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_CAPM"] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_CAPM"] = beta

        # CAPM + Industry

        alpha, beta, betaI = olsIndustry(estimation_window)
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn_Industry"
        ] = tempt["Return"] - (
            tempt["RiskFree"] + alpha + beta * tempt["EMR"] + betaI * tempt["EIR"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha_Industry",
        ] = tempt["Return"] - (
            tempt["RiskFree"] + beta * tempt["EMR"] + betaI * tempt["EIR"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_MarketIndustry",
        ] = tempt["Return"] - (2 * tempt["RiskFree"] + tempt["EMR"] + tempt["EIR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_CAPMIndustry"
        ] = alpha

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_CAPMIndustry"
        ] = beta
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "BetaI_CAPMIndustry"
        ] = betaI

        # Market Model
        alpha, beta = olsMarket(estimation_window)

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_MarketModel",
        ] = tempt["Return"] - (alpha + beta * tempt["Market_return"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha_MarketModel",
        ] = tempt["Return"] - (beta * tempt["Market_return"])

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_Market"] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_Market"] = beta

        # Market Model + Industry

        alpha, beta, betaI = olsMarketIndustry(estimation_window)
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_MarketModel_Industry",
        ] = tempt["Return"] - (
            alpha + beta * tempt["Market_return"] + betaI * tempt["Industry_return"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha_MarketModel_Industry",
        ] = tempt["Return"] - (
            beta * tempt["Market_return"] + betaI * tempt["Industry_return"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_MarketIndustry"
        ] = alpha

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_MarketIndustry"
        ] = beta
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "BetaI_MarketIndustry"
        ] = betaI

        # 4Factor
        alpha, betaM, betaS, betaH, betaW = ols4(estimation_window)

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn_4Factor"
        ] = tempt["Return"] - (
            tempt["RiskFree"]
            + alpha
            + betaM * tempt["EMR"]
            + betaS * tempt["SMB"]
            + betaH * tempt["HML"]
            + betaW * tempt["Winner_Loser"]
        )

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_FOUR"] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaM_FOUR"] = betaM
        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaS_FOUR"] = betaS

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaH_FOUR"] = betaH

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "betaW_FOUR"] = betaW

        #
        #
        #

        estimation_window = a.loc[(a.EPeriod < -1 * Rlag) | (a.EPeriod > 2 * Rlag)]

        # CAPM
        alpha, beta = ols(estimation_window)

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn2"
        ] = tempt["Return"] - (tempt["RiskFree"] + alpha + beta * tempt["EMR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha2",
        ] = tempt["Return"] - (tempt["RiskFree"] + beta * tempt["EMR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn_Market2"
        ] = tempt["Return"] - (tempt["RiskFree"] + tempt["EMR"])

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_CAPM2"] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_CAPM2"] = beta

        # CAPM + Industry

        alpha, beta, betaI = olsIndustry(estimation_window)
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_Industry2",
        ] = tempt["Return"] - (
            tempt["RiskFree"] + alpha + beta * tempt["EMR"] + betaI * tempt["EIR"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha_Industry2",
        ] = tempt["Return"] - (
            tempt["RiskFree"] + beta * tempt["EMR"] + betaI * tempt["EIR"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_MarketIndustry2",
        ] = tempt["Return"] - (2 * tempt["RiskFree"] + tempt["EMR"] + tempt["EIR"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_CAPMIndustry2"
        ] = alpha

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_CAPMIndustry2"
        ] = beta
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "BetaI_CAPMIndustry2"
        ] = betaI

        # Market Model
        alpha, beta = olsMarket(estimation_window)

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_MarketModel2",
        ] = tempt["Return"] - (alpha + beta * tempt["Market_return"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha_MarketModel2",
        ] = tempt["Return"] - (beta * tempt["Market_return"])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_Market2"
        ] = alpha

        a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_Market2"] = beta

        # Market Model + Industry

        alpha, beta, betaI = olsMarketIndustry(estimation_window)
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_MarketModel_Industry2",
        ] = tempt["Return"] - (
            alpha + beta * tempt["Market_return"] + betaI * tempt["Industry_return"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)),
            "AbnormalReturn_WithoutAlpha_MarketMOdel_Industry2",
        ] = tempt["Return"] - (
            beta * tempt["Market_return"] + betaI * tempt["Industry_return"]
        )

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Alpha_MarketIndustry2"
        ] = alpha

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "Beta_MarketIndustry2"
        ] = beta
        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "BetaI_MarketIndustry2"
        ] = betaI

    return a[(~a["EPeriod"].isnull())]


def ols(tempt):
    y, x = "ER", "EMR"
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    beta = model.params[1]
    alpha = model.params[0]
    return alpha, beta


def olsIndustry(tempt):
    y, x = "ER", ["EMR", "EIR"]
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    betaI = model.params[2]
    beta = model.params[1]
    alpha = model.params[0]
    return alpha, beta, betaI


def olsMarket(tempt):
    y, x = "Return", "Market_return"
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    beta = model.params[1]
    alpha = model.params[0]
    return alpha, beta


def olsMarketIndustry(tempt):
    y, x = "Return", ["Market_return", "Industry_return"]
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    betaI = model.params[2]
    beta = model.params[1]
    alpha = model.params[0]
    return alpha, beta, betaI


def ols4(tempt):
    y, x = "ER", ["EMR", "SMB", "HML", "Winner_Loser"]
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    betaW = model.params[4]
    betaH = model.params[3]
    betaS = model.params[2]
    betaM = model.params[1]
    alpha = model.params[0]
    return alpha, betaM, betaS, betaH, betaW


#%%

ARdata = pd.DataFrame()
ARdata = ARdata.append(data)
ARdata["Return"] = ARdata.groupby("name")["close_price"].pct_change(periods=1) * 100
ARdata["ER"] = ARdata["Return"] - ARdata["RiskFree"]
ARdata["EMR"] = ARdata["Market_return"] - ARdata["RiskFree"]
ARdata["Industry_return"] = (
    ARdata["Industry_return"] - ARdata["Weight"] * ARdata["Return"]
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
Data["Amihud"] = abs(Data["Return"]) / Data["Volume"]
Data = Data.loc[(Data.EPeriod >= -20) & (Data.EPeriod <= 100)]

Data["NetInd"] = Data["ind_buy_volume"] - Data["ind_sell_volume"]
Data["TotalInd"] = Data["ind_buy_volume"] + Data["ind_sell_volume"]
Data["NetIns"] = Data["ins_buy_volume"] - Data["ins_sell_volume"]
Data["TotalIns"] = Data["ins_buy_volume"] + Data["ins_sell_volume"]

Data["IndlImbalance"] = Data["NetInd"].divide(Data["TotalInd"])
Data["InslImbalance"] = Data["NetIns"].divide(Data["TotalIns"])

for i in ["count", "volume", "value"]:
    Data["ind_imbalance_" + i] = Data["ind_buy_" + i] - Data["ind_sell_" + i]
    Data["ins_imbalance_" + i] = Data["ins_buy_" + i] - Data["ins_sell_" + i]
Data["ind_nav"] = (
    Data["ind_imbalance_volume"] * Data["close_price"] - Data["ind_imbalance_value"]
)
Data["ins_nav"] = (
    Data["ins_imbalance_volume"] * Data["close_price"] - Data["ins_imbalance_value"]
)


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
    "High",
    "Low",
    "Open",
    "Last",
    "Volume",
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
    "ind_nav",
    "ins_nav",
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
