library(RnaSeqSampleSize)
library(heatmap3)

args <- commandArgs(trailingOnly = TRUE)
print(args)

mode <- args[1] # mode: data, tcga, none
m <- as.numeric(args[2]) # number of genes
m1 <- as.numeric(args[3]) # expected number of DE genes
f <- as.numeric(args[4]) # FDR

if(mode=="none") {
  phi0 <- as.numeric(args[5]) # dispersion
  lambda0 <- as.numeric(args[6]) # avg. read count/gene
  result_file <- args[7]
}
if(mode=="tcga") {
  tcga <- args[5]
  result_file <- args[6]
  data(list = tcga)
  repNumber = 10
  temp <- RnaSeqSampleSize:::selectDistribution(distributionObject = tcga, repNumber = repNumber, dispersionDigits = 2,
      minAveCount = 5, maxAveCount = 2000,
      seed = 123,
      species = "hsa")
  dispersionDistribution <- temp$selectedDispersion
  countDistribution <- temp$selectedCount
  phi0 <- temp$maxDispersionDistribution
  lambda0 <- max(min(countDistribution), 1)
}

#power <- as.numeric(args[7]) # power (sensitivity)

result<-optimize_parameter(fun=sample_size,opt1="rho", opt2="power",opt1Value=c(1.5,2,3,4), opt2Value=c(0.5,0.6,0.7,0.8,0.9,0.95), lambda0=lambda0, m=m, m1=m1, phi0=phi0, f=f)
#result<-optimize_parameter(fun=sample_size,opt1="rho", opt2="lambda0",opt1Value=c(1.1,2,3,4), opt2Value=c(1:5,10,20), power=power, m=m, m1=m1, phi0=phi0, f=f)
print(result)
pdf(result_file)
heatmap3(result, Colv = NA, Rowv = NA, xlab = "Log fold change", ylab = "Sensitivity (power)", scale = "n", col = matlab::jet.colors(1000), cexCol = 1, cexRow = 1, lasCol = 1, lasRow = 1, main = "Minimum sample size (per group)")
#heatmap3(result, Colv = NA, Rowv = NA, xlab = "Log fold change", ylab = "Average read count per gene", scale = "n", col = matlab::jet.colors(1000), cexCol = 1, cexRow = 1, lasCol = 1, lasRow = 1, main = "Minimum sample size (per group)")
dev.off()
