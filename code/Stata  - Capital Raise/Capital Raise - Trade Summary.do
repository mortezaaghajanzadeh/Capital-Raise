

/**/

clear
cls
import delimited "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CapitalRaise.csv", encoding(UTF-8) 
cd "D:\Dropbox\Capital Raise\Capital-Raise\Report\Output"
capture drop lnVolume lnAmihud
gen lnAmihud = ln(amihud)
gen lnVolume = ln(volume)



gen RaiseType2 = raisetype
replace RaiseType2 = "NoRevaluation" if raisetype != "Revaluation"

foreach var in indlimbalance inslimbalance relvolume lnAmihud lnVolume hm_ins hm_ind ind_nav ins_nav{
	foreach vv in "NoRevaluation" "Revaluation"{
		display "`vv'"
		capture drop x 
		egen x = mean(`var') if RaiseType2 == "`vv'", by(eperiod) 
		gen `var'`vv' =  x
		capture drop x 
	} 
}

foreach var in ind_navNoRevaluation ind_navRevaluation ins_navNoRevaluation ins_navRevaluation{
		replace `var' = `var'/1e13
}


foreach var in indlimbalance inslimbalance relvolume lnAmihud lnVolume hm_ins hm_ind {
	capture drop x 
	egen x = mean(`var'), by(eperiod) 
	replace `var' =  x
}

foreach var in ind_nav ins_nav  {
	capture drop x 
	egen x = sum(`var'), by(eperiod) 
	replace `var' =  x
}

replace ind_nav = ind_nav/1e13
replace ins_nav = ins_nav/1e13



local e 21
local u = `e' -1

twoway connected ind_nav ins_nav  eperiod  if eperiod <`e' , sort(eperiod)  xline(0) yline(0) xlab(-20(10)`u')  msymbol(O D) title("Traders' NAV around Capital Raise",size(medium))   xtitle("Period")  color(navy)note("This figure graphs the traders' nav. It is defined as BuyedVolume{sub:i,t} * ClosePrice{sub:k,t} + NetSellValue{sub:i,t}")   ytitle("Thousand Billion Toman") legend(label (1 "Individual") label (2 "Institutional") col(4))   

 graph export IndInsNav.png,replace
graph export IndInsNav.eps,replace



twoway connected ind_navRevaluation  ins_navRevaluation   eperiod  if eperiod <`e' , sort(eperiod)  xline(0) yline(0) xlab(-20(10)`u')  msymbol(O D) title("Traders' NAV around Capital Raise from revaluation",size(medium))   xtitle("Period")  color(navy)note("This figure graphs the traders' nav. It is defined as BuyedVolume{sub:i,t} * ClosePrice{sub:k,t} + NetSellValue{sub:i,t}")   ytitle("Thousand Billion Toman") legend(label (1 "Individual") label (2 "Institutional") col(4))   

 graph export IndInsNav_Revaluation.png,replace
graph export IndInsNav_Revaluation.eps,replace

twoway connected ind_navNoRevaluation  ins_navNoRevaluation   eperiod  if eperiod <`e' , sort(eperiod)  xline(0) yline(0) xlab(-20(10)`u')  msymbol(O D) title("Traders' NAV around Capital Raise from non-revaluation",size(medium))   xtitle("Period")  color(navy)note("This figure graphs the traders' nav. It is defined as BuyedVolume{sub:i,t} * ClosePrice{sub:k,t} + NetSellValue{sub:i,t}")   ytitle("Thousand Billion Toman") legend(label (1 "Individual") label (2 "Institutional") col(4))   

 graph export IndInsNav_NoRevaluation.png,replace
graph export IndInsNav_NoRevaluation.eps,replace


 
local e 11
local u = `e' -1
local l = -1 * `u'
local g = -1* `e'

capture drop hm_ind_percent hm_ins_percent

gen hm_ind_percent = hm_ind * 100
gen hm_ins_percent = hm_ins*100
twoway connected hm_ind_percent hm_ins_percent  eperiod  if (eperiod <`e')&(eperiod >`g') , sort(eperiod)  xline(0) yline(0) xlab(`l'(5)`u')  msymbol(O D) title("LSV measure of herd behavior around Capital Raise",size(medium))   xtitle("Period")  color(navy)note("LSV measure equal to |br{sub:it} - E[br{sub:t}]| - E[|br{sub:it} - E[br{sub:t}]|]")   ytitle("Percent") legend(label (1 "Individual") label (2 "Institutional") col(4)) ylabe(,angle(0))



 graph export IndInsHerd.png,replace
graph export IndInsHerd.eps,replace


capture drop hm_ind_percent hm_ins_percent

gen hm_ind_percent = hm_indNoRevaluation * 100
gen hm_ins_percent = hm_insNoRevaluation *100
twoway connected hm_ind_percent hm_ins_percent  eperiod  if (eperiod <`e')&(eperiod >`g') , sort(eperiod)  xline(0) yline(0) xlab(`l'(5)`u')  msymbol(O D) title("LSV measure of herd behavior around Capital Raise from non-revaluation",size(medium))   xtitle("Period")  color(navy)note("LSV measure equal to |br{sub:it} - E[br{sub:t}]| - E[|br{sub:it} - E[br{sub:t}]|]")   ytitle("Percent") legend(label (1 "Individual") label (2 "Institutional") col(4)) ylabe(,angle(0))



 graph export IndInsHerdNoRevaluation.png,replace
graph export IndInsHerdNoRevaluation.eps,replace

capture drop hm_ind_percent hm_ins_percent

gen hm_ind_percent = hm_indRevaluation * 100
gen hm_ins_percent = hm_insRevaluation*100
twoway connected hm_ind_percent hm_ins_percent  eperiod  if (eperiod <`e')&(eperiod >`g') , sort(eperiod)  xline(0) yline(0) xlab(`l'(5)`u')  msymbol(O D) title("LSV measure of herd behavior around Capital Raise from revaluation",size(medium))   xtitle("Period")  color(navy)note("LSV measure equal to |br{sub:it} - E[br{sub:t}]| - E[|br{sub:it} - E[br{sub:t}]|]")   ytitle("Percent") legend(label (1 "Individual") label (2 "Institutional") col(4)) ylabe(,angle(0))



 graph export IndInsHerdRevaluation.png,replace
graph export IndInsHerdRevaluation.eps,replace















local l = -20
local u = 50


 twoway connected indlimbalance  eperiod  , xline(0) yline(0)  xlab(`l'(10)`u')  msymbol(O D) title("Individual imbalances After Capital",size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.1(0.05)0.05,angle(0)labsize(vsmall)) sort(eperiod)
 
 

graph export IndImb.png,replace
graph export IndImb.eps,replace

 
  twoway connected inslimbalance  eperiod  , xline(0) yline(0) xlab(`l'(10)`u')  msymbol(O D) title("Institutional imbalances After Capital",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.2(0.1)0.2,angle(0)labsize(vsmall)) sort(eperiod)
 
 
graph export InsImb.png,replace
graph export InsImb.eps,replace



/***/



twoway connected lnVolume  eperiod   , xline(0) xlab(`l'(10)`u')  msymbol(O D) title("Volume  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall)) sort(eperiod)

graph export volume.png,replace
graph export volume.eps,replace



twoway connected relvolume  eperiod   , xline(0) xlab(`l'(10)`u')  msymbol(O D) title("Relative Volume  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1) sort(eperiod)

graph export relvolume.png,replace
graph export relvolume.eps,replace


twoway connected lnAmihud  eperiod  , xline(0)xlab(`l'(10)`u')  msymbol(O D) title("Amihud measurment  After Capital Raise",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall)) sort(eperiod)

graph export Amihud.png,replace
graph export Amihud.eps,replace

/*****/



/******/

local l = -20
local u = 50



twoway connected lnVolumeRevaluation  eperiod  , xline(0) xlab(`l'(10)`u')  msymbol(O D) title("Volume  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall)) sort(eperiod)

graph export volume_Revaluation.png,replace
graph export volume_Revaluation.eps,replace

twoway connected relvolumeRevaluation  eperiod    , xline(0)  xlab(`l'(10)`u')  msymbol(O D) title("Relative Volume  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1) sort(eperiod)

graph export relvolume_Revaluation.png,replace
graph export relvolume_Revaluation.eps,replace


twoway connected lnAmihudRevaluation  eperiod  , xline(0)  xlab(`l'(10)`u')  msymbol(O D) title("Amihud measurment  After Capital Raise from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall)) sort(eperiod)

graph export Amihud_Revaluation.png,replace
graph export Amihud_Revaluation.eps,replace



twoway connected lnVolumeRevaluation  eperiod   , xline(0) xlab(`l'(10)`u')  msymbol(O D) title("Volume  After Capital Raise that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Volume) ") ylabe(,angle(0) labsize(vsmall))  sort(eperiod)

graph export volume_NoRevaluation.png,replace
graph export volume_NoRevaluation.eps,replace

twoway connected relvolumeNoRevaluation  eperiod   , xline(0)  xlab(`l'(10)`u')  msymbol(O D) title("Relative Volume  After Capital Raise  that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle(" Relative Volume") ylabe(,angle(0) labsize(vsmall)) yline(1) sort(eperiod)

graph export relvolume_NoRevaluation.png,replace
graph export relvolume_NoRevaluation.eps,replace


twoway connected lnAmihudNoRevaluation  eperiod   , xline(0)  xlab(`l'(10)`u')  msymbol(O D) title("Amihud measurment  After Capital Raise that it's not from Revaluation",size(medium))   xtitle("Period")  color(navy)  ytitle("ln(Amihud) ")ylabe(,angle(0) labsize(vsmall)) sort(eperiod)

graph export Amihud_NoRevaluation.png,replace
graph export Amihud_NoRevaluation.eps,replace


 twoway connected indlimbalanceRevaluation  eperiod    , xline(0) yline(0) xlab(`l'(10)`u')  msymbol(O D) title("Individual imbalances After Capital from revaluation", size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.05(0.05)0.1,angle(0)labsize(vsmall)) sort(eperiod)
 
 

graph export IndImb_Revaluation.png,replace
graph export IndImb_Revaluation.eps,replace


twoway connected inslimbalanceRevaluation  eperiod  , xline(0) yline(0) xlab(`l'(10)`u')  msymbol(O D) title("Institutional imbalances After Capital  Raise from revaluation",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances")   ylabe(-0.4(0.2)0.4,angle(0)labsize(vsmall)) sort(eperiod)
 
 
graph export InsImb_Revaluation.png,replace
graph export InsImb_Revaluation.eps,replace

 twoway connected indlimbalanceNoRevaluation eperiod   , xline(0) yline(0) xlab(`l'(10)`u')  msymbol(O D) title("Individual imbalances After Capital that not from revaluation", size(medium))   xtitle("Period")  color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances") ylabe(-0.1(0.05)0.05,angle(0)labsize(vsmall)) sort(eperiod)
 
 

graph export IndImb_NoRevaluation.png,replace
graph export IndImb_NoRevaluation.eps,replace

 
  twoway connected inslimbalanceNoRevaluation  eperiod  , xline(0) yline(0) xlab(`l'(10)`u')  msymbol(O D) title("Institutional imbalances After Capital that not from revaluation",size(medium))   xtitle("Period") color(navy)note("This figure graphs the buy-sell imbalances.""It is defined as the net buying ratio of stock k on date t by a particular type to the amounts bought ""and sold by that type.")   ytitle("Buy-Sell Imbalances")   ylabe(-0.2(0.1)0.2,angle(0)labsize(vsmall)) sort(eperiod)
 
 
graph export InsImb_NoRevaluation.png,replace
graph export InsImb_NoRevaluation.eps,replace




/**/


