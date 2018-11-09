library(RnaSeqSampleSize)

args <- commandArgs(trailingOnly = TRUE)
print(args)
# trailingOnly=TRUE means that only your arguments are returned, check:
# print(commandArgs(trailingOnly=FALSE))
n <- args[1]
rho <- args[2]
lambda0 <- args[3]
phi0 <- args[4]
f <- args[5]

est_power(n=n, rho=rho, lambda0=lambda0, phi0=phi0,f=f)
