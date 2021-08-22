
clear
cls
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CapitalRaise.xlsx", sheet("Sheet1") firstrow
cd "D:\Dropbox\Capital Raise\Capital-Raise\Report\Output"


/**/

local varlist "CAR CAR_Market CAR_WithoutAlpha CAR_4Factor CAR_Industry CAR_WithoutAlpha_Industry CAR_MarketIndustry CAR_MarketModel CAR_WithoutAlpha_MarketModel CAR_MarketModel_Industry CAR_WithoutAlpha_MarketModel_Ind" 

// set graphics off
set graphics on

foreach x in `varlist'{
	display "`x'"
	/*Abnormal Return */
{
	foreach var in meanvar se p25 p95 n t_stat e g{
		capture drop `var'
	}
	egen meanvar = mean(`x'), by(EPeriod) 
	egen se = sd(`x'), by(EPeriod) 
	egen p95 = pctile(`x'), p(95) by(EPeriod) 
	egen p25 = pctile(`x'), p(25) by(EPeriod) 
	egen n = count(`x'), by(EPeriod) 
	gen t_stat = meanvar / se * sqrt(n)
	egen  e =  max(meanvar) 
	gen g  = round(e,1) +0.5
	quietly: summarize meanvar
	
	local mi =  round(r(min),1)
	local ma = round(r(max),1)
	local step = round(abs(round(r(min),1))/2,1)
	if `mi' == 0 {
	local step = round(abs(round(r(max),1))/10,1)
	}
	
	local number = round(r(max),1) - abs(round(r(min),1)) / `step'

	if `number' > 20 {
		local step = abs(round(r(min),1))
	}


	twoway bar g EPeriod if ~inrange(t_stat, -1.96 , 1.96) , bcolor(gs14) base(`mi')  || line meanvar EPeriod , xlab(-20(10)100,labsize(vsmall)) sort(EPeriod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(`mi') barw (0.01) 
	graph export `x'.png,replace
	graph export `x'.eps,replace
}
local typelist "JustRO Revaluation Hybrid JustSaving"

/*Abnormal Return for each type */
foreach type in `typelist'{
	display "`type'"
	foreach var in meanvar se p25 p95 n t_stat e g	{
		capture drop `var'
	}	
	egen meanvar = mean(`x') if  RaiseType == "`type'", by(EPeriod)	
	egen se = sd(`x') if  RaiseType == "`type'", by(EPeriod) 
	egen p95 = pctile(`x') if  RaiseType == "`type'", p(95) by(EPeriod) 
	egen p25 = pctile(`x') if  RaiseType == "`type'", p(25) by(EPeriod) 
	egen n = count(`x') if  RaiseType == "`type'", by(EPeriod) 
	gen t_stat = meanvar / se * sqrt(n)	
	egen  e =  max(meanvar)  if  RaiseType == "`type'"
	gen g  = round(e,1) +0.5 if  RaiseType == "`type'"
	quietly: summarize meanvar  if  RaiseType == "`type'"
	local mi =  round(r(min),1)
	local ma = round(r(max),1)
	local step = round(abs(round(r(min),1))/2,1)
	if `mi' == 0 {
	local step = round(abs(round(r(max),1))/10,1)
	}
	
	local number = round(r(max),1) - abs(round(r(min),1)) / `step'

	if `number' > 20 {
		local step = abs(round(r(min),1))
	}
	
	local name = "`type'"
	if "`type'" == "JustRO"{
		local name = "Cash"
	}
	if "`type'" == "JustSaving"{
		local name = "Saving"
	}
	twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "`type'", bcolor(gs14) base(`mi')  || line meanvar EPeriod if RaiseType == "`type'",xlab(-20(10)100,labsize(vsmall)) sort(EPeriod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from `name'",size(medium)) ytitle("Percent")  ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(`mi') barw (0.01) 
	
	graph export `x'`name'.png,replace
	graph export `x'`name'.eps,replace

}


}


