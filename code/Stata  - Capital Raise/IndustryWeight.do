local x  "weight"

/*Weight change*/

foreach var in meanvar se p25 p95 n t_stat e g aftervalue beforevalue {
	capture drop `var'
}
capture drop meanvar1
egen meanvar1 = mean(`x'), by(eperiod) 
gen meanvar = meanvar1*100
egen se = sd(`x') , by(eperiod) 
gen p95 = meanvar + 1.96 * se
gen p25 = meanvar - 1.96 * se 

egen aftervalue = mean(meanvar)  if eperiod> 0
replace aftervalue = .  if eperiod < 0

egen beforevalue = mean(meanvar)  if eperiod<0
replace beforevalue = .  if eperiod >= 0



twoway  line meanvar eperiod , xlab(-20(20)100,labsize(vsmall)) sort(eperiod) note("Firm's weight in their industry." ) title("Weight in Indusytry") ytitle("Percent") ylabe(,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) xline(0) || line aftervalue eperiod || line beforevalue eperiod 

graph export `x'.png,replace
graph export `x'.eps,replace

twoway  line meanvar eperiod , xlab(-20(20)100,labsize(vsmall)) sort(eperiod) note("Firm's weight in their industry." ) title("Weight in Indusytry") ytitle("Percent") ylabe(,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || rcap p95 p25 eperiod if mod(eperiod,2) == 1 ,xline(0)

graph export `x'confidence.png,replace
graph export `x'confidence.eps,replace