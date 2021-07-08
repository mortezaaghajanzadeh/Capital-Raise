#%%
def ABnormal(g, Rlag):
    lag = 121 + Rlag
    print(g.name)
    a = pd.DataFrame()
    a = a.append(g)
    a = a[~a.ER.isnull()]
    a = a.reset_index(drop=True).reset_index().rename(columns={"index": "Period"})
    a["Period"] = a["Period"].astype(int)
    a["AbnormalReturn"] = np.nan

    a["Alpha_FOUR"] = np.nan
    nEvent = 0
    for i in a[a.Event == a.t]["Period"]:
        nEvent += 1
        tempt = pd.DataFrame()
        tempt = a.loc[(a.Period >= (i - lag)) & (a.Period <= (i + lag))]

        if len(a.loc[a.EPeriod < -1 * Rlag]) < 30:
            continue

        alpha, beta = ols(a.loc[a.EPeriod < -1 * Rlag])

        a.loc[
            (a.Period >= (i - lag)) & (a.Period <= (i + lag)), "AbnormalReturn"
        ] = tempt["Return"] - (tempt["RiskFree"] + alpha + beta * tempt["EMR"])

    return a[(~a["EPeriod"].isnull())]


def ols(tempt):
    y, x = "ER", "EMR"
    model = sm.OLS(tempt[y], sm.add_constant(tempt[x])).fit()
    beta = model.params[1]
    alpha = model.params[0]
    return alpha, beta


gg = ARdata.groupby("name")
ARdata = gg.apply(ABnormal, Rlag=20).reset_index(drop=True)
