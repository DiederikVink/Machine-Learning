#!/usr/bin/env Rscript
source("q3a.r")
source("q3b.r")

main <- function() {
    inc <- 1;
    a <- 1;
    b <- 0.1;

    q3a_main(inc, a, b);
    l;aksjdf;alksjfa;

    iter <- 100;
    incr <- 100;
    gamma <- 0;
    x <- seq(1,500/incr);
    error <- matrix( , nrow = length(x), ncol = iter);
    updates <- matrix( , nrow=length(x), ncol=iter);
    t <- matrix( , nrow=length(x), ncol=iter);
    rho <- matrix( , nrow=length(x), ncol=iter);
    w <- matrix(, nrow=500/incr*iter, ncol=3);
    epsilon <- c();
    broke <- 0;

    if (gamma == 0) {
        timer <- proc.time();
        for(i in x) {
            for (j in 1:iter) {
                coeff <- perceptron(incr*i, inc, a, b, gamma);
                updates[i,j] <- coeff$iter;
                t[i,j] <- coeff$t;
                rho[i,j] <- coeff$rho;
                w[i*j,] <- coeff$w;
                error[i,j] <- areas(a, b, coeff$a, coeff$b, gamma, 0);
                epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
                broke <- broke + coeff$broke;
                print(c(i,j));
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
                t[i,j] <- coeff$t;
                rho[i,j] <- coeff$rho;
                w[i*j,] <- coeff$w;
                error1[i,j] <- areas(a, b + gamma, coeff$a, coeff$b, gamma, 1);
                error2[i,j] <- areas(a, b - gamma, coeff$a, coeff$b, gamma, -1);
                epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
            }
        }
        total_time <- proc.time() - timer;
        error <- error1 + error2;
    }

    w_star <- matrix(,nrow=1,ncol=3);
    j <- seq(1,iter);
    for(i in x) {
        pos <- j[rho[i,j]>0];
        w_star <- rbind(w_star, head(w[pos*i,],2));
    }

    w_star <- w_star[-1,];
    print("wstar");
    print(w_star);

    non_hoeff <- non_hoeffdings(error);
    error_mean <- rowMeans(error);
    update_mean <- rowMeans(updates);
    t_mean <- rowMeans(t);
    print(t);
    print(t_mean);

    hoeff_5 <- error_mean - epsilon;
    hoeff_95 <- error_mean + epsilon;
    maximum <- max(hoeff_95)+0.001;
    #if (max(non_hoeff[,95]) > maximum) {maximum <- max(non_hoeff[,95]) + 0.001;}
    minimum <- min(hoeff_5)-0.001;
    #if (min(non_hoeff[,5]) < minimum) {minimum <- min(non_hoeff[,5]) - 0.001;}

    print(total_time);
    print(broke);
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
}

main()
