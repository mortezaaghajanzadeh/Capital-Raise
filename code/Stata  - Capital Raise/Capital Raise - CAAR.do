cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR.xlsx", sheet("Sheet1") firstrow

 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"

 



 
 /**/
 line CAAR EPeriod if RaiseType == "Total"|| rarea CAAR_05 CAAR_95 EPeriod if RaiseType == "Total", color(gs15)|| line CAAR_95 EPeriod if RaiseType == "Total", lpattern(dash_dot ) color(maroon )|| line CAAR_05 EPeriod if RaiseType == "Total" , lpattern(dash_dot ) color(navy ) || line CAAR EPeriod if RaiseType == "Total", legend(label(5 "Mean") label(3 "95Percentile") label(4 "5Percentile") order(5 3 4)  col(3) ) note("This figure graphs the CAAR from 20 period before event ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(,angle(0)) xtitle("Period") xlab(-20(10)100) 

graph export 95-5AbReturn.png,replace
graph export 95-5AbReturn.eps,replace
 
 
 
 
 
 
egen e =  max(CAAR) if RaiseType == "Total"
gen g  = round(e,1) + 0.5






twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Total", bcolor(gs14) base(-4.5)  || line CAAR EPeriod if RaiseType == "Total", xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(-4.5(1.5)7.5 ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-4.5) barw (0.01) 


graph export AbReturn.png,replace
graph export AbReturn.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "Revaluation"
gen g  = round(e,1) +1

 
 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Revaluation", bcolor(gs14) base(-3)  || line CAAR EPeriod if RaiseType == "Revaluation",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Revaluation",size(medium)) ytitle("Percent") ylabe(-0(5)30,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-3) barw (0.01) 
 

graph export AbReturnRevalution.png,replace
graph export AbReturnRevalution.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustRO"
gen g  = round(e,1)

 
 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96)& RaiseType == "JustRO", bcolor(gs14) base(-0.50)  || line CAAR EPeriod if RaiseType == "JustRO",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash",size(medium)) ytitle("Percent") ylabe(0(1)5,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-0.5) barw (0.01) 
 

graph export AbReturnCash.png,replace
graph export AbReturnCash.eps,replace




drop g e
 
egen  e =  max(CAAR)  if RaiseType == "Hybrid"
gen g  = round(e,1) + 1


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & (RaiseType == "Hybrid"), bcolor(gs14) base(-6)  || line CAAR EPeriod if RaiseType == "Hybrid" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash & Resereves",size(medium)) ytitle("Percent") ylabe(-6(2)6,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-6) barw (0.01) 


graph export AbReturnHybrid.png,replace
graph export AbReturnHybrid.eps,replace




drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustSaving"
gen g  = round(e,1) +1


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) &(RaiseType == "JustSaving"), bcolor(gs14) base(-16)  || line CAAR EPeriod  if RaiseType == "JustSaving" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Resereves",size(medium)) ytitle("Percent") ylabe(-16(4)8,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-16) barw (0.01) 


graph export AbReturnSaving.png,replace
graph export AbReturnSaving.eps,replace




/*4Factor*/
cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR_4Factor.xlsx", sheet("Sheet1") firstrow


 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"

 
 
 line CAAR EPeriod if RaiseType == "Total"|| rarea CAAR_05 CAAR_95 EPeriod if RaiseType == "Total", color(gs15)|| line CAAR_95 EPeriod if RaiseType == "Total", lpattern(dash_dot ) color(maroon )|| line CAAR_05 EPeriod if RaiseType == "Total" , lpattern(dash_dot ) color(navy ) || line CAAR EPeriod if RaiseType == "Total", legend(label(5 "Mean") label(3 "95Percentile") label(4 "5Percentile") order(5 3 4)  col(3) ) note("This figure graphs the CAAR from 20 period before event ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(,angle(0)) xtitle("Period") xlab(-20(10)100) 

graph export 95-5AbReturn_4Factor.png,replace
graph export 95-5AbReturn_4Factor.eps,replace
 
 
 
 
 
 
egen e =  max(CAAR) if RaiseType == "Total"
gen g  = round(e,1) +1



twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Total", bcolor(gs14) base(-8)  || line CAAR EPeriod if RaiseType == "Total", xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(-8(2)8 ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-8) barw (0.01) 


graph export AbReturn_4Factor.png,replace
graph export AbReturn_4Factor.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "Revaluation"
gen g  = round(e,1) +2

 
 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Revaluation", bcolor(gs14) base(-5)  || line CAAR EPeriod if RaiseType == "Revaluation",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Revaluation",size(medium)) ytitle("Percent") ylabe(-5(5)35,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-5) barw (0.01) 
 

graph export AbReturnRevalution_4Factor.png,replace
graph export AbReturnRevalution_4Factor.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustRO"
gen g  = round(e,1)+0.5

 
 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96)& RaiseType == "JustRO", bcolor(gs14) base(-1)  || line CAAR EPeriod if RaiseType == "JustRO",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash",size(medium)) ytitle("Percent") ylabe(-1(1)5,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-1) barw (0.01) 
 

graph export AbReturnCash_4Factor.png,replace
graph export AbReturnCash_4Factor.eps,replace




drop g e
 
egen  e =  max(CAAR)  if RaiseType == "Hybrid"
gen g  = round(e,1) +1


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & (RaiseType == "Hybrid"), bcolor(gs14) base(-12) || line CAAR EPeriod if RaiseType == "Hybrid" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash & Resereves",size(medium)) ytitle("Percent") ylabe(-12(2)4,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-12) barw (0.01) 


graph export AbReturnHybrid_4Factor.png,replace
graph export AbReturnHybrid_4Factor.eps,replace




drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustSaving"
gen g  = round(e,1) + 1


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) &(RaiseType == "JustSaving"), bcolor(gs14) base(-16)  || line CAAR EPeriod  if RaiseType == "JustSaving" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Resereves",size(medium)) ytitle("Percent") ylabe(-16(4)7,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(-16) barw (0.01) 


graph export AbReturnSaving_4Factor.png,replace
graph export AbReturnSaving_4Factor.eps,replace


/**/





/*Without alpha*/
cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR_WithoutAlpha.xlsx", sheet("Sheet1") firstrow


 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"

 

 
 line CAAR EPeriod if RaiseType == "Total"|| rarea CAAR_05 CAAR_95 EPeriod if RaiseType == "Total", color(gs15)|| line CAAR_95 EPeriod if RaiseType == "Total", lpattern(dash_dot ) color(maroon )|| line CAAR_05 EPeriod if RaiseType == "Total" , lpattern(dash_dot ) color(navy ) || line CAAR EPeriod if RaiseType == "Total", legend(label(5 "Mean") label(3 "95Percentile") label(4 "5Percentile") order(5 3 4)  col(3) ) note("This figure graphs the CAAR from 20 period before event ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(,angle(0)) xtitle("Period") xlab(-20(10)100) 

graph export 95-5AbReturn_WithoutAlpha.png,replace
graph export 95-5AbReturn_WithoutAlpha.eps,replace
 
 
 
 
 
 
egen e =  max(CAAR) if RaiseType == "Total"
gen g  = round(e,1) 



twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Total", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "Total", xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(0(2)14 ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 


graph export AbReturn_WithoutAlpha.png,replace
graph export AbReturn_WithoutAlpha.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "Revaluation"
gen g  = round(e,1) +1

 
 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Revaluation", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "Revaluation",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Revaluation",size(medium)) ytitle("Percent") ylabe(0(5)45,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
 

graph export AbReturnRevalution_WithoutAlpha.png,replace
graph export AbReturnRevalution_WithoutAlpha.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustRO"
gen g  = round(e,1) + 0.5

 



twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96)& RaiseType == "JustRO", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "JustRO",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash",size(medium)) ytitle("Percent") ylabe(0(3)12,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
 

graph export AbReturnCash_WithoutAlpha.png,replace
graph export AbReturnCash_WithoutAlpha.eps,replace




drop g e
 
egen  e =  max(CAAR)  if RaiseType == "Hybrid"
gen g  = round(e,1) +1


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & (RaiseType == "Hybrid"), bcolor(gs14) base(0) || line CAAR EPeriod if RaiseType == "Hybrid" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash & Resereves",size(medium)) ytitle("Percent") ylabe(0(2)12,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 


graph export AbReturnHybrid_WithoutAlpha.png,replace
graph export AbReturnHybrid_WithoutAlpha.eps,replace




drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustSaving"
gen g  = round(e,1) 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) &(RaiseType == "JustSaving"), bcolor(gs14) base(0)  || line CAAR EPeriod  if RaiseType == "JustSaving" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Resereves",size(medium)) ytitle("Percent") ylabe(0(2)14,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 


graph export AbReturnSaving_WithoutAlpha.png,replace
graph export AbReturnSaving_WithoutAlpha.eps,replace


/**/


/*From Market*/
cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR_Market.xlsx", sheet("Sheet1") firstrow



 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"

 

 
 line CAAR EPeriod if RaiseType == "Total"|| rarea CAAR_05 CAAR_95 EPeriod if RaiseType == "Total", color(gs15)|| line CAAR_95 EPeriod if RaiseType == "Total", lpattern(dash_dot ) color(maroon )|| line CAAR_05 EPeriod if RaiseType == "Total" , lpattern(dash_dot ) color(navy ) || line CAAR EPeriod if RaiseType == "Total", legend(label(5 "Mean") label(3 "95Percentile") label(4 "5Percentile") order(5 3 4)  col(3) ) note("This figure graphs the CAAR from 20 period before event ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(,angle(0)) xtitle("Period") xlab(-20(10)100) 

graph export 95-5AbReturn_Market.png,replace
graph export 95-5AbReturn_Market.eps,replace
 
 
 
 
 
 
egen e =  max(CAAR) if RaiseType == "Total"
gen g  = round(e,1) +0.5



twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Total", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "Total", xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5% ") title("CAAR After Capital Raise") ytitle("Percent") ylabe(0(2)10 ,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 


graph export AbReturn_Market.png,replace
graph export AbReturn_Market.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "Revaluation"
gen g  = round(e,1) +2

 
 


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & RaiseType == "Revaluation", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "Revaluation",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Revaluation",size(medium)) ytitle("Percent") ylabe(0(5)40,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
 

graph export AbReturnRevalution_Market.png,replace
graph export AbReturnRevalution_Market.eps,replace





drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustRO"
gen g  = round(e,1)+0.5

 



twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96)& RaiseType == "JustRO", bcolor(gs14) base(0)  || line CAAR EPeriod if RaiseType == "JustRO",xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash",size(medium)) ytitle("Percent") ylabe(0(1)7,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 
 

graph export AbReturnCash_Market.png,replace
graph export AbReturnCash_Market.eps,replace




drop g e
 
egen  e =  max(CAAR)  if RaiseType == "Hybrid"
gen g  = round(e,1) +0.5


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) & (RaiseType == "Hybrid"), bcolor(gs14) base(0) || line CAAR EPeriod if RaiseType == "Hybrid" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Cash & Resereves",size(medium)) ytitle("Percent") ylabe(0(1)9,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 


graph export AbReturnHybrid_Market.png,replace
graph export AbReturnHybrid_Market.eps,replace




drop g e
 
egen  e =  max(CAAR) if RaiseType == "JustSaving"
gen g  = round(e,1) +0.5


twoway bar g EPeriod if ~inrange(t, -1.96 , 1.96) &(RaiseType == "JustSaving"), bcolor(gs14) base(0)  || line CAAR EPeriod  if RaiseType == "JustSaving" ,xlab(-20(10)100,labsize(vsmall))  note("This figure graphs the CAAR from 20 period before event." "The gray area represents significant returns in 5%") title("CAAR After Capital Raise from Resereves",size(medium)) ytitle("Percent") ylabe(0(2)10,angle(0)labsize(vsmall)) xtitle("Period") color(navy) legend(off) || bar g EPeriod if EPeriod == 0 , bcolor(maroon) base(0) barw (0.01) 


graph export AbReturnSaving_Market.png,replace
graph export AbReturnSaving_Market.eps,replace


/**/


/*From Market*/
cls
clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\TradeSumm.xlsx", sheet("Sheet1") firstrow



 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report"

 
 
 
 
 /***/
 twoway connected IndlImbalance  EPeriod   if (RaiseType == "Total") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Individual imbalances After Capital",size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.1(0.05)0.05,angle(0)labsize(vsmall))
 
 

graph export IndImb.png,replace
graph export IndImb.eps,replace

 
  twoway connected InslImbalance  EPeriod   if (RaiseType == "Total") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Institutional imbalances After Capital",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.2(0.1)0.2,angle(0)labsize(vsmall)) 
 
 
graph export InsImb.png,replace
graph export InsImb.eps,replace


/**/
 twoway connected IndlImbalance  EPeriod   if (RaiseType == "Revaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Individual imbalances After Capital from revaluation", size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.05(0.05)0.1,angle(0)labsize(vsmall))
 
 

graph export IndImb_Revaluation.png,replace
graph export IndImb_Revaluation.eps,replace

 /**/
  twoway connected InslImbalance  EPeriod   if (RaiseType == "Revaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Institutional imbalances After Capital  Raise from revaluation",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances")   ylabe(-0.4(0.2)0.4,angle(0)labsize(vsmall)) 
 
 
graph export InsImb_Revaluation.png,replace
graph export InsImb_Revaluation.eps,replace

/**/
 twoway connected IndlImbalance  EPeriod   if (RaiseType == "NoRevaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Individual imbalances After Capital that not from revaluation", size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.1(0.05)0.05,angle(0)labsize(vsmall))
 
 

graph export IndImb_NoRevaluation.png,replace
graph export IndImb_NoRevaluation.eps,replace

 
  twoway connected InslImbalance  EPeriod   if (RaiseType == "NoRevaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Institutional imbalances After Capital that not from revaluation",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances")   ylabe(-0.2(0.1)0.2,angle(0)labsize(vsmall)) 
 
 
graph export InsImb_NoRevaluation.png,replace
graph export InsImb_NoRevaluation.eps,replace

/***/

gen lnVolume = ln(volume)

twoway connected lnVolume  EPeriod   if (RaiseType == "Total") , xline(0) xlab(-20(10)100)  msymbol(O D) title("Volume  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall))

graph export volume.png,replace
graph export volume.eps,replace



twoway connected RelVolume  EPeriod   if (RaiseType == "Total") , xline(0) xlab(-20(10)100)  msymbol(O D) title("Relative Volume  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1)

graph export Relvolume.png,replace
graph export Relvolume.eps,replace

gen lnAmihud = ln(Amihud)

twoway connected lnAmihud  EPeriod   if (RaiseType == "Total") , xline(0)xlab(-20(10)100)  msymbol(O D) title("Amihud measurment  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall))

graph export Amihud.png,replace
graph export Amihud.eps,replace



/***/

twoway connected lnVolume  EPeriod   if (RaiseType == "Revaluation") , xline(0) xlab(-20(10)100)  msymbol(O D) title("Volume  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall))

graph export volume_Revaluation.png,replace
graph export volume_Revaluation.eps,replace

twoway connected RelVolume  EPeriod   if (RaiseType == "Revaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Relative Volume  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1)

graph export Relvolume_Revaluation.png,replace
graph export Relvolume_Revaluation.eps,replace


twoway connected lnAmihud  EPeriod   if (RaiseType == "Revaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Amihud measurment  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall))

graph export Amihud_Revaluation.png,replace
graph export Amihud_Revaluation.eps,replace


/****/

twoway connected lnVolume  EPeriod   if (RaiseType == "NoRevaluation") , xline(0) xlab(-20(10)100)  msymbol(O D) title("Volume  After Capital Raise that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall))

graph export volume_NoRevaluation.png,replace
graph export volume_NoRevaluation.eps,replace

twoway connected RelVolume  EPeriod   if (RaiseType == "NoRevaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Relative Volume  After Capital Raise  that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1)

graph export Relvolume_NoRevaluation.png,replace
graph export Relvolume_NoRevaluation.eps,replace


twoway connected lnAmihud  EPeriod   if (RaiseType == "NoRevaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Amihud measurment  After Capital Raise that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall))

graph export Amihud_NoRevaluation.png,replace
graph export Amihud_NoRevaluation.eps,replace

 
 /**/
