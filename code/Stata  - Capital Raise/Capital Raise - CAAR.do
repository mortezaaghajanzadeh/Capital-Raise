
clear
cls
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CapitalRaise.csv", encoding(UTF-8) 
cd "D:\Dropbox\Capital Raise\Capital-Raise\Report\Output"


capture drop zero

gen zero = 0



/**/


local varlist "car_abnormalreturn2 car  car_market car_withoutalpha car_4factor car_industry car_withoutalpha_industry car_marketindustry car_marketmodel car_withoutalpha_marketmodel car_marketmodel_industry car_withoutalpha_marketmodel_ind" 

// set graphics off
set graphics on

foreach x in `varlist'{
	display "`x'"
	local xlim 100
	/*Abnormal Return */	
{
	foreach var in meanvar se p25 p95 n t_stat e g{
		capture drop `var'
	}
	egen meanvar = mean(`x'), by(eperiod) 
	egen se = sd(`x'), by(eperiod) 
	egen p95 = pctile(`x'), p(95) by(eperiod) 
	egen p25 = pctile(`x'), p(25) by(eperiod) 
	egen n = count(`x'), by(eperiod) 
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


	twoway bar g eperiod if ~inrange(t_stat, -1.96 , 1.96) , bcolor(gs14) base(`mi')  || line meanvar eperiod , xlab(-20(10)`xlim',labsize(vsmall)) sort(eperiod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g eperiod if eperiod == 0 , bcolor(maroon) base(`mi') barw (0.01) 
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
	egen meanvar = mean(`x') if  raisetype == "`type'", by(eperiod)	
	egen se = sd(`x') if  raisetype == "`type'", by(eperiod) 
	egen p95 = pctile(`x') if  raisetype == "`type'", p(95) by(eperiod) 
	egen p25 = pctile(`x') if  raisetype == "`type'", p(25) by(eperiod) 
	egen n = count(`x') if  raisetype == "`type'", by(eperiod) 
	gen t_stat = meanvar / se * sqrt(n)	
	egen  e =  max(meanvar)  if  raisetype == "`type'"
	gen g  = round(e,1) +0.5 if  raisetype == "`type'"
	quietly: summarize meanvar  if  raisetype == "`type'"
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
	twoway bar g eperiod if ~inrange(t, -1.96 , 1.96) & raisetype == "`type'", bcolor(gs14) base(`mi')  || line meanvar eperiod if raisetype == "`type'",xlab(-20(10)`xlim',labsize(vsmall)) sort(eperiod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from `name'",size(medium)) ytitle("Percent")  ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g eperiod if eperiod == 0 , bcolor(maroon) base(`mi') barw (0.01) 
	
	graph export `x'`name'.png,replace
	graph export `x'`name'.eps,replace

}


}







local x "car_withoutalpha"

local varlist "car_abnormalreturn2 car  car_market car_withoutalpha car_4factor car_industry car_withoutalpha_industry car_marketindustry car_marketmodel car_withoutalpha_marketmodel car_marketmodel_industry car_withoutalpha_marketmodel_ind" 
foreach x in `varlist'{
display "`x'"
local xlim 100
	/*Abnormal Return */	
{
	foreach var in meanvar se p25 p95 n t_stat e g{
		capture drop `var'
	}
	egen meanvar = mean(`x'), by(eperiod) 
	egen se = sd(`x'), by(eperiod) 
	egen p95 = pctile(`x'), p(95) by(eperiod) 
	egen p25 = pctile(`x'), p(25) by(eperiod) 
	egen n = count(`x'), by(eperiod) 
	gen t_stat = meanvar / se * sqrt(n)
	egen  e =  max(meanvar) 
	gen g  = round(e,1) +0.5
	quietly: summarize meanvar
	
	local mi =  round(r(min),1)
	local ma = round(r(max),1)
	
	

	
	local lenght = round(r(max),1) - round(r(min),1)
	if `lenght' < 15{
	local step  = round( `lenght'/ 3 , 1)
	}
	if `lenght' >= 15{
	local step  = round( `lenght'/ 5 , 1)
	}
	
	if `mi'>=0 {
			twoway bar g eperiod if ~inrange(t_stat, -1.96 , 1.96) , bcolor(gs14) base(`mi')  || line meanvar eperiod , xlab(-20(10)`xlim',labsize(vsmall)) sort(eperiod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g eperiod if eperiod == 0 , bcolor(maroon) base(`mi') barw (0.01) 
		graph export `x'.png,replace
		graph export `x'.eps,replace
	
	}
	
	if `mi'< 0 {
			twoway bar g eperiod if ~inrange(t_stat, -1.96 , 1.96) , bcolor(gs14) base(`mi')  || line meanvar eperiod , xlab(-20(10)`xlim',labsize(vsmall)) sort(eperiod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g eperiod if eperiod == 0 , bcolor(maroon) base(`mi') barw (0.01) || line zero  eperiod  ,sort(eperiod)
		graph export `x'.png,replace
		graph export `x'.eps,replace
	
	}


}
local typelist "JustRO Revaluation Hybrid JustSaving"

/*Abnormal Return for each type */
foreach type in `typelist'{
	display "`type'"
	foreach var in meanvar se p25 p95 n t_stat e g	{
		capture drop `var'
	}	
	egen meanvar = mean(`x') if  raisetype == "`type'", by(eperiod)	
	egen se = sd(`x') if  raisetype == "`type'", by(eperiod) 
	egen p95 = pctile(`x') if  raisetype == "`type'", p(95) by(eperiod) 
	egen p25 = pctile(`x') if  raisetype == "`type'", p(25) by(eperiod) 
	egen n = count(`x') if  raisetype == "`type'", by(eperiod) 
	gen t_stat = meanvar / se * sqrt(n)	
	egen  e =  max(meanvar)  if  raisetype == "`type'"
	gen g  = round(e,1) +0.5 if  raisetype == "`type'"
	quietly: summarize meanvar  if  raisetype == "`type'"
	local mi =  round(r(min),1)
	local ma = round(r(max),1)
	
	
	
	local lenght = round(r(max),1) - round(r(min),1)
	if `lenght' < 15{
	local step  = round( `lenght'/ 3 , 1)
	}
	if `lenght' >= 15{
	local step  = round( `lenght'/ 5 , 1)
	}
	
	
	
	local name = "`type'"
	if "`type'" == "JustRO"{
		local name = "Cash"
	}
	if "`type'" == "JustSaving"{
		local name = "Saving"
	}
	
	if `mi'>=0 {
	twoway bar g eperiod if ~inrange(t, -1.96 , 1.96) & raisetype == "`type'", bcolor(gs14) base(`mi')  || line meanvar eperiod if raisetype == "`type'",xlab(-20(10)`xlim',labsize(vsmall)) sort(eperiod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from `name'",size(medium)) ytitle("Percent")  ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g eperiod if eperiod == 0 , bcolor(maroon) base(`mi') barw (0.01) 
	
	graph export `x'`name'.png,replace
	graph export `x'`name'.eps,replace
	}
	
	if `mi'<0 {
	twoway bar g eperiod if ~inrange(t, -1.96 , 1.96) & raisetype == "`type'", bcolor(gs14) base(`mi')  || line meanvar eperiod if raisetype == "`type'",xlab(-20(10)`xlim',labsize(vsmall)) sort(eperiod) note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from `name'",size(medium)) ytitle("Percent")  ylabe(`mi'(`step')`ma' ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g eperiod if eperiod == 0 , bcolor(maroon) base(`mi') barw (0.01) || line zero  eperiod  ,sort(eperiod)
	
	graph export `x'`name'.png,replace
	graph export `x'`name'.eps,replace
	}
}
}



