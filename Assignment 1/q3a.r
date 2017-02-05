#!/usr/bin/env Rscript

q3a_main <- function(inc, a, b) {
    data <- perceptron(2,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 2);
    data <- perceptron(4,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 4);
    data <- perceptron(10,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 10);
    data <- perceptron(100,inc,a,b,0);
    generate_graphs(data$x, data$dist, data$color, data$x1, data$l1, data$x2, data$l2, data$y, data$line, 100);

}

generate_graphs <- function(x, dist, color, x1, l1, x2, l2, y, line, size) {
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
    #if (gamma == 0) {
    #    data <- gen_data(size, inc, m, c);
    #    class <- classify(data$dist, data$y);
    #}
    #else {
        data <- gen_data_gamma_2(size, inc, m, c, gamma);
        class <- list(posneg = data$posneg, color = data$color);
    #}
    x0 <- rep(1, length(data$x));

    X <- matrix(c(x0, data$x, data$dist), nrow = 3, ncol = length(data$x), byrow = TRUE);
    WT <- matrix(rep(1, 3), nrow=1, ncol=3);

    w <- percep(X, WT, class$posneg);
    
    ywTx <- class$posneg * (w$wt %*% w$x);
    magx <- diag(t(w$x) %*% w$x);

    rho <- min(ywTx);
    magw <- sum(w$wt^2);
    r_sq <- max(magx);

    t <- ((r_sq) * (magw^2))/(rho^2);

    #w <- percep1(data$x, data$dist, class$posneg);
    #w$wt<-w$iter<-rho<-t<-0;
    #if (w$broke) {
    #    print("----------------");
    #}

    return(list(a=w$a, b=w$b, iter=w$iter, t=t, rho=rho, w=w$wt, broke=w$broke, x=data$x, dist=data$dist, color=class$color, x1=data$x1, x2=data$x2, l1=data$l1, l2=data$l2, y=data$y, line=w$line));
}

gen_data_gamma_2 <- function(size, inc, m, c, gamma) {

    xdisty <- matrix(,nrow=3, ncol=size);

    i <- 0;
    j <- 0;
    k <- 1;
    count <- 1;
    while((i < (size/2)) || (j < (size/2))) {
        count <- count + 1;
        pointx <- runif(1, 0, 1);
        pointy <- runif(1, 0, 1);
        if ((pointy > (m*pointx) + c + gamma) && (i < (size/2))) {
            xdisty[1,k] <- pointx;
            xdisty[2,k] <- pointy;
            xdisty[3,k] <- 1;
            i = i + 1;
            k = k + 1;
        }
        else if ((pointy < (m*pointx) + c - gamma) && (j < (size/2))) {
            xdisty[1,k] <- pointx;
            xdisty[2,k] <- pointy;
            xdisty[3,k] <- -1;
            j = j + 1;
            k = k + 1;
        }
    }

    xysorted <- xdisty[,order(xdisty[1,])];

    i <- seq(1,length(xysorted[1,]));
    pos <- i[xysorted[3,i] == 1];
    neg <- i[xysorted[3,i] == -1];
    color <- seq(1, length(xysorted[1,]));
    color[pos] <- 'blue';
    color[neg] <- 'red';

    y <- (m*xysorted[1,]) + c;
    l1 <- (m*xysorted[1,pos]) + c + gamma;
    x1 <- xysorted[1,pos];
    l2 <- (m*xysorted[1,neg]) + c - gamma;
    x2 <- xysorted[1,neg];

    return(list(dist=xysorted[2,], x=xysorted[1,], posneg=xysorted[3,], y=y, x1=x1, x2=x2, l1=l1, l2=l2, color=color));
}

gen_data_gamma <- function(size, inc, m, c, gamma) {
    yinter1 <- (1 - (c + gamma))/m;
    if (yinter1 > 1) {yinter <- 1};

    xinter1 <- (0 - (c + gamma))/m;
    if (xinter1 < 0) {xinter1 <- 0};
    
    yinter2 <- (1 - (c - gamma))/m;
    if (yinter2 > 1) {yinter2 <- 1};

    xinter2 <- (0 - (c - gamma))/m;
    if (xinter2 < 0) {xinter2 <- 0};

    xl1 <- seq(xinter1, yinter1, ((yinter1-xinter1)/((size/2)-1)));
    xl2 <- seq(xinter2, yinter2, ((yinter2-xinter2)/((size/2)-1)));

    l1 <- (m*xl1) + c + gamma;
    l2 <- (m*xl2) + c - gamma;

    dist1 <- runif(length(xl1), l1, 1);
    dist2 <- runif(length(xl2), 0, l2);

    y1 <- rep(1, length(xl1));
    y2 <- rep(-1, length(xl2));

    xdisty1 <- matrix(rbind(xl1, dist1, y1), nrow=3);
    xdisty2 <- matrix(rbind(xl2, dist2, y2), nrow=3);
    xy <- matrix(cbind(xdisty1, xdisty2), nrow=3);

    xysorted <- xy[,order(xy[1,])];

    i <- seq(1,length(xysorted[1,]));
    pos <- i[xysorted[3,i] == 1];
    neg <- i[xysorted[3,i] == -1];
    color <- seq(1, length(xysorted[1,]));
    color[pos] <- 'blue';
    color[neg] <- 'red';

    y <- (m*xysorted[1,]) + c;

    return(list(dist=xysorted[2,], x=xysorted[1,], posneg=xysorted[3,], y=y, color=color, l1=l1, l2=l2));

}

gen_data <- function(size, inc, m, c) {
    x <- seq(0, 1, inc/(size-1));
    y <- (m*x) + c;
    #noise <- rnorm(size, mean=0, sd=150);
    noise <- runif(size,-1,1);
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

percep1 <- function(x1, x2, y) {
    x0 <- rep(1, length(x1));
    i <- seq(1, length(x1));
        
    X <- matrix(c(x0, x1, x2), nrow = 3, ncol = length(x1), byrow = TRUE);
    WT <- matrix(rep(1, 3), nrow=1, ncol=3);

    broke <- 0;
            
    iter <- 0;
    limit <- 15000;
    while (iter < limit) {
        H <- sign(WT %*% X);
        fail <- i[H[i] * y[i] < 0];
        
        if (length(fail) < 1) {
            iter <- limit;
        }
        else {
            WT <- WT + y[fail[1]] * t(X[,fail[1]]);
            iter <- iter + 1;
            if (iter == limit) {
                broke <- 1;
            }
        }
    }
    
    a <- -WT[2]/WT[3];
    b <- -WT[1]/WT[3];
    line <- a*X[2,] + b;
                
    return(list(a=a, b=b, line=line, w=WT, broke=broke));    
}

percep <- function(X, WT, y) {
    i <- seq(1, ncol(X));

    fdata <- c();
    rfdata <- c();
    
    broke <- 0;
    
    iter <- 0;
    limit <- 15000;
    repeat {
        H <- sign(WT %*% X);
        fail <- i[H[i] * y[i] < 0];

        fdata <- c(fdata, length(fail));
        rfdata <- c(rfdata, length(fail)/length(y));
        if ((length(fail) < 1) || iter == limit) {
            if(iter == limit) {
                broke <- 1;
            }
            break;
        }
        else {
            WT <- WT + y[fail[1]] * t(X[,fail[1]]);
            iter <- iter + 1;
        }
    }

    a <- -WT[2]/WT[3];
    b <- -WT[1]/WT[3];
    line <- a*X[2,] + b;
    
    return(list(a=a, b=b, line=line, iter=iter, wt=WT, x=X, fdata=fdata, rfdata=rfdata, broke=broke));
}
