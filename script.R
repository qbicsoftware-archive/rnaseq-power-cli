library(RnaSeqSampleSize)

args <- commandArgs(trailingOnly = TRUE)
print(args)
# trailingOnly=TRUE means that only your arguments are returned, check:
# print(commandArgs(trailingOnly=FALSE))
n <- as.numeric(args[1])
rho <- as.numeric(args[2])
lambda0 <- as.numeric(args[3])
phi0 <- as.numeric(args[4])
f <- as.numeric(args[5])

est_power(n=n, rho=rho, lambda0=lambda0, phi0=phi0,f=f)
