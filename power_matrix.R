library(RnaSeqSampleSize)
library(heatmap3)

args <- commandArgs(trailingOnly = TRUE)
print(args)
mode <- args[1] # data, tcga or none
m <- as.numeric(args[2]) # number of genes
m1 <- as.numeric(args[3]) # expected number of DE genes
n <- as.numeric(args[4]) # sample size
#rho <- as.numeric(args[3]) # minimum detectable log fold change
f <- as.numeric(args[5]) # FDR

if(mode=="none") {
  phi0 <- as.numeric(args[6]) # dispersion
  #lambda0 <- as.numeric(args[6]) # avg. read count/gene
  result_file <- args[7]
}
if(mode=="tcga") {
  tcga <- args[6]
  result_file <- args[7]
  data(list = tcga)
  repNumber = 10
  temp <- RnaSeqSampleSize:::selectDistribution(distributionObject = tcga, repNumber = repNumber, dispersionDigits = 2,
      minAveCount = 5, maxAveCount = 2000,
      seed = 123,
      species = "hsa")
  dispersionDistribution <- temp$selectedDispersion
  countDistribution <- temp$selectedCount
  phi0 <- temp$maxDispersionDistribution
  #lambda0 <- max(min(countDistribution), 1)
}

result<-optimize_parameter(fun=est_power,opt1="rho", opt2="lambda0",opt1Value=c(1.1,2,3,4), opt2Value=c(1:5,10,15,20,25), m=m, m1=m1, n=n, phi0=phi0, alpha=f)
#result<-optimize_parameter(fun=est_power,opt1="n", opt2="lambda0",opt1Value=c(5,10,15,20,25,30,45,50,55,60,65,70), opt2Value=c(1:5,10,20), m=m, m1=m1, rho=rho, phi0=phi0, alpha=f)
print(result)
pdf(result_file) 
heatmap3(result, Colv = NA, Rowv = NA, xlab = "Minimum detectable log fold change", ylab = "Average read count per gene", scale = "n", col = matlab::jet.colors(1000), cexCol = 1, cexRow = 1, lasCol = 1, lasRow = 1, main = "Power (sensitivity)")
#heatmap3(result, Colv = NA, Rowv = NA, xlab = "Samples per Group", ylab = "Average read count per gene", scale = "n", col = matlab::jet.colors(1000), cexCol = 1, cexRow = 1, lasCol = 1, lasRow = 1, main = "Power (sensitivity)")
dev.off()
