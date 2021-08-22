



/**/
clear
cls
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\QVDate.xlsx", sheet("Sheet1") firstrow

 cd "D:\Dropbox\Capital Raise\Capital-Raise\Report\Output"

generate var1 = "Spring" in 1

replace var1 = "Summer" in 2

replace var1 = "Fall" in 3

replace var1 = "Winter" in 4




graph bar Sum, over(var1)  ylab(,angle(hori)) ytitle("Number") title("Number of Capital Raise in Quarter")
graph export QNumber.png,replace
graph export QNumber.eps,replace



graph bar Cash Reserves  Hybrid   , over(var1)  ylab(,angle(hori)) ytitle("Number") stack legend(label (1 "Cash") label (2 "Reserves")label (4 "Premium")label (3 "Cash&Reserves") col(4)) title("Number of Capital Raise in Quarter ")

graph export QNumber2.png,replace
graph export QNumber2.eps,replace

graph bar Cash Reserves  Hybrid   , over(var1)  ylab(,angle(hori)) ytitle("Number")  legend(label (1 "Cash") label (2 "Reserves")label (4 "Premium")label (3 "Cash&Reserves") col(4)) title("Number of Capital Raise in Quarter")

graph export QNumber3.png,replace
graph export QNumber3.eps,replace




/**/




/**/

clear
import excel "G:\Economics\Finance(Prof.Heidari-Aghajanzadeh)\Data\Capital Rise\SummaryCapitalData.xlsx", sheet("Sheet1") firstrow
cd "D:\Dropbox\Capital Raise\Capital-Raise\Report\Output"

twoway bar Number year, xlab(1383(1)1398,angle(vertical)) title("Number of Capital Raise ") ytitle("Number") ylab(0(20)140,angle(hori))

graph export Number.png,replace
graph export Number.eps,replace




graph bar JustRO JustSaving  Hybrid   Revaluation, over(year , lab(angle(90))) stack  title("Number of Capital Raise ") ytitle("Number") ylab(0(20)140,angle(hori)) legend(label (1 "Cash") label (2 "Reserves")label (3 "Cash & Resereves") label(4 "Revaluation") col(2))

graph export Number2.png,replace
graph export Number2.eps,replace

gen PJustRO = JustRO/Number *100
gen PJustSaving    = JustSaving/Number *100
gen PHybrid = Hybrid/Number *100
gen PJustPremium = JustPremium/Number *100

gen PRevaluation = Revaluation/Number *100


graph bar PJustRO PJustSaving  PHybrid  PRevaluation, over(year , lab(angle(90)))  title("Percent of each type of Capital Raise ") ytitle("Percent") legend(label (1 "Cash") label (2 "Reserves")label (4 "Premium")label (3 "Cash & Resereves") label(4 "Revaluation") col(2)) ylab(0(15)75,angle(hori))

graph export Number3.png,replace
graph export Number3.eps,replace




twoway bar MedianPercent year , xlab(1383(1)1398,angle(vertical)) ylab(20(10)100)  title("Median of Percent of Capital Raise") ytitle("Percent")


graph export MedianPercent.png,replace
graph export MedianPercent.eps,replace

replace MedianCapRaise = MedianCapRaise/10000

twoway bar MedianCapRaise year , xlab(1383(1)1398,angle(vertical))   title("Median of Raised Capital") ytitle("Billion Tomans")


graph export MedianCapRaise.png,replace
graph export MedianCapRaise.eps,replace


gen MedianCapRaiseAdjusted = MedianCapRaise / Inflation

twoway bar MedianCapRaiseAdjusted year , xlab(1383(1)1398,angle(vertical)) ylab(0(20)100)   title("Median of Raised Capital ")subtitle("(adjusted by CPI base on 1398)") ytitle("Billion Tomans")


graph export MedianCapRaiseAdjusted.png,replace
graph export MedianCapRaiseAdjusted.eps,replace





replace MeanCapRaise = MeanCapRaise/10000

twoway bar MeanCapRaise year , xlab(1383(1)1398,angle(vertical))   title("Mean of Raised Capital") ytitle("Billion Tomans")


graph export MeanCapRaise.png,replace
graph export MeanCapRaise.eps,replace


gen MeanCapRaiseAdjusted = MeanCapRaise / Inflation

twoway bar MeanCapRaiseAdjusted year , xlab(1383(1)1398,angle(vertical))  ylab(0(250)1000)  title("Mean of Raised Capital ")subtitle("(adjusted by CPI base on 1398)") ytitle("Billion Tomans")


graph export MeanCapRaiseAdjusted.png,replace
graph export MeanCapRaiseAdjusted.eps,replace






replace Sum = Sum/10000000
twoway bar Sum year , xlab(1383(1)1398,angle(vertical))   title("Sum of Raised Capital") ytitle("Thousand Billion Tomans ")


graph export SumCapRaise.png,replace
graph export SumCapRaise.eps,replace

gen SumAdjusted = Sum / Inflation

twoway bar SumAdjusted year , xlab(1383(1)1398,angle(vertical))   title("Sum of Raised Capital ") subtitle("(adjusted by CPI base on 1398)") ytitle("Thousand Billion Tomans ")


graph export SumCapRaiseAdjusted.png,replace
graph export SumCapRaiseAdjusted.eps,replace


twoway bar SumAdjusted year , xlab(1383(1)1398,angle(vertical))   title("Sum of Raised Capital ")subtitle("(adjusted by CPI base on 1398)") ytitle("Thousand Billion Tomans ")

foreach v in Sum_Revaluation Sum_RO Sum_Premium Sum_Saving Sum_Hybrid{
	gen Adjusted`v' = `v' / Inflation /10000000
}

   

graph bar AdjustedSum_RO AdjustedSum_Saving  AdjustedSum_Hybrid  AdjustedSum_Revaluation, stack over(year , lab(angle(90)))  title("Sum of the raised capital for each type")subtitle("(adjusted by CPI base on 1398)") legend(label (1 "Cash") label (2 "Reserves")label (4 "Premium")label (3 "Cash & Resereves") label(4 "Revaluation") col(2)) ylab(0(20)100,angle(hori)) ytitle("Thousand Billion Tomans ") 
 graph export SumCapRaiseAdjustedEachtype.png,replace
graph export SumCapRaiseAdjustedEachtype.eps,replace
