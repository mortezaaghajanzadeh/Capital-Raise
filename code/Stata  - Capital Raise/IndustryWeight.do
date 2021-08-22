local x  "Weight"

/*Abnormal Return */

foreach var in meanvar se p25 p95 n t_stat e g{
	capture drop `var'
}
capture drop meanvar1
egen meanvar1 = mean(`x'), by(EPeriod) 
gen meanvar = meanvar1*100
egen se = sd(`x'), by(EPeriod) 
gen p95 = meanvar + 1.96 * se
gen p25 = meanvar - 1.96 * se 


twoway  line meanvar EPeriod , xlab(-20(10)100,labsize(vsmall)) sort(EPeriod) note("Firm's weight in their industry." ) title("Weight in Indusytry") ytitle("Percent") ylabe(,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) 

graph export `x'.png,replace
graph export `x'.eps,replace

twoway  line meanvar EPeriod , xlab(-20(10)100,labsize(vsmall)) sort(EPeriod) note("Firm's weight in their industry." ) title("Weight in Indusytry") ytitle("Percent") ylabe(,angle(0) labsize(vsmall)) xtitle("Period") color(navy) legend(off) || rcap p95 p25 EPeriod if mod(EPeriod,2) == 1

graph export `x'confidence.png,replace
graph export `x'confidence.eps,replace