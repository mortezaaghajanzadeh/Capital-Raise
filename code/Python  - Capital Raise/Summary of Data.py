# %%
import os
import pandas as pd
import numpy as np
import re
import statsmodels.api as sm
import matplotlib.pyplot as plt


# %%
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


# %%
path = r"G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\\"
df = pd.read_excel(path + "SDate.xlsx")
df.columns

# %%
df["Q"] = df.ExtOrdGMDate.astype(str)
df["year"] = df.Q.str[0:4]
df["Q"] = df.Q.str[4:6]
df.Q = df.Q.astype(int)
df.loc[df.Q > 9, "Q"] = 40
df.loc[(df.Q > 6) & (df.Q != 40), "Q"] = 30
df.loc[(df.Q > 3) & (df.Q != 40) & (df.Q != 30), "Q"] = 20
df.loc[df.Q < 4, "Q"] = 10
df.Q = df.Q / 10
df.Q = df.Q.astype(int)
df.Q = df.Q.astype(str)
df.year = df.year.astype(int)
df["yearQ"] = df.year.astype(str)
df["yearQ"] = df["yearQ"] + "/" + df["Q"]
df.Q = df.Q.astype(int)
df[["ExtOrdGMDate", "Q", "yearQ", "year"]]


# %%
a = (
    df.groupby("Q")
    .JustSaving.sum()
    .to_frame()
    .rename(columns={"JustSaving": "Reserves"})
    .T
)
a = a.append(
    df.groupby("Q").JustRO.sum().to_frame().rename(columns={"JustRO": "Cash"}).T
)
a = a.append(
    df.groupby("Q")
    .JustPremium.sum()
    .to_frame()
    .rename(columns={"JustPremium": "Premium"})
    .T
)
a = a.append(
    df.groupby("Q").Hybrid.sum().to_frame().rename(columns={"Hybrid": "Hybrid"}).T
)
a = a.append(
    df.groupby("Q")
    .Revaluation.sum()
    .to_frame()
    .rename(columns={"Revaluation": "Revaluation"})
    .T
)
a = a.append(df.groupby("Q").size().to_frame().rename(columns={0: "Sum"}).T)
a.T.to_excel(path + "QVDate.xlsx")
a


# %%
a = (
    df.groupby("yearQ")
    .JustSaving.sum()
    .to_frame()
    .rename(columns={"JustSaving": "Saving"})
    .T
)
a = a.append(
    df.groupby("yearQ").JustRO.sum().to_frame().rename(columns={"JustRO": "Cash"}).T
)
a = a.append(
    df.groupby("yearQ")
    .JustPremium.sum()
    .to_frame()
    .rename(columns={"JustPremium": "Premium"})
    .T
)
a = a.append(
    df.groupby("yearQ").Hybrid.sum().to_frame().rename(columns={"Hybrid": "Hybrid"}).T
)
a = a.append(
    df.groupby("yearQ")
    .Revaluation.sum()
    .to_frame()
    .rename(columns={"Revaluation": "Revaluation"})
    .T
)
a = a.append(df.groupby("yearQ").size().to_frame().rename(columns={0: "Sum"}).T)
a.T.to_excel(path + "QVDate2.xlsx")
a = a.T
a


# %%
a = a.T
a[["Sum"]].plot.bar(stacked=True, figsize=(20, 10), legend=False)
plt.title("Number of Capital Raise")
# txt= "Note: Number of Capital Raise from each source "
plt.xlabel("Year Quarter")
# plt.figtext(0.5,-0.005, txt, horizontalalignment='center',
#             fontsize=12, multialignment='left',
#             bbox=dict(boxstyle="round", facecolor='#D8D8D8',
#                       ec="0.5", pad=0.5, alpha=1), fontweight='bold')
# plt.legend(["Lower Hit", "Upper Hit"]);
# path2 = r"G:\Dropbox\Dropbox\Finance(Prof.Heidari-Aghajanzadeh)\Project\Capital Raise\Report"
# plt.savefig(path2 + "\\Q2Number.png", bbox_inches="tight")
# plt.savefig(path2 + "\\Q2Number.eps", bbox_inches="tight")


# %%

a[["Cash", "Reserves", "Hybrid", "Revaluation", "Premium"]].plot.bar(
    stacked=True, figsize=(20, 10)
)
plt.title("Number of Capital Raise")
txt = "Note: Number of Capital Raise from each source "
plt.xlabel("Year Quarter ")
plt.figtext(
    0.5,
    -0.005,
    txt,
    horizontalalignment="center",
    fontsize=12,
    multialignment="left",
    bbox=dict(boxstyle="round", facecolor="#D8D8D8", ec="0.5", pad=0.5, alpha=1),
    fontweight="bold",
)
# plt.legend(["Lower Hit", "Upper Hit"]);
# path2 = r"G:\Dropbox\Dropbox\Finance(Prof.Heidari-Aghajanzadeh)\Project\Capital Raise\Report"
# plt.savefig(path2 + "\\Q2Number2.png", bbox_inches="tight")
# plt.savefig(path2 + "\\Q2Number2.eps", bbox_inches="tight")


# %%

df["CapRaised"] = df["CapAfter"] - df["CapBefore"]
yearCapmedian = (
    df.groupby("year")
    .CapRaised.median()
    .to_frame()
    .rename(columns={"CapRaised": "MedianCapRaise"})
)
yearCapmedian.plot.bar(stacked=False, figsize=(10, 5))
yearCapmedian = yearCapmedian.reset_index()

yearCapmean = (
    df.groupby("year")
    .CapRaised.mean()
    .to_frame()
    .rename(columns={"CapRaised": "MeanCapRaise"})
)
yearCapmean.plot.bar(stacked=False, figsize=(10, 5))
yearCapmean = yearCapmean.reset_index()


yearsum = (
    df.groupby("year").CapRaised.sum().to_frame().rename(columns={"CapRaised": "Sum"})
)
yearsum.plot.bar(stacked=False, figsize=(10, 5))
yearsum = yearsum.reset_index()


# %%
df["Percent"] = ((df.CapAfter / df.CapBefore) - 1) * 100

yearmean = (
    df.groupby("year")
    .Percent.median()
    .to_frame()
    .rename(columns={"Percent": "MedianPercent"})
)
yearmean.plot.bar(stacked=False, figsize=(10, 5))
yearmean = yearmean.reset_index()
yearnumber = df.groupby("year").size().to_frame().rename(columns={0: "Number"})
yearnumber.plot.bar(stacked=False, figsize=(10, 5))
yearnumber = yearnumber.reset_index()


# %%
vv = df.groupby("name").size().to_frame().sort_values(by=0)
vv.to_excel(path + "vdata2.xlsx")
vv


# %%
yearHybridnumber = df.groupby("year").Hybrid.sum().to_frame()
yearHybridnumber.plot.bar(stacked=False, figsize=(10, 5))
yearHybridnumber = yearHybridnumber.reset_index()

yearPremiumnumber = df.groupby("year").JustPremium.sum().to_frame()
yearPremiumnumber.plot.bar(stacked=False, figsize=(10, 5))
yearPremiumnumber = yearPremiumnumber.reset_index()

yearSavingnumber = df.groupby("year").JustSaving.sum().to_frame()
yearSavingnumber.plot.bar(stacked=False, figsize=(10, 5))
yearSavingnumber = yearSavingnumber.reset_index()

yearROnumber = df.groupby("year").JustRO.sum().to_frame()
yearROnumber.plot.bar(stacked=False, figsize=(10, 5))
yearROnumber = yearROnumber.reset_index()

yearRevaluationnumber = df.groupby("year").Revaluation.sum().to_frame()
yearRevaluationnumber.plot.bar(stacked=False, figsize=(10, 5))
yearRevaluationnumber = yearRevaluationnumber.reset_index()


# %%
vdata = (
    yearnumber.merge(yearmean)
    .merge(yearsum)
    .merge(yearCapmedian)
    .merge(yearCapmean)
    .merge(yearHybridnumber)
    .merge(yearPremiumnumber)
    .merge(yearSavingnumber)
    .merge(yearROnumber)
    .merge(yearRevaluationnumber)
)


# %%
vdata
vdata.to_excel(path + "SummaryCapitalData.xlsx", index=False)

# %%
df.loc[df.Revaluation == 1][
    [
        "name",
        "JustRO",
        "JustSaving",
        "JustPremium",
        "Hybrid",
        "Revaluation",
    ]
]


# %%
a = (
    df[["JustRO", "JustSaving", "JustPremium", "Revaluation", "Hybrid"]]
    .sum()
    .to_frame()
    .T.rename(index={0: "Event"})
)
b = (
    (
        df[["JustRO", "JustSaving", "JustPremium", "Revaluation", "Hybrid"]]
        .describe()
        .T.iloc[:, 1]
        * 100
    )
    .round(2)
    .to_frame()
    .T.rename(index={"mean": "Percent"})
)
a.append(b)

# %%
