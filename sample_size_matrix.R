library(RnaSeqSampleSize)
library(heatmap3)

args <- commandArgs(trailingOnly = TRUE)
print(args)
m <- as.numeric(args[1]) # number of genes
m1 <- as.numeric(args[2]) # expected number of DE genes
phi0 <- as.numeric(args[3]) # dispersion
f <- as.numeric(args[4]) # FDR
power <- as.numeric(args[5]) # power (sensitivity)
result_file <- args[6]

result<-optimize_parameter(fun=sample_size,opt1="rho", opt2="lambda0",opt1Value=c(1.1,2,3,4), opt2Value=c(1:5,10,20), power=power, m=m, m1=m1, phi0=phi0, f=f)
print(result)
pdf(result_file)
heatmap3(result, Colv = NA, Rowv = NA, xlab = "Log fold change", ylab = "Average read count per gene", scale = "n", col = matlab::jet.colors(1000), cexCol = 1, cexRow = 1, lasCol = 1, lasRow = 1, main = "Minimum sample size (per group)")
dev.off()
