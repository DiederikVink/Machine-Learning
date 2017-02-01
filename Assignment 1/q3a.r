#!/usr/bin/env Rscript

perceptron <- function(size, inc, m, c) {
    data <- gen_data(size, inc, m, c);
    class <- classify(data$dist, data$y);
    w <- percep(data$x, data$dist, class);
    plot(data$x, data$dist);
    lines(data$x, data$y, col="blue");
    lines(data$x, w, col = "red");
}

gen_data <- function(size, inc, m, c) {
    x <- seq(1, size+1, inc);
    y <- (m*x) + c; 
    noise <- rnorm(size+1, mean=0, sd=150);
    dist <- y + noise;

    return(list(dist=dist,x=x,y=y));
}

classify <- function(dist, y) {
   x <- seq(1, length(y));
   pos <- x[dist[x] > y[x]];
   neg <- x[dist[x] <= y[x]];
   y[pos] <- -1;
   y[neg] <- 1;

   return(y);
}

percep <- function(x1, x2, y) {
    x0 <- rep(1, length(x1));
    i <- seq(1, length(x1));

    X <- matrix(c(x0, x1, x2), nrow = 3, ncol = length(x1), byrow = TRUE);
    WT <- matrix(rep(1, 3), nrow=1, ncol=3);

    iter <- 0;
    limit <- 50000;
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

    line <- line_calc(WT,X);

    return (line);    
}

line_calc <- function(w, x){
    return(-w[2]/w[3]*x[2,] + w[1]/w[3]);
}

main <- function() {
    inc <- 1;
    m <- 2;
    c <- 3;
    #perceptron(2,inc,m,c);
    #perceptron(4,inc,m,c);
    #perceptron(10,inc,m,c);
    perceptron(100,inc,m,c);
    

    

}

main()
