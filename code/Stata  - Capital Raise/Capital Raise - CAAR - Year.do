cls
clear
import excel "H:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\CAAR_year.xlsx", sheet("Sheet1") firstrow

 cd "G:\Dropbox\Dropbox\Capital Raise\Report"

 drop if year < 1388
 
 line CAAR EPeriod if RaiseType == "Total", by(year,title("CAAR in days surrounding the capital raise announcements",size(small))) xtitle("Period") color(navy)  xline(0)  ytitle("Percent") xlab(-20(20)100,valuelabel) 
 
 
 graph export AbReturn_year.png,replace
graph export AbReturn_year.eps,replace
 



  line CAAR EPeriod if RaiseType == "NoRevaluation", by(year,title("CAAR in days surrounding the capital raise announcements that it is not from revaluation",size(small))) xtitle("Period") color(navy)  xline(0)  ytitle("Percent") xlab(-20(20)100,valuelabel) 
 
 
 graph export AbReturn_year_NoRevaluation.png,replace
graph export AbReturn_year_NoRevaluation.eps,replace
 
  drop if year < 1391
  drop if year == 1396
  line CAAR EPeriod if RaiseType == "Revaluation", by(year,title("CAAR in days surrounding the revaluation announcements",size(small))) xtitle("Period") color(navy)  xline(0)  ytitle("Percent") xlab(-20(20)100,valuelabel) 
 
 
 graph export AbReturn_year_Revaluation.png,replace
graph export AbReturn_year_Revaluation.eps,replace