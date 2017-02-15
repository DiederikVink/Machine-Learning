#!/usr/bin/env Rscript

q3a_main <- function(inc, a, b) {

    inc <- 1;
    a <- 0.75;
    b <- 0.2;
    
    data <- perceptron(2,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 2);
    data <- perceptron(4,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 4);
    data <- perceptron(10,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 10);
    data <- perceptron(100,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 100);

    # produces Figure 7. Eventhough this is not part of q3a, it is easiest to procure this graph
    # in this area of the code.
    data <- perceptron(1000,inc,1,0.1,0.1);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 1000);
}

generate_graphs <- function(x, dist, color, x1, l1, x2, l2, y, line, size) {
    fname <- paste0("results/Q2/q3a-",size, ".pdf");
    #fname <- paste0(fname, ".png");
    pdf(fname);
    main_title <- paste0("Dataset of size: ", size);
    plot(x, dist, 
        col=color,
        main = main_title,
        xlab = "Feature 1 value",
        ylab = "Feature 2 value");
    lines(x1, l1, col = "blue");
    lines(x2, l2, col = "red");
    lines(x, y, col="green");
    lines(x, line, col = "orange");
}

perceptron <- function(size, inc, m, c, gamma) {

    # generate uniformly distributed data
    data <- gen_data_gamma(size, inc, m, c, gamma);

    #create extra coordinate for offset
    x0 <- rep(1, length(data$x));
    # create X and W matrices    
    X <- matrix(c(x0, data$x, data$dist), nrow = 3, ncol = length(data$x), byrow = TRUE);
    WT <- matrix(rep(1, 3), nrow=1, ncol=3);

    # run perceptron alogrithm
    w <- percep(X, WT, data$posneg);
    
    # calculate y*w^T*x
    ywTx <- data$posneg * (w$wt %*% w$x);
    # calculate magnitude of x
    magx <- diag(t(w$x) %*% w$x);
    # calculate rho
    rho <- min(ywTx);
    # calculate magnitude of omega
    magw <- sum(w$wt^2);
    # calculate R^2
    r_sq <- max(magx);
    # calculate upper bound on t
    t <- ((r_sq) * (magw^2))/(rho^2);

    return(list(a=w$a, b=w$b, iter=w$iter, t=t, rho=rho, w=w$wt, broke=w$broke, x=data$x, dist=data$dist, color=data$color, x1=data$x1, x2=data$x2, l1=data$l1, l2=data$l2, y=data$y, line=w$line));
}

gen_data_gamma <- function(size, inc, m, c, gamma) {

    # generate matrix to hold x1,x2 and the corresponding y values
    xdisty <- matrix(,nrow=3, ncol=size);

    i <- 0;
    j <- 0;
    k <- 1;
    count <- 1;
    # continue generating points until ther are 50 left of the line and 50 right of the line region (this includes gamma if it is not zero)
    while((i < (size/2)) || (j < (size/2))) {
        count <- count + 1;
        # generate unifromly distributed feature1(x) and feature2(y) coordinates
        pointx <- runif(1, 0, 1);
        pointy <- runif(1, 0, 1);
        # if the features1,feature2 coordinate is left of the line, save the coordinates and associate a y value of +1 
        if ((pointy > (m*pointx) + c + gamma) && (i < (size/2))) {
            xdisty[1,k] <- pointx;
            xdisty[2,k] <- pointy;
            xdisty[3,k] <- 1;
            i = i + 1;
            k = k + 1;
        }
        # if the features1,feature2 coordinate is right of the line, save the coordinates and associate a y value of -1 
        else if ((pointy < (m*pointx) + c - gamma) && (j < (size/2))) {
            xdisty[1,k] <- pointx;
            xdisty[2,k] <- pointy;
            xdisty[3,k] <- -1;
            j = j + 1;
            k = k + 1;
        }
    }

    #sort the coordinates according to increasing feature1 values
    xysorted <- xdisty[,order(xdisty[1,])];

    # color the dots according to what side of the original line they are on
    i <- seq(1,length(xysorted[1,]));
    pos <- i[xysorted[3,i] == 1];
    neg <- i[xysorted[3,i] == -1];
    color <- seq(1, length(xysorted[1,]));
    color[pos] <- 'blue';
    color[neg] <- 'red';

    # produce the lines to represent all lines present (including the gamma offset lines if those exist)
    y <- (m*xysorted[1,]) + c;
    l1 <- (m*xysorted[1,pos]) + c + gamma;
    x1 <- xysorted[1,pos];
    l2 <- (m*xysorted[1,neg]) + c - gamma;
    x2 <- xysorted[1,neg];

    return(list(dist=xysorted[2,], x=xysorted[1,], posneg=xysorted[3,], y=y, x1=x1, x2=x2, l1=l1, l2=l2, color=color));
}

percep <- function(X, WT, y) {
    i <- seq(1, ncol(X));
    
    # record the amount of times the maximum number of iterations is reached
    broke <- 0;
    
    iter <- 0;
    limit <- 100000;
    repeat {
        # find the value of H
        H <- sign(WT %*% X);
        # find the amount of points that failed the classification using the current values of w
        fail <- i[H[i] * y[i] < 0];

        # if nothing fails, or the iteration limit is reached, end the function
        if ((length(fail) < 1) || iter == limit) {
            if(iter == limit) {
                broke <- 1;
            }
            break;
        }
        # if one or more points failed, update w. Use the first point that failed
        else {
            WT <- WT + y[fail[1]] * t(X[,fail[1]]);
            iter <- iter + 1;
        }
    }

    # calculate the a and b values for y = a*x + b from w, to be able to create a line for the Perceptron-generated line
    a <- -WT[2]/WT[3];
    b <- -WT[1]/WT[3];
    line <- a*X[2,] + b;
    
    return(list(a=a, b=b, line=line, iter=iter, wt=WT, x=X, broke=broke));
}
