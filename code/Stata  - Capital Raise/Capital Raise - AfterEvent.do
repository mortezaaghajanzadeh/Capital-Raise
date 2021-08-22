
/*After Event*/

/*CAPM*/

cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR_AbnormalReturn2.xlsx", sheet("Sheet1") firstrow

 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"


 line CAAR EPeriod if RaiseType == "Total"|| rarea CAAR_05 CAAR_95 EPeriod if RaiseType == "Total", color(gs15)|| line CAAR_95 EPeriod if RaiseType == "Total", lpattern(dash_dot ) color(maroon )|| line CAAR_05 EPeriod if RaiseType == "Total" , lpattern(dash_dot ) color(navy ) || line CAAR EPeriod if RaiseType == "Total", legend(label(5 "Mean") label(3 "95Percentile") label(4 "5Percentile") order(5 3 4)  col(3) ) note("This figure graphs the CAAR from 20 period before event" "Estimation window is before and after event ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(,angle(0)) xtitle("Period") xlab(-20(10)100) 

graph export 95-5AbReturn2.png,replace
graph export 95-5AbReturn2.eps,replace
 
 
 
 
 
 
egen e =  max(CAAR) if RaiseType == "Total"
gen g  = round(e,1) + 0.5
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Total", bcolor(gs14) base(-3)  || line CAAR EPeriod if RaiseType == "Total", xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% " "Estimation window is before and after event ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(-3(1.5)9 ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-3) barw (0.01) 
graph export AbReturn2.png,replace
graph export AbReturn2.eps,replace



drop g e
egen  e =  max(CAAR) if RaiseType == "Revaluation"
gen g  = round(e,1) +1
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Revaluation", bcolor(gs14) base(-3)  || line CAAR EPeriod if RaiseType == "Revaluation",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%" "Estimation window is before and after event ") title("CAAR After Capital Raise from Revaluation",size(medium)) ytitle("Percent") ylabe(-0(5)30,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-3) barw (0.01) 
graph export AbReturnRevalution2.png,replace
graph export AbReturnRevalution2.eps,replace





drop g e
egen  e =  max(CAAR) if RaiseType == "JustRO"
gen g  = round(e,1)+0.5
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96)& RaiseType == "JustRO", bcolor(gs14) base(-0.50)  || line CAAR EPeriod if RaiseType == "JustRO",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%" "Estimation window is before and after event " ) title("CAAR After Capital Raise from Cash",size(medium)) ytitle("Percent") ylabe(0(1)7 ,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-0.5) barw (0.01) 
graph export AbReturnCash2.png,replace
graph export AbReturnCash2.eps,replace




drop g e
egen  e =  max(CAAR)  if RaiseType == "Hybrid"
gen g  = round(e,1) + 1
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & (RaiseType == "Hybrid"), bcolor(gs14) base()  || line CAAR EPeriod if RaiseType == "Hybrid" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%" "Estimation window is before and after event " ) title("CAAR After Capital Raise from Cash & Resereves"  ,size(medium)) ytitle("Percent") ylabe(0(2)8,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
graph export AbReturnHybrid2.png,replace
graph export AbReturnHybrid2.eps,replace




drop g e
egen  e =  max(CAAR) if RaiseType == "JustSaving"
gen g  = round(e,1) +1
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) &(RaiseType == "JustSaving"), bcolor(gs14) base(0)  || line CAAR EPeriod  if RaiseType == "JustSaving" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%" "Estimation window is before and after event ") title("CAAR After Capital Raise from Resereves",size(medium)) ytitle("Percent") ylabe(0(2)8,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
graph export AbReturnSaving2.png,replace
graph export AbReturnSaving2.eps,replace



/*Market Model*/


cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR_AbnormalReturn_MarketModel2.xlsx", sheet("Sheet1") firstrow



 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"

 
 
egen e =  max(CAAR) if RaiseType == "Total"
gen g  = round(e,1) 
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Total", bcolor(gs14) base(-4)  || line CAAR EPeriod if RaiseType == "Total", xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(-4(2)8 ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-4) barw (0.01) 
graph export AbReturn_MarketModel2.png,replace
graph export AbReturn_MarketModel2.eps,replace





drop g e
egen  e =  max(CAAR) if RaiseType == "Revaluation"
gen g  = round(e,1) +0.5
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Revaluation", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "Revaluation",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Revaluation",size(medium)) ytitle("Percent") ylabe(0(5)30,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
graph export AbReturnRevalution_MarketModel2.png,replace
graph export AbReturnRevalution_MarketModel2.eps,replace





drop g e
egen  e =  max(CAAR) if RaiseType == "JustRO"
gen g  = round(e,1)+ 1
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96)& RaiseType == "JustRO", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "JustRO",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash",size(medium)) ytitle("Percent") ylabe(0(2)8,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
graph export AbReturnCash_MarketModel2.png,replace
graph export AbReturnCash_MarketModel2.eps,replace


drop g e
egen  e =  max(CAAR) if RaiseType == "JustSaving"
gen g  = round(e,1) +0.5
twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) &(RaiseType == "JustSaving"), bcolor(gs14) base(0)  || line CAAR EPeriod  if RaiseType == "JustSaving" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Resereves",size(medium)) ytitle("Percent") ylabe(0(2)10,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
graph export AbReturnSaving_MarketModel2.png,replace
graph export AbReturnSaving_MarketModel2.eps,replace


