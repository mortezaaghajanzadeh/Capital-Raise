
capture drop lnVolume lnAmihud
gen lnAmihud = ln(Amihud)
gen lnVolume = ln(volume)
foreach var in IndlImbalance InslImbalance RelVolume lnAmihud lnVolume{
	capture drop x 
	egen x = mean(`var'), by(EPeriod) 
	replace `var' =  x
}

gen RaiseType2 = RaiseType
replace RaiseType2 = "NoRevaluation" if RaiseType != "Revaluation"



 twoway connected IndlImbalance  EPeriod  , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Individual imbalances After Capital",size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.1(0.05)0.05,angle(0)labsize(vsmall)) sort(EPeriod)
 
 

graph export IndImb.png,replace
graph export IndImb.eps,replace

 
  twoway connected InslImbalance  EPeriod  , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Institutional imbalances After Capital",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.2(0.1)0.2,angle(0)labsize(vsmall)) sort(EPeriod)
 
 
graph export InsImb.png,replace
graph export InsImb.eps,replace


/**/
 twoway connected IndlImbalance  EPeriod   if (RaiseType2 == "Revaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Individual imbalances After Capital from revaluation", size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.05(0.05)0.1,angle(0)labsize(vsmall)) sort(EPeriod)
 
 

graph export IndImb_Revaluation.png,replace
graph export IndImb_Revaluation.eps,replace

 /**/
  twoway connected InslImbalance  EPeriod   if (RaiseType2 == "Revaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Institutional imbalances After Capital  Raise from revaluation",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances")   ylabe(-0.4(0.2)0.4,angle(0)labsize(vsmall)) sort(EPeriod)
 
 
graph export InsImb_Revaluation.png,replace
graph export InsImb_Revaluation.eps,replace

/**/
 twoway connected IndlImbalance  EPeriod   if (RaiseType2 == "NoRevaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Individual imbalances After Capital that not from revaluation", size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.1(0.05)0.05,angle(0)labsize(vsmall)) sort(EPeriod)
 
 

graph export IndImb_NoRevaluation.png,replace
graph export IndImb_NoRevaluation.eps,replace

 
  twoway connected InslImbalance  EPeriod   if (RaiseType2 == "NoRevaluation") , xline(0) yline(0) xlab(-20(10)100)  msymbol(O D) title("Institutional imbalances After Capital that not from revaluation",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances")   ylabe(-0.2(0.1)0.2,angle(0)labsize(vsmall)) sort(EPeriod)
 
 
graph export InsImb_NoRevaluation.png,replace
graph export InsImb_NoRevaluation.eps,replace

/***/



twoway connected lnVolume  EPeriod   , xline(0) xlab(-20(10)100)  msymbol(O D) title("Volume  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall)) sort(EPeriod)

graph export volume.png,replace
graph export volume.eps,replace



twoway connected RelVolume  EPeriod   , xline(0) xlab(-20(10)100)  msymbol(O D) title("Relative Volume  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1) sort(EPeriod)

graph export Relvolume.png,replace
graph export Relvolume.eps,replace


twoway connected lnAmihud  EPeriod  , xline(0)xlab(-20(10)100)  msymbol(O D) title("Amihud measurment  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall)) sort(EPeriod)

graph export Amihud.png,replace
graph export Amihud.eps,replace



/***/

twoway connected lnVolume  EPeriod   if (RaiseType2 == "Revaluation") , xline(0) xlab(-20(10)100)  msymbol(O D) title("Volume  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall)) sort(EPeriod)

graph export volume_Revaluation.png,replace
graph export volume_Revaluation.eps,replace

twoway connected RelVolume  EPeriod   if (RaiseType2 == "Revaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Relative Volume  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1) sort(EPeriod)

graph export Relvolume_Revaluation.png,replace
graph export Relvolume_Revaluation.eps,replace


twoway connected lnAmihud  EPeriod   if (RaiseType2 == "Revaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Amihud measurment  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall)) sort(EPeriod)

graph export Amihud_Revaluation.png,replace
graph export Amihud_Revaluation.eps,replace


/****/

twoway connected lnVolume  EPeriod   if (RaiseType2 == "NoRevaluation") , xline(0) xlab(-20(10)100)  msymbol(O D) title("Volume  After Capital Raise that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall))  sort(EPeriod)

graph export volume_NoRevaluation.png,replace
graph export volume_NoRevaluation.eps,replace

twoway connected RelVolume  EPeriod   if (RaiseType2 == "NoRevaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Relative Volume  After Capital Raise  that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1) sort(EPeriod)

graph export Relvolume_NoRevaluation.png,replace
graph export Relvolume_NoRevaluation.eps,replace


twoway connected lnAmihud  EPeriod   if (RaiseType2 == "NoRevaluation") , xline(0)  xlab(-20(10)100)  msymbol(O D) title("Amihud measurment  After Capital Raise that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall)) sort(EPeriod)

graph export Amihud_NoRevaluation.png,replace
graph export Amihud_NoRevaluation.eps,replace

 
 /**/