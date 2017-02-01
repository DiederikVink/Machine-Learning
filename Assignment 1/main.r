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
    coeff <- perceptron(100,inc,a,b); #q3a
    #get_intersects(a, b, coeff$a, coeff$b);
    get_intersects(a, b, 2, 0.5);
    

}

main()
