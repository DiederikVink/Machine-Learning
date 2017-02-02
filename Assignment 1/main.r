#!/usr/bin/env Rscript
source("q3a.r")
source("q3b.r")

main <- function() {
    inc <- 1;
    #given line of x2 - x1 - 0.1 = 0, c = 1, d = 0.1

    a <- 1;
    b <- 0.1;
    #perceptron(2,inc,a,b);
    #perceptron(4,inc,a,b);
    #perceptron(10,inc,a,b);
    
    iter = 100;
    incr <- 50;
    x <- seq(1,500/incr);
    error <- matrix( , nrow = length(x), ncol = iter);
    epsilon <- c();

    timer <- proc.time();
    for(i in x) {
        for (j in 1:iter) {
            coeff <- perceptron(incr*i, inc, a, b);
            error[i,j] <- areas(a, b, coeff$a, coeff$b);
            epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
        }
    }
    total_time <- proc.time() - timer;
    

    
    
    non_hoeff <- non_hoeffdings(error);
    mean <- rowMeans(error);
    hoeff_5 <- mean - epsilon;
    hoeff_95 <- mean + epsilon;
    maximum <- max(hoeff_95)+0.001;
    minimum <- min(hoeff_5)-0.001;

    plot(x*incr, seq(minimum,maximum-0.0000001,(maximum-minimum)/(500/incr)), type='n', main = "", xlab = "sample size", ylab = "Error probability");
    lines(x*incr, mean, type = 'p');
    lines(lowess(x*incr, mean));
    lines(x*incr, non_hoeff[,5], col="blue", type = 'p');
    lines(lowess(x*incr, non_hoeff[,5]), col="blue");
    lines(x*incr, non_hoeff[,95], col="red", type = 'p');
    lines(lowess(x*incr, non_hoeff[,95]), col = "red");
    lines(x*incr, hoeff_5, col="green", type = 'p');
    lines(lowess(x*incr, hoeff_5), col = "green");
    lines(x*incr, hoeff_95, col="orange", type = 'p');
    lines(lowess(x*incr, hoeff_95), col = "orange");
    print(total_time);
}

main()
