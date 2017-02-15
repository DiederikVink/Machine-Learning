#!/usr/bin/env Rscript

source("q3a.r")
source("q3b.r")

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

q3c_main <- function() {
    sink("results/Q3c/data.out");
    #extract
    zip_vars <- set_up("data/zip.train");
    feature_vars <- set_up("data/features.train");
    zip_test <- set_up("data/zip.test");
    feature_test <- set_up("data/features.test");

    # ZIP - Non-lin Reg
    z_train_new <- percep_mod_1(zip_vars$x, zip_vars$w, zip_vars$y);
    z_train <- percep_mod(zip_vars$x, zip_vars$w, zip_vars$y);
    z_errors_new <- test(zip_test$x, z_train_new$wt, zip_test$y, z_train_new$wdata);
    z_errors <- test(zip_test$x, z_train$wt, zip_test$y, z_train$wdata);
     
    print("Zip data training error (Original algorithm)");
    print(z_train$fdata[length(z_train$fdata)]);
    print("Zip data test error (Original algorithm)");
    print(z_errors$fail_num[length(z_errors$fail_num)]);
    print("Zip data training error (Modified algorithm)");
    print(z_train_new$fdata[length(z_train_new$fdata)]);
    print("Zip data test error (Modified algorithm)");
    print(z_errors_new$fail_num[length(z_errors_new$fail_num)]);

    pdf("results/Q3c/zip_org.pdf")
    x <- seq(1, length(z_train$rfdata));
    plot(x,z_train$rfdata,
        type='n',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Zip Data Relative Error values for Train and Test data \n (Original Perceptron Algorithm)"
    );
    legend("topright", c("Train error", "Test error"),col=c('blue','red'),lty=c(1,1));
    lines(x,z_train$rfdata, col='blue');
    lines(x,z_errors$fail_rel, col='red');

    pdf("results/Q3c/zip_mod.pdf")
    x <- seq(1, length(z_train_new$rfdata));
    plot(x,z_train_new$rfdata,
        type='n',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Zip Data Relative Error values for Train and Test data \n (Modified Perceptron Algorithm)"
    );
    legend("topright", c("Train error", "Test error"),col=c('blue','red'),lty=c(1,1));
    lines(x,z_train_new$rfdata, col='blue');
    lines(x,z_errors_new$fail_rel, col='red');

    # Features - Non-lin Reg
    f_train_new <- percep_mod_1(feature_vars$x, feature_vars$w, feature_vars$y);
    f_train <- percep_mod(feature_vars$x, feature_vars$w, feature_vars$y);
    f_errors_new <- test(feature_test$x, f_train_new$wt, feature_test$y, f_train_new$wdata);
    f_errors <- test(feature_test$x, f_train$wt, feature_test$y, f_train$wdata);
    print("Feature data training error (Original algorithm)");
    print(f_train$fdata[length(f_train$fdata)]);
    print("Feature data test error (Original algorithm)");
    print(f_errors$fail_num[length(f_errors$fail_num)]);
    print("Feature data training error (Modified algorithm)");
    print(f_train_new$fdata[length(f_train_new$fdata)]);
    print("Feature data test error (Modified algorithm)");
    print(f_errors_new$fail_num[length(f_errors_new$fail_num)]);
     
    pdf("results/Q3c/feat_org.pdf")
    x <- seq(1, length(f_train$rfdata));
    plot(x,f_train$rfdata,
        type='n',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Featured Data Relative Error values for Train and Test data \n (Original Perceptron Algorithm)"
    );
    legend("topright", c("Train error", "Test error"),col=c('blue','red'),lty=c(1,1));
    lines(x,f_train$rfdata, col='blue');
    lines(x,f_errors$fail_rel, col='red');

    pdf("results/Q3c/feat_mod.pdf")
    x <- seq(1, length(f_train_new$rfdata));
    plot(x,f_train_new$rfdata,
        type='n',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Featured Data Relative Error values for Train and Test data \n (Modified Perceptron Algorithm)"
    );
    legend("topright", c("Train error", "Test error"),col=c('blue','red'),lty=c(1,1));
    lines(x,f_train_new$rfdata, col='blue');
    lines(x,f_errors_new$fail_rel, col='red');

    # Features - Lin Reg
    f_lin_reg <- linear_reg(feature_vars$x, feature_vars$y);
    f_train_new <- percep_mod_1(feature_vars$x, f_lin_reg, feature_vars$y);
    f_train <- percep_mod(feature_vars$x, f_lin_reg, feature_vars$y);
    f_errors_new <- test(feature_test$x, f_train_new$wt, feature_test$y, f_train_new$wdata);
    f_errors <- test(feature_test$x, f_train$wt, feature_test$y, f_train$wdata);
    print("Feature data training error (Original algorithm)");
    print(f_train$fdata[length(f_train$fdata)]);
    print("Feature data test error (Original algorithm)");
    print(f_errors$fail_num[length(f_errors$fail_num)]);
    print("Feature data training error (Modified algorithm)");
    print(f_train_new$fdata[length(f_train_new$fdata)]);
    print("Feature data test error (Modified algorithm)");
    print(f_errors_new$fail_num[length(f_errors_new$fail_num)]);
     
    pdf("results/Q3c/lin_org.pdf")
    x <- seq(1, length(f_train$rfdata));
    plot(x,f_train$rfdata,
        type='n',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Featured Data Relative Error values for Train and Test data \n (Original Perceptron Algorithm, Using Linear Regression)"
    );
    legend("topright", c("Train error", "Test error"),col=c('blue','red'),lty=c(1,1));
    lines(x,f_train$rfdata, col = 'blue' );
    lines(x,f_errors$fail_rel, col = 'red');

    pdf("results/Q3c/lin_mod_train.pdf")
    x <- seq(1, length(f_train_new$rfdata));
    #plot(x,f_train_new$rfdata,type='l');
    plot(x,f_errors_new$fail_rel, col='red',type='l',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Featured Data Relative Error values for Train data \n (Modified Perceptron Algorithm, Using Linear Regression)"
    );
    pdf("results/Q3c/lin_mod_test.pdf")
    plot(x,f_train_new$rfdata, col='blue',type='l',
        xlab = "Number of perceptron iterations",
        ylab = "Relative Error (%)",
        main = "Featured Data Relative Error values for Train data \n (Modified Perceptron Algorithm, Using Linear Regression)"
    );
}

linear_reg <- function(X, Y) {
    #could have used ginv() from MASS library
    x <- t(X);
    y <- t(Y);
    x <- solve(t(x) %*% x) %*% t(x);

    w <- x %*% y;
    return(t(w));

}

test <- function(X,WT,y,wdata) {
    i <- seq(1, length(X[2,]));
    h_final <- sign(WT %*% X);
    fail <- i[h_final[i] * y[i] < 0];
    fail_perc <- length(fail)/length(y);

    fail_num <- c();
    fail_rel <- c();
    H <- sign(wdata %*% X);
    for(j in 1:nrow(wdata)) {
        fail_num[j] <- length(i[H[j,i] * y[i] < 0]);
        fail_rel[j] <- fail_num[j]/length(y);
    }
    
    return(list(fail_num=fail_num, fail_rel=fail_rel, fail_perc=fail_perc));
}

percep_mod <- function(X, WT, y) {
    wdata <- matrix(,ncol=ncol(WT));
    fdata <- c();
    rfdata <- c();
    i <- seq(1, ncol(X));

    iter <- 0;
    repeat {

        H <- sign(WT %*% X);
        fail <- i[H[i] * y[i] < 0];

        wdata <- rbind(wdata, WT);
        fdata <- c(fdata, length(fail));
        rfdata <- c(rfdata, length(fail)/length(y));

        if ((length(fail) < 1) || iter == 1000) {
            break;
        }
        else {
            WT <- WT + y[fail[1]] * t(X[,fail[1]]);
            iter <- iter + 1;
        }
    }

    wdata <- wdata[-1,];

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
    i <- seq(1, ncol(X));

    iter <- 0;
    repeat {

        H <- sign(WT %*% X);
        fail <- i[H[i] * y[i] < 0];

        if(length(fail) < minimum) {
            minimum <- length(fail);
            minW <- WT;
        }

        wdata <- rbind(wdata, minW);
        fdata <- c(fdata, minimum);
        rfdata <- c(rfdata, minimum/length(y));
        

        if ((length(fail) < 1) || iter == 1000) {
            break;
        }
        else {
            WT <- WT + y[fail[1]] * t(X[,fail[1]]);
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

