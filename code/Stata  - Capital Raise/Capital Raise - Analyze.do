

clear
cls
import excel "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CapitalRaise_Analyze.xlsx", sheet("Sheet1") firstrow

cd "G:\Dropbox\Dropbox\Capital Raise\Report"


drop if JustPremium == 1



label define Bad 0 "Good" 1 "Bad"
label values Bad Bad
label define Good 1 "Good" 0 "Bad"
label values Good Good 

label define Reval 0 "No" 1 "Yes"

label values Revaluation Reval
label define qarter 1 "Low" 2 "Middle" 3  "High"

 foreach v of varlist  QuantileBM QuantilePE QuantileSize 	QuantileFreeFloat QuantileFreeFloatCap 	QuantileVolatility QuantileDebtRatio QuantileLeverageRatio {

	label values `v' qarter
	tabulate `v' Revaluation , summarize(AbnormalReturn) 
		
	quietly estpost ttest AbnormalReturn if `v' != 2, by(`v')  unequal
	esttab , wide  mtitle("diff.") p
	
	quietly estpost ttest AbnormalReturn if Revaluation != 1 & `v' != 2, by(`v')  unequal
	esttab , wide  mtitle("diff.") p
	
	quietly estpost ttest AbnormalReturn if Revaluation == 1 & `v' != 2, by(`v') unequal
	esttab , wide  mtitle("diff.") p
	
}











tabulate Good Revaluation , summarize(AbnormalReturn)


tabulate QuantilePE QuantileBM, summarize(AbnormalReturn)




tabout QuantilePE QuantileBM using m.tex, replace c(mean AbnormalReturn ) sum style(tex)  ///
topf(top.tex) botf(bot.tex) topstr(15cm) 


tabulate QuantileSize QuantileBM, summarize(AbnormalReturn) 


tabout QuantileSize QuantileBM using m.tex, replace c(mean AbnormalReturn ) sum style(tex)  ///
topf(top.tex) botf(bot.tex) topstr(15cm) 

tabulate QuantileSize QuantilePE, summarize(AbnormalReturn)

tabout QuantileSize QuantilePE using m.tex, replace c(mean AbnormalReturn ) sum style(tex)  ///
topf(top.tex) botf(bot.tex) topstr(15cm) 


tabulate Good QuantileSize, summarize(AbnormalReturn) 

tabout  Good QuantileSize  using m.tex, replace c(mean AbnormalReturn ) sum style(tex)  ///
topf(top.tex) botf(bot.tex) topstr(15cm) 

tabulate Good QuantileSize, summarize(AbnormalReturn)  mean
 
 



tabulate QuantilePE QuantileBM, summarize(AbnormalReturn_4Factor)

tabulate QuantileSize QuantileBM, summarize(AbnormalReturn_4Factor) 

tabulate QuantileSize QuantilePE, summarize(AbnormalReturn_4Factor)

tabulate Good QuantileSize, summarize(AbnormalReturn_4Factor) 
 
 
 
 
 
 
 
 
label define LH 0 "Low" 1 "High"
 foreach v of varlist  QuantileBM QuantilePE QuantileSize QuantileFreeFloat QuantileFreeFloatCap QuantileVolatility QuantileDebtRatio QuantileLeverageRatio {
replace `v' = 1 if `v' == 2
replace `v' = 2 if `v' == 3 | `v' == 4

label values `v' LH
replace `v' = `v' - 1
}



tabulate QuantilePE 




eststo v1: quietly reg AbnormalReturn Good QuantileBM QuantilePE QuantileSize QuantileFreeFloat QuantileFreeFloatCap QuantileVolatility QuantileDebtRatio QuantileLeverageRatio JustSaving  Hybrid Revaluation , cluster(YearQarter)
eststo v2: quietly reg AbnormalReturn Good QuantileBM  QuantileSize QuantileFreeFloat QuantileFreeFloatCap QuantileVolatility QuantileDebtRatio QuantileLeverageRatio JustSaving  Hybrid Revaluation , cluster(YearQarter)

eststo v3: quietly reg AbnormalReturn_4Factor Good QuantileBM QuantilePE QuantileSize QuantileFreeFloat QuantileFreeFloatCap QuantileVolatility QuantileDebtRatio QuantileLeverageRatio JustSaving  Hybrid Revaluation , cluster(YearQarter)
eststo v4: quietly reg AbnormalReturn_4Factor Good QuantileBM  QuantileSize QuantileFreeFloat QuantileFreeFloatCap QuantileVolatility QuantileDebtRatio QuantileLeverageRatio JustSaving  Hybrid Revaluation , cluster(YearQarter)

 


label variable QuantileBM "Book-to-Market Quantile"
label variable QuantileSize "Size Quantile"
label variable Hybrid "Cash \& Resereves"

label variable JustSaving "Resereves"


label variable Good "Bullish Market"
label variable QuantileBM "High Book-to-Market"
 label variable QuantilePE "High P/E"
label variable  QuantileSize "Large"
label variable  QuantileFreeFloat "High Free Float"
 label variable QuantileFreeFloatCap "High Free Market Cap"
 label variable QuantileVolatility "High Volatility"
 label variable QuantileDebtRatio "High Debt Ratio"
 label variable QuantileLeverageRatio "High Leverage Ratio"



esttab v1 v2  v3 v4, compress nomtitle  label mgroups("CAPM" "4Factor"   , pattern(1 0 1 0) prefix(\multicolumn{@span}{c}{) suffix(}) span erepeat(\cmidrule(lr){@span}) ),using AbnormalResult.tex ,replace