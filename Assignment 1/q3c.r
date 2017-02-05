#!/usr/bin/env Rscript

source("q3a.r")

set_up <- function(name) {
    data <- read.table(name);
    
    i <- seq(1,nrow(data));
    idigit1 <- i[data[i,1] == 2];
    idigit2 <- i[data[i,1] == 8];
    
    digit1 <- t(data[idigit1,2:ncol(data)]);
    digit2 <- t(data[idigit2,2:ncol(data)]);

    size = ncol(digit1) + ncol(digit2);

    w <- matrix(rep(1,ncol(data)),ncol=ncol(data),nrow=1);
    x0 <- matrix(rep(1,size),ncol=size,nrow=1);
    x_temp <- cbind(digit1, digit2);
    x <- rbind(x0,x_temp);
    y_digit1 <- matrix(rep(1,ncol(digit1)),ncol=ncol(digit1),nrow=1);
    y_digit2 <- matrix(rep(-1,ncol(digit2)),ncol=ncol(digit2),nrow=1);
    y <- cbind(y_digit1, y_digit2);

    return(list(x=x,w=w,y=y));
}

main <- function() {
    #extract
    zip_vars <- set_up("data/zip.train");
    feature_vars <- set_up("data/features.train");
    zip_test_vars <- set_up("data/zip.test");
    feature_test_vars <- set_up("data/features.test");

    zip_learned <- percep_mod(zip_vars$x, zip_vars$w, zip_vars$y);
    feature_learned <- percep_mod(feature_vars$x, feature_vars$w, feature_vars$y);
    zip_test_final_errors <- test(zip_test_vars$x, zip_learned$wt, zip_test_vars$y);
    feature_test_final_errors <- test(feature_test_vars$x, feature_learned$wt,feature_test_vars$y);

    ztfel <- large_test(zip_test_vars$x, zip_learned$wdata, zip_test_vars$y);
    ftfel <- large_test(feature_test_vars$x, feature_learned$wdata, feature_test_vars$y);

    x <- seq(1,length(ftfel$fail_num));
    plot(x,ftfel$fail_num);

    feat_lin_w <- linear_reg(feature_vars$x, feature_vars$y);
    feature_lin_learned <- percep_mod(feature_vars$x, feat_lin_w, feature_vars$y);
    ftfel_lin <- large_test(feature_test_vars$x, feature_lin_learned$wdata, feature_test_vars$y);

    x <- seq(1,length(ftfel_lin$fail_num));
    plot(x,ftfel_lin$fail_num, type = 'l', col = 'red');
    lines(x, ftfel$fail_num, col = 'blue');

    print(zip_test_final_errors$fail_num);
    print(feature_test_final_errors$fail_num);

    x <- seq(1,length(zip_learned$rfdata));
    plot(x,zip_learned$rfdata);
    x <- seq(1,length(feature_learned$rfdata));
    plot(x,feature_learned$rfdata, type='l');
    lines(x, feature_lin_learned$rfdata, type='l', col = 'blue');
}

linear_reg <- function(X, Y) {
    #could have used ginv() from MASS library
    x <- t(X);
    y <- t(Y);
    x <- solve(t(x) %*% x) %*% t(x);

    w <- x %*% y;
    return(t(w));

}

large_test <- function(X,WT,y) {
    i <- seq(1, length(X[2,]));
    H <- sign(WT %*% X);

    fail_num <- c();
    for(j in 1:nrow(WT)) {
        fail_num[j] <- length(i[H[j,i] * y[i] < 0]);
    }
    
    return(list(fail_num=fail_num));
}

test <- function(X,WT,y) {
    i <- seq(1, length(X[2,]));
    H <- sign(WT %*% X);
    fail <- i[H[i] * y[i] < 0];
    fail_num <- length(fail);
    return(list(fail=fail, fail_num=fail_num));
}

percep_mod <- function(X, WT, y) {
    wdata <- matrix(,ncol=ncol(WT));
    fdata <- c();
    rfdata <- c();

    iter <- 0;
    repeat {
        fail <- test(X,WT,y);

        wdata <- rbind(wdata, WT);
        fdata <- c(fdata, fail$fail_num);
        rfdata <- c(rfdata, fail$fail_num/length(y));
        

        if ((fail$fail_num < 1) || iter == 1000) {
            break;
        }
        else {
            WT <- WT + y[fail$fail[1]] * t(X[,fail$fail[1]]);
            iter <- iter + 1;
        }
    }

    wdata <- wdata[-1,];
    best <- which.min(fdata);
    WT <- wdata[best,];

    a <- -WT[2]/WT[3];
    b <- -WT[1]/WT[3];
    line <- a*X[2,] + b;
    
    return(list(a=a, b=b, line=line, iter=iter, wt=WT, x=X, wdata=wdata, fdata=fdata, rfdata=rfdata));
}

percep_mod_1 <- function(X, WT, y) {
    wdata <- matrix(,ncol=ncol(WT));
    fdata <- c();
    rfdata <- c();
    minimum <- ncol(X) + 1;
    minW <- WT;

    iter <- 0;
    repeat {
        fail <- test(X,WT,y);

        if(fail$fail_num < minimum) {
            minimum <- fail$fail_num;
            minW <- WT;
        }

        wdata <- rbind(wdata, minW);
        fdata <- c(fdata, minimum);
        rfdata <- c(rfdata, minimum/length(y));
        

        if ((fail$fail_num < 1) || iter == 1000) {
            break;
        }
        else {
            WT <- WT + y[fail$fail[1]] * t(X[,fail$fail[1]]);
            iter <- iter + 1;
        }
    }

    wdata <- wdata[-1,];
    best <- which.min(fdata);
    WT <- wdata[best,];

    a <- -WT[2]/WT[3];
    b <- -WT[1]/WT[3];
    line <- a*X[2,] + b;
    
    return(list(a=a, b=b, line=line, iter=iter, wt=WT, x=X, wdata=wdata, fdata=fdata, rfdata=rfdata));
}

main();
