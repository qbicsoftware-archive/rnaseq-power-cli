library(RnaSeqSampleSize)

args <- commandArgs(trailingOnly = TRUE)
print(args)
m <- as.numeric(args[1])
m1 <- as.numeric(args[2])
rho <- as.numeric(args[3])
phi0 <- as.numeric(args[4])
f <- as.numeric(args[5])

result<-optimize_parameter(fun=est_power,opt1="n", opt2="lambda0",opt1Value=c(5,10,15,20,25,30,45,50,55,60,65,70), opt2Value=c(1:5,10,20), m=m, m1=m1, rho=rho, phi0=phi0, f=f)
print(result)
