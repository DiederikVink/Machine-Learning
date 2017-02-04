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
    perceptron(1000,inc,a,b,0);
    
    iter = 100;
    incr <- 50;
    gamma <- 0;
    x <- seq(1,500/incr);
    error <- matrix( , nrow = length(x), ncol = iter);
    updates <- matrix( , nrow=length(x), ncol=iter);
    allt <- matrix( , nrow=length(x), ncol=iter);
    rho <- matrix( , nrow=length(x), ncol=iter);
    w <- matrix(, nrow=length(x), ncol=iter);
    epsilon <- c();

    if (gamma == 0) {
        timer <- proc.time();
        for(i in x) {
            for (j in 1:iter) {
                coeff <- perceptron(incr*i, inc, a, b, gamma);
                updates[i,j] <- coeff$iter;
                #allt[i,j] <- coeff$t;
                #rho[i,j] <- coeff$rho;
                #w[i,j] <- coeff$w;
                error[i,j] <- areas(a, b, coeff$a, coeff$b, gamma, 0);
                epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
            }
        }
        total_time <- proc.time() - timer;
    }
    else {
        error1 <- matrix( , nrow = length(x), ncol = iter);
        error2 <- matrix( , nrow = length(x), ncol = iter);
        timer <- proc.time();
        for(i in x) {
            for (j in 1:iter) {
                coeff <- perceptron(incr*i, inc, a, b, gamma);
                updates[i,j] <- coeff$iter;
                #allt[i,j] <- coeff$t;
                #rho[i,j] <- coeff$rho;
                #w[i,j] <- coeff$w;
                error1[i,j] <- areas(a, b + gamma, coeff$a, coeff$b, gamma, 1);
                error2[i,j] <- areas(a, b - gamma, coeff$a, coeff$b, gamma, -1);
                epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
            }
        }
        total_time <- proc.time() - timer;
        error <- error1 + error2;
    }

    #j <- seq(1,iter);
    #test <- mapply(error_epsilon, x, j, list(incr, inc, a, b, error, epsilon));

    #count <- 0;
    #index <- matrix(,nrow=nrow(rho),ncol=2);

    #for (i in 1:nrow(rho)) {
    #    for (j in 1:ncol(rho)) {
    #        if (rho[i,j] > 0) {
    #            count = count + 1;
    #            index[i,count] <- j;
    #        }
    #        if (count == 2) {
    #            count <- 0;
    #            break;
    #        }
    #    }
    #}
    #print(index);

    non_hoeff <- non_hoeffdings(error);
    error_mean <- rowMeans(error);
    update_mean <- rowMeans(updates);
    t_mean <- rowMeans(allt);

    hoeff_5 <- error_mean - epsilon;
    hoeff_95 <- error_mean + epsilon;
    maximum <- max(hoeff_95)+0.001;
    #if (max(non_hoeff[,95]) > maximum) {maximum <- max(non_hoeff[,95]) + 0.001;}
    minimum <- min(hoeff_5)-0.001;
    #if (min(non_hoeff[,5]) < minimum) {minimum <- min(non_hoeff[,5]) - 0.001;}

    plot(x*incr, seq(minimum,maximum-0.0000001,(maximum-minimum)/(500/incr)), type='n', main = "", xlab = "sample size", ylab = "Error probability");
    lines(x*incr, error_mean, type = 'p');
    lines(lowess(x*incr, error_mean));
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
