mydf <- read.table("sample.csv", header = TRUE, as.is = FALSE)
row.names(mydf) <- mydf[ , 1]
mydf <- mydf[ , -1]
library(DESeq2)
up_quantile <- function(df){
  up_quantile_value = as.numeric()
  for (i in 1:length(names(df))){
    x <- df[ , i]
    x <- x[x > 0]
    up_quantile_value <- c(up_quantile_value, quantile(x)["75%"])
  }
  up_quantile_mean <- mean(up_quantile_value)
  for (i in 1:length(names(df))){
    df[ , i] <- df[ , i] * up_quantile_mean / up_quantile_value[i]
  }
  return(df)
}

DE_Seq <- function(df){
  ratio <- data.frame()
  for (i in 1:length(row.names(df))){
    x <- as.numeric(df[i, ])
    geometric_mean <- exp(mean(log(x)))
    if (geometric_mean > 0){
      row <- df[i, ] / geometric_mean
      ratio <- rbind(ratio, row)
    }
  }
  geometric_mean_median <- as.numeric()
  for (i in 1:length(names(ratio))){
    geometric_mean_median <- c(geometric_mean_median, median(ratio[ , i]))
  }
  for (i in 1:length(names(df))){
    df[ , i] <- df[ , i] / geometric_mean_median[i]
  }
  return(df)
}
mydf2 <- up_quantile(mydf)
mydf3 <- up_quantile(mydf2)
mydf4 <- DE_Seq(mydf)
mydf5 <- DE_Seq(mydf4)
write.table(mydf2,file = "norm.csv")