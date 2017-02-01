#!/usr/bin/env Rscript

perceptron <- function(size, inc, m, c) {
    data <- gen_data(size, inc, m, c);
    class <- classify(data$dist, data$y);
    w <- percep(data$x, data$dist, class$posneg);
    plot(data$x, data$dist, col=class$color);
    lines(data$x, data$y, col="blue");
    lines(data$x, w$line, col = "red");
    return(list(a=w$a, b=w$b));
}

gen_data <- function(size, inc, m, c) {
    x <- seq(0, 1, inc/(size-1));
    x <- c(1, x);
    y <- (m*x) + c;
    noise <- rnorm(size+1, mean=0, sd=150);
    dist <- y + noise;
    dist <- abs(dist);
    dist <- dist/max(dist);

    return(list(dist=dist,x=x,y=y));
}

classify <- function(dist, y) {
   x <- seq(1, length(y));
   color <- seq(1, length(y));
   pos <- x[dist[x] > y[x]];
   neg <- x[dist[x] <= y[x]];
   y[pos] <- -1;
   y[neg] <- 1;
   color[pos] <- 'blue';
   color[neg] <- 'red';

   return(list(posneg=y, color=color));
}

percep <- function(x1, x2, y) {
    x0 <- rep(1, length(x1));
    i <- seq(1, length(x1));

    X <- matrix(c(x0, x1, x2), nrow = 3, ncol = length(x1), byrow = TRUE);
    WT <- matrix(rep(1, 3), nrow=1, ncol=3);

    iter <- 0;
    limit <- 1000;
    while (iter < limit) {
        H <- sign(WT %*% X);
        fail <- i[H[i] * y[i] < 0];

        if (length(fail) < 1) {
            iter <- limit;
        }
        else {
            WT <- WT + y[fail[1]] * t(X[,fail[1]]);
            iter <- iter + 1;
        }
    }

    a <- -WT[2]/WT[3];
    b <- -WT[1]/WT[3];
    line <- a*X[2,] + b;
    
    return(list(a=a, b=b, line=line));    
}
