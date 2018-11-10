library(RnaSeqSampleSize)

args <- commandArgs(trailingOnly = TRUE)
print(args)
m <- as.numeric(args[1]) # number of genes
m1 <- as.numeric(args[2]) # expected number of DE genes
rho <- as.numeric(args[3]) # minimum detectable log fold change
phi0 <- as.numeric(args[4]) # dispersion
f <- as.numeric(args[5]) # FDR

result<-optimize_parameter(fun=est_power,opt1="n", opt2="lambda0",opt1Value=c(5,10,15,20,25,30,45,50,55,60,65,70), opt2Value=c(1:5,10,20), m=m, m1=m1, rho=rho, phi0=phi0, alpha=f)
print(result)
pdf("power.pdf") 
heatmap3(result, Colv = NA, Rowv = NA, xlab = "Samples per Group", ylab = "Average read count per gene", scale = "n", col = matlab::jet.colors(1000), cexCol = 1, cexRow = 1, lasCol = 1, lasRow = 1, main = "Power (sensitivity)")
dev.off()
