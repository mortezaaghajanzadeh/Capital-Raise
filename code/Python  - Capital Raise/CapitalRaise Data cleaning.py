# %%
import os
import pandas as pd
import numpy as np
import re


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


# %%
path3 = r"D:\Hard Data\Capital Raise\\"
n8 = path3 + "Name-ISN-Code-Latinname-Symbol-Industry-Sub_industry.xlsx"
symbolfirm = pd.read_excel(n8)[["Symbol", "Firm"]]
symbolfirm["Symbol"] = symbolfirm["Symbol"].apply(lambda x: convert_ar_characters(x))
symbolfirm["Firm"] = symbolfirm["Firm"].apply(lambda x: convert_ar_characters(x))


# %%
path3 = r"D:\Hard Data\Capital Raise\\"
n8 = path3 + "FirmSymbol.xlsx"
symbolfirm1 = pd.read_excel(n8).rename(columns={"name": "Symbol"})
symbolfirm1["Symbol"] = symbolfirm1["Symbol"].apply(lambda x: convert_ar_characters(x))
symbolfirm1["Firm"] = symbolfirm1["Firm"].apply(lambda x: convert_ar_characters(x))


# %%
symbolfirm = symbolfirm.append(symbolfirm1).drop_duplicates().reset_index(drop=True)
symbolfirm.loc[symbolfirm.Firm.str[-1] == " ", "Firm"] = symbolfirm.loc[
    symbolfirm.Firm.str[-1] == " "
].Firm.str[:-1]


# %%
path1 = r"D:\Hard Data\Capital Raise\افزایش سرمایه\\"
n1 = path1 + "full share capital increase.xlsx"
df1 = pd.read_excel(n1)
df1 = df1[~df1["CapBefore"].isnull()]
df1.columns
ids = symbolfirm.Firm
mapingdict = dict(zip(symbolfirm.Firm, symbolfirm.Symbol))
df1["firm"] = df1["firm"].apply(lambda x: convert_ar_characters(x))
df1["Symbol"] = df1["firm"].map(mapingdict)
df1 = df1.sort_values(by=["Symbol", "ExtOrdGMDate"])
df1.loc[df1.year.isnull(), "year"] = df1[df1.year.isnull()]["ExtOrdGMDate"].str[:4]
df1 = df1.rename(columns={"firm": "Firm"})


# %%
n2 = path1 + "capital raise - 89-92.xlsx"
df2 = pd.read_excel(n2)
df2["Symbol"] = df2["Symbol"].apply(lambda x: convert_ar_characters(x))
df2["Firm"] = df2["Firm"].apply(lambda x: convert_ar_characters(x))
df2.columns


# %%
n3 = path1 + "ƒnd ƒs¬ƒn¼ ½¬Oƒn8 8ƒ ƒ¬ ½ƒnó FºƒT ƒ½óª¬ƒñ ¼º8.xlsx"
df3 = pd.read_excel(n3)
df3["Symbol"] = df3["Symbol"].apply(lambda x: convert_ar_characters(x))
df3["Firm"] = df3["Firm"].apply(lambda x: convert_ar_characters(x))
df3.columns
df3.head()


# %%
n4 = path1 + "Share Capital Increase - 970715.xlsx"
df4 = pd.read_excel(n4)

df4 = df4.sort_values(by=["Symbol", "RegDate"])
df4["Symbol"] = df4["Symbol"].apply(lambda x: convert_ar_characters(x))
df4.columns


# %%
n5 = path1 + "Shareholders' Capital-82-92.xlsx"
df5 = pd.read_excel(n5)
df5["Firm"] = np.nan
df5.loc[df5.ExtOrdGMDate.str.contains("شرکت"), "Firm"] = df5.loc[
    df5.ExtOrdGMDate.str.contains("شرکت")
].ExtOrdGMDate.str[5:]
df5.Firm = df5.Firm.fillna(method="ffill")
df5 = df5.drop(df5.loc[df5.ExtOrdGMDate.str.contains("شرکت")].index)
df5 = df5[
    [
        "Firm",
        "ExtOrdGMDate",
        "GMType",
        "BookValue",
        "CapBefore",
        "CapAfter",
        "CapRaised",
        "%CapRaised",
        "%SavingCapRaising",
        "%ROCapRaising",
        "%PremiumCapRaising",
        "PriceBMG",
        "PriceAMG",
        "SubsCloseDate",
        "RegDate",
    ]
]
df5.columns
df5.Firm = df5.Firm.str[1::]
ids = symbolfirm.Firm
mapingdict = dict(zip(symbolfirm.Firm, symbolfirm.Symbol))
df5["Firm"] = df5["Firm"].apply(lambda x: convert_ar_characters(x))
df5["Symbol"] = df5["Firm"].map(mapingdict)
df5.head()


# %%
path2 = r"D:\Hard Data\Capital Raise\Share Capital Increase\\"
n6 = path2 + "Shareholders' Capital-84-97.xlsx"

df6 = pd.read_excel(n6)
df6["Symbol"] = df6["Symbol"].apply(lambda x: convert_ar_characters(x))
df6.head()


# %%
path3 = r"D:\Hard Data\Capital Raise\Rights Offerings\\"
n3 = path3 + "Rights Offerings 1389 to 1397.xlsx"
df7 = pd.DataFrame()
for i in range(1383, 1398):
    print(i)
    t = pd.read_excel(n3, str(i))
    df7 = df7.append(t)
df7 = df7[
    [
        "symbol",
        "ExtOrdGMInvDate",
        "ExtOrdGMDate",
        "CapAfter",
        "CapBefore",
        "CapRaised",
        "Costs",
        "ExRightsNo",
        "GenSubsRightsNo",
        "IPODate",
        "LicenseDate",
        "MktOfferCloseDate",
        "MktOfferOpenDate",
        "NetCashUnEx",
        "OnlyRO",
        "PreviousRODate",
        "ROCapRaising",
        "PremiumCapRaising",
        "RegDate",
        "SubsCloseDate",
        "SubsOpenDate",
        "TotUnExRev",
        "UnExRightsNo",
        "financial_firm",
        "fiscal_year",
        "group_en_name",
        "group_id",
        "group_name",
        "market",
        "market_en",
        "perShareNetCashUnEx",
    ]
]

df7 = df7.sort_values(by=["symbol", "ExtOrdGMDate"]).rename(
    columns={"symbol": "Symbol"}
)



# %%
df1 = df1[
    [
        "Symbol",
        "Firm",
        "year",
        "ExtOrdGMDate",
        "GMType",
        "BookValue",
        "CapBefore",
        "CapAfter",
        "CapRaised",
        "%CapRaised",
        "%SavingCapRaising",
        "SavingCapRaising",
        "%ROCapRaising",
        "ROCapRaising",
        "%PremiumCapRaising",
        "PremiumCapRaising",
        "SubsCloseDate",
    ]
].reset_index(drop=True)


# %%
df7 = df7[
    [
        "Symbol",
        "ExtOrdGMInvDate",
        "ExtOrdGMDate",
        "CapAfter",
        "CapBefore",
        "CapRaised",
        "Costs",
        "ExRightsNo",
        "GenSubsRightsNo",
        "LicenseDate",
        "MktOfferCloseDate",
        "MktOfferOpenDate",
        "NetCashUnEx",
        "OnlyRO",
        "ROCapRaising",
        "PremiumCapRaising",
        "RegDate",
        "SubsCloseDate",
        "SubsOpenDate",
        "TotUnExRev",
        "UnExRightsNo",
        "perShareNetCashUnEx",
    ]
].reset_index(drop=True)


# %%
df1["file"] = 1
df2["file"] = 2
df3["file"] = 3
df4["file"] = 4
df5["file"] = 5
df6["file"] = 6
df7["file"] = 7
df = (
    df1.append(df2)
    .append(df3)
    .append(df4)
    .append(df5)
    .append(df6)
    .append(df7)
    .sort_values(by=["Symbol", "ExtOrdGMDate"])
)
#%%

path4 = r"D:\Hard Data\Capital Raise\Raw Data\\"

mdf = pd.read_excel(path4 + "Capital Raised - codal crawl.xlsx")
mdf = mdf[mdf.BeforeCap > 0]
mdf['SavingCapRaising'] = mdf.profit + mdf.reserve
mdf = mdf.rename(
    columns ={
        'name':'Symbol',
        "EXORDate" : "ExtOrdGMDate" ,
        "RegisterDate":"RegDate",
        "BeforeCap":"CapBefore",
        "AfterCap":"CapAfter",
        "cash":"ROCapRaising",
        "revaluation":"Revaluation",
        "premium":"PremiumCapRaising"
    }
    ).drop(
        columns = ['profit','reserve']
    )
for i in ['ROCapRaising','Revaluation','PremiumCapRaising','SavingCapRaising'] :
    mdf["%"+i] =   mdf[i]/(mdf.CapAfter - mdf.CapBefore)*100
    
mdf['file'] = 0

mdf['year'] = mdf.ExtOrdGMDate.apply( lambda x : float(x.split('/')[0]) )
mdf["Symbol"] = mdf["Symbol"].apply(lambda x: convert_ar_characters(x))

df = (
    df.append(mdf
              ).sort_values(by=["Symbol", "ExtOrdGMDate"])
)




# %%

df.Firm = df.Firm.str.replace("سر.", "سرمایه گذاری")
df.loc[df.year.isnull(), "year"] = df[df.year.isnull()]["ExtOrdGMDate"].str[:4]
df.Symbol = df.Symbol.replace(np.nan, "")
df.loc[df.Symbol.str.contains("\("), "Symbol"] = df[df.Symbol.str.contains("\(")][
    "Symbol"
].str.split("\(", n=1, expand=True)[0]
df.Symbol = df.Symbol.replace("", np.nan)
df.year = df.year.replace(np.nan, 0)
df.year = df.year.astype(int)
df.year = df.year.replace(0, np.nan)
tt = df
df = df.sort_values(by=["Symbol", "year", "file"]).drop_duplicates(
    ["year", "Symbol", "CapAfter", "CapBefore"], keep="first"
)
df = df[(~df.CapBefore.isnull()) & (~df.CapAfter.isnull())].reset_index(drop=True)
df = df[(~df.year.isnull())].reset_index(drop=True)
df.loc[df.Firm == "ص مهندسی فیروزا", "Firm"] = "مهندسی فیروزا"
df.loc[
    df.Firm == "س.ص. بازنشستگی کارکنان بانکها", "Firm"
] = "س.ص.بازنشستگی کارکنان بانکها"
df.loc[df.Firm == "پیام", "Firm"] = "صنعتی پیام"
df.loc[df.Firm == "پیوند گستر پارس", "Firm"] = "برق و انرژی پیوندگستر پارس"
df.loc[
    df.Firm == "توسعه بین الملی پدیده شاندیز", "Firm"
] = "توسعه بین المللی پدیده شاندیز"
df.loc[df.Firm == "لیزینگ ایران و شرق", "Firm"] = "لیزینگ ایران و شرق"
df.loc[
    df.Firm == "سرمایه گذاری نفت و گاز و پتروشیمی تامین", "Firm"
] = "سر. نفت و گاز تامین"
df.loc[df.Firm == "دارو داملران رازک", "Firm"] = "دارو رازک"
df.loc[df.Firm == "موسسه مالی و اعتباری قوامین", "Firm"] = "بانک قوامین"
df.loc[df.Firm == "بوتان", "Firm"] = "صنعتی بوتان"
df.loc[df.Firm == "زر ماکارون", "Firm"] = "صنعتی زر ماکارون"
df.loc[df.Firm == "مالی اعتباری کوثر مرکزی", "Firm"] = "اعتباری کوثر مرکزی"
df.loc[df.Firm == "تاید واتر", "Firm"] = "تایدواترخاورمیانه"
df.loc[df.Firm == "مپنا (نیروگاهی ایران)", "Firm"] = "گروه مپنا"
df.loc[df.Firm == "دنا آفرین فدک", "Firm"] = "تهیه توزیع غذای دنا آفرین فدک"
df.loc[df.Firm == "کود شیمیائی اوره لردگان", "Firm"] = "کود شیمیایی اوره لردگان"
df.loc[df.Firm == "شیر پاستوریزه پگاه گیلان", "Firm"] = "شیرپاستوریزه پگاه گیلان"
df.loc[df.Firm == "فولاد سپید فراب کویر", "Firm"] = "تولیدی فولاد سپید فراب کویر"
df.loc[df.Firm == "چین چین", "Firm"] = "کشت‌ و صنعت‌ چین‌ چین"
df.loc[df.Firm == "لیزینگ ایران و شرق ", "Firm"] = "لیزینگ ایران و شرق"
df.loc[
    df.Firm == "سرمایه گذاری صندوق بازنشستگی کارکنان بانکها", "Firm"
] = "س.ص.بازنشستگی کارکنان بانکها"
mapingdict = dict(zip(symbolfirm.Firm, symbolfirm.Symbol))
df["Symbol2"] = df["Firm"].map(mapingdict)
df["Symbol1"] = np.nan
df.loc[~df.Symbol.isnull(), "Symbol1"] = df.loc[~df.Symbol.isnull()].Symbol
df.loc[~df.Symbol2.isnull(), "Symbol1"] = df.loc[~df.Symbol2.isnull()].Symbol2
df = df.drop(columns=["Symbol", "Symbol2"]).rename(columns={"Symbol1": "Symbol"})
df.loc[df.Firm == "سرمایه گذاری کشاورزی کوثر", "Symbol"] = "زکوثر"
df.loc[df.Firm == "صنعتی و معدنی ستبران", "Symbol"] = "ستبرا"

df.loc[df.Firm == "سیمان سفیدنی ریز", "Symbol"] = "سنیر"
df.loc[df.Firm == "تامین مواد اولیه فولاد صبانور", "Symbol"] = "کنور"
df.loc[df.Firm == "کیا الکترود شرق", "Symbol"] = "کیا"
df.loc[df.Symbol.str[-1] == " ", "Symbol"] = df.loc[
    df.Symbol.str[-1] == " "
].Symbol.str[:-1]
df.loc[df.Symbol.str[0] == " ", "Symbol"] = df.loc[df.Symbol.str[0] == " "].Symbol.str[
    1:
]


# %%
def vv2(row):
    X = row.split("/")
    return int(X[0] + X[1] + X[2])


df.ExtOrdGMDate = df.ExtOrdGMDate.apply(vv2)
df = df.sort_values(by=["Symbol", "file", "ExtOrdGMDate"])
df = df.drop(columns=["file"])

df["CapBefore2"] = (df["CapBefore"] / 100).round(0)
df["CapAfter2"] = (df["CapAfter"] / 100).round(0)
df["ExtOrdGMDate2"] = (df["ExtOrdGMDate"] / 10).round(0)

df = df.drop_duplicates(subset=["Symbol", "CapAfter2", "CapBefore2"], keep="first")


df = df[df.CapBefore != 0]
df["Percent"] = ((df["CapAfter"] - df["CapBefore"]) / df["CapBefore"]) * 100
df["Percent"] = df["Percent"].round(2)
df["year"] = df["ExtOrdGMDate"] / 10000
df["year"] = df["year"].round(0)


df = df.drop_duplicates(subset=["ExtOrdGMDate", "Symbol"], keep="first")


df = df.sort_values(by=["Symbol", "Firm", "ExtOrdGMDate"])
df.head()

df = df.reset_index(drop=True)

#%%
df["JustRO"] = 0
df.loc[df["%ROCapRaising"] > 99.99999999, "JustRO"] = 1
df["JustSaving"] = 0
df.loc[df["%SavingCapRaising"]  > 99.99999999, "JustSaving"] = 1
df["JustPremium"] = 0
df.loc[df["%PremiumCapRaising"]  > 99.99999999, "JustPremium"] = 1
df["JustRevaluation"] = 0
df.loc[df["%Revaluation"]  > 99.99999999, "JustRevaluation"] = 1

df["Hybrid"] = 0
df.loc[
    (df["%PremiumCapRaising"]  < 99.99999999)
    & (df["%SavingCapRaising"] < 99.999999990)
    & (df["%Revaluation"] < 99.999999990)
    & (df["%ROCapRaising"] < 99.99999999),
    "Hybrid",
] = 1

df = df[
    [
        "Symbol",
        "year",
        "Firm",
        "CapAfter",
        "CapBefore",
        "ExtOrdGMDate",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "Hybrid",
        "JustRevaluation",
        "%CapRaised",
        "%PremiumCapRaising",
        "%ROCapRaising",
        "%SavingCapRaising",
        "%Revaluation",
        "BookValue",
        "CapRaised",
        "Costs",
        "ExRightsNo",
        "ExtOrdBoardDate",
        "ExtOrdGMInvDate",
        "FirstTrade",
        "GMType",
        "GenSubsRightsNo",
        "LicenseDate",
        "MktOfferCloseDate",
        "MktOfferOpenDate",
        "NetCashUnEx",
        "OnlyRO",
        "PremiumCapRaising",
        "ROCapRaising",
        "Revaluation",
        "RegDate",
        "SavedDevelopmentPlanCapRaising",
        "SavedSafetyCapRaising",
        "SavingCapRaising",
        "SubsCloseDate",
        "SubsExtendedCloseDate",
        "SubsOpenDate",
        "TotUnExRev",
        "UnExRightsNo",
        "perShareNetCashUnEx",
    ]
]


# %%
len(df)


# %%
# ['سرمایه گذاری صنعت و معدن',
# 'موسسه مالی و اعتباری عسکریه',
# 'بانک آریا',
# 'آپادانا سرمایه گذاریم',
# 'امین توان آفرین ساز',
# 'ریسندگی شهرضا',
#  'گسترش تجارت و سرمایه گذاریایه ایرانیان',
# ]


# %%
def vv2(row):
    X = row.split("/")
    return int(X[0] + X[1] + X[2])


df8 = pd.read_excel(
    r"D:\Hard Data\Capital Raise\\" + "tajdidArzyabi.xlsx", "all")
df8 = df8.rename(
    columns={df8.columns[1]: "RegDate", df8.columns[0]: "Firm"}
    ).drop(
    columns=df8.columns[2]
)
df8 = df8[df8.RegDate != "nan"]
df8 = df8[~df8.RegDate.isnull()]
df8 = df8[~df8.Firm.isnull()]
df8["RegDate"] = df8["RegDate"].astype(str)


# %%
def vv2(row):
    X = row.split("/")
    return int(X[0] + X[1] + X[2])


df8 = pd.read_excel(r"D:\Hard Data\Capital Raise\\" + "tajdidArzyabi.xlsx", "all")
df8 = df8.rename(columns={df8.columns[1]: "RegDate", df8.columns[0]: "Firm"}).drop(
    columns=df8.columns[2]
)
df8 = df8[df8.RegDate != "nan"]
df8 = df8[~df8.RegDate.isnull()]
df8 = df8[~df8.Firm.isnull()]
df8["RegDate"] = df8["RegDate"].astype(str)


df8.RegDate = df8.RegDate.apply(vv2)


ids = symbolfirm.Firm
mapingdict = dict(zip(symbolfirm.Firm, symbolfirm.Symbol))
df8.loc[df8.Firm == "آذرآب", "Firm"] = "آذراب"
df8.loc[df8.Firm == "آذرآب", "Firm"] = "آذراب"
df8.loc[df8.Firm == "تولید محور خودرو", "Firm"] = "محورخودرو"
df8.loc[df8.Firm == "قند هکمتان", "Firm"] = "قندهکمتان‌"


# df8.loc[df8.Firm == '','Firm'] = ""
# df8.loc[df8.Firm == '','Firm'] = ""
# df8.loc[df8.Firm == '','Firm'] = ""
# df8.loc[df8.Firm == '','Firm'] = ""

df8["Firm"] = df8["Firm"].apply(lambda x: convert_ar_characters(x))
df8["Symbol"] = df8["Firm"].map(mapingdict)
index = [34, 35, 36, 37, 38, 39, 40, 41, 42]
df8.loc[df8.index.isin(index), "Symbol"] = df8[df8.index.isin(index)].Firm
df8.loc[df8.Firm == "کمک فنر ایندامین سایپا", "Symbol"] = "خکمک"
df8.loc[df8.Firm == "کمباین سازی ایران", "Symbol"] = "تکمبا"

df8.loc[df8.Firm == ": کشتیرانی جمهوری اسلمی ایران", "Symbol"] = "حکشتی"
df8.loc[df8.Firm == ": کاشی تکسرام", "Symbol"] = "تکسرام"
df8.loc[df8.Firm == ": قند نیشابور", "Symbol"] = "قنیشا"
df8.loc[df8.Firm == ": قند ثابت خراسان", "Symbol"] = "قثابت"
df8.loc[df8.Firm == ": شرکت ایرانی تولید اتومبیل )سایپا(", "Symbol"] = "خساپا"
df8.loc[df8.Firm == ": گسترش صنایع و خدمات کشاورزی", "Symbol"] = "تکشا"
df8.loc[df8.Firm == ": مهندسی صنعتی روان فن آور", "Symbol"] = "خفناور"
df8.loc[df8.Firm == "سرامیک های صنعتی اردکان", "Symbol"] = "اردکان"
df8.loc[df8.Firm == ": فرآورده های غذائی و قند تربت جام", "Symbol"] = "قجام"
df8.loc[df8.Firm == "کارخانجات پلسکوکار سایپا", "Symbol"] = "پلاسک"
df8.loc[df8.Firm == "معدنی املح ایران", "Symbol"] = "شاملا"
df8.loc[df8.Firm == ": بانک سینا", "Symbol"] = "وسینا"
df8.loc[df8.Firm == "قند شیروان، قوچان", "Symbol"] = "قشیر"
df8.loc[df8.Firm == "تامین ماسه ریخته گری", "Symbol"] = "کماسه"
df8.loc[df8.Firm == "فولد کاویان", "Symbol"] = "فوکا"
df8.loc[df8.Firm == "آهنگری تراکتور سازی ایران", "Symbol"] = "خاهن"
df8.loc[df8.Firm == "سهامی ذوب آهن اصفهان", "Symbol"] = "ذوب"
df8.loc[df8.Firm == ": قند بیستون", "Symbol"] = "قیستو"

# df8.loc[df8.Firm == '','Symbol'] = "حکشتی"
df8["year"] = df8.RegDate.astype(str)
df8["year"] = df8["year"].str[0:4]
df8["year"] = df8.year.astype(int)
df8.loc[~df8.symbol.isnull(), "Symbol"] = df8.loc[~df8.symbol.isnull()].symbol
# df8 = df8.dropna()


# %%
df8[df8.Symbol.isnull()]
#%%


#%%
def vv2(row):
    X = row.split("/")
    return int(X[0] + X[1] + X[2])


df9 = pd.read_excel(
    r"D:\Hard Data\Capital Raise\\" + "TajdidArziabi_9912.xlsx")
# df9 = df9.rename(columns = {df9.columns[1]:"RegDate",df9.columns[0]:"Firm"}).drop(columns = df9.columns[2])
df9 = df9.drop(columns=["finYear", "registered_date.1"])

# df9 = df9[df9.RegDate != 'nan']
# df9 = df9[~df9.RegDate.isnull()]
# df9 = df9[~df9.Firm.isnull()]
# df9['RegDate'] = df9['RegDate'].astype(str)


# %%


# %%

# %%


# %%
fkey = zip(df8.Symbol, df8.year)
len(dict(fkey))
tt = df8[["Symbol", "year"]].dropna()
tt
fkey = zip(tt.Symbol, tt.year)
len(tt)
fkey = zip(tt.Symbol, tt.year)
mapingdict = dict(zip(fkey, [1] * 91))
df["year"] = df.year.astype(int)
df["Revaluation2"] = df.set_index(["Symbol", "year"]).index.map(mapingdict)
df.loc[df.Revaluation2.isnull(), "Revaluation2"] = 0

#%%
df['Revaluation']= 0
df.loc[df.Revaluation2 == 1,'Revaluation' ] = 1
df.loc[df.JustRevaluation == 1,'Revaluation' ] = 1
df.loc[df['%Revaluation']>0,'Revaluation'] = 1


# %%
df.loc[df.Revaluation == 1, "JustRO"] = 0
df.loc[df.Revaluation == 1, "Hybrid"] = 0
df.loc[df.Revaluation == 1, "JustSaving"] = 0
df.loc[df.Revaluation == 1, "JustPremium"] = 0
df.loc[df.Revaluation == 1, "JusHybridtRO"] = 0
df[df.Symbol == "خمهر"][["Revaluation", "year", "Symbol", "JustSaving"]]


# %%
# datasource = open(r"G:\Hard Data\Capital Raise\\" + 'افزایش سرمایه.xml')
# import xml.etree.ElementTree as ET
# xml_data = open(r"G:\Hard Data\Capital Raise\\" + 'افزایش سرمایه.xml', 'r').read()  # Read file
# root = ET.XML(xml_data)  # Parse XML

# data = []
# cols = []
# for i, child in enumerate(root):
#     data.append([subchild.text for subchild in child])
#     cols.append(child.tag)

# d = pd.DataFrame(data).T  # Write in DF and transpose it
# d.columns = cols  # Update column names
# print(d)



#%%
n = r"D:\Hard Data\Capital Raise\\" + "TajdidArziabi_9912.xlsx"
df9 = pd.read_excel(n)

df9 = df9[['symbol', 'registered_date',
    'capitalBeforeRevaluation',  'ExtOrdGMDate']]
df9['Revaluation'] = 1
df9 = df9.rename(columns = {
    'symbol': "Symbol",
    'capitalBeforeRevaluation':'CapBefore',
    'registered_date':'LicenseDate'
})

# df9.ExtOrdGMDate = df9.ExtOrdGMDate.apply(vv2)
df9.LicenseDate = df9.LicenseDate.apply(vv2)
df9['year'] = round(df9.ExtOrdGMDate / 10000,0).astype(int)
df9.head()

a = pd.DataFrame()
a = a.append(df)
dfindex = zip(df9.Symbol,df9.year)
mapingdict = dict(zip(dfindex,df9.Revaluation))
a['Revaluation2'] = a.set_index(['Symbol','year']).index.map(mapingdict)

a.loc[(a.Revaluation == 0)&(a.Revaluation2 == 1),'Revaluation'] = 1
a = a.drop(columns = 'Revaluation2')

a = a.append(df9[~(df9.set_index([
    'Symbol','year'
    ]).index .isin(a.set_index(['Symbol','year']).index))])
a.loc[
    a.Firm == 'سرمایه گذاری صنعت و معدن','Symbol'
    ] = 'وصنعت'
a.loc[
    a.Firm == 'گسترش تجارت و سرمایه گذاریایه ایرانیان','Symbol'
    ] = 'ولتجار'

a.loc[
    a.Firm == 'امین توان آفرین ساز','Symbol'
    ] = 'وامین'

a.loc[
    a.Firm == 'آپادانا سرمایه گذاریم','Symbol'
    ] = 'كپانا'

# %%
df = pd.DataFrame()
df = df.append(a)
df.to_excel(r"D:\Hard Data\Capital Raise" + "\Capital Rise - 71-99.xlsx", index=False)


# %%
df[df.Symbol == "خمهر"][
    [
        "ExtOrdGMDate",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "Hybrid",
        "Revaluation",
        "year",
    ]
]


# %%
df8


# %%
df[df.Revaluation == 1]


# %%
