library(RnaSeqSampleSize)

args <- commandArgs(trailingOnly = TRUE)
print(args)
m <- as.numeric(args[1])
m1 <- as.numeric(args[2])
phi0 <- as.numeric(args[3])
f <- as.numeric(args[4])
power <- as.numeric(args[5])

result<-optimize_parameter(fun=sample_size,opt1="rho", opt2="lambda0",opt1Value=c(1.1,2,3,4), opt2Value=c(1:5,10,20), power=power, m=m, m1=m1, phi0=phi0, f=f)
print(result)
