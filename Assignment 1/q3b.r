#!/usr/bin/env Rscript
source("q3a.r")

q3b_main <- function(gamma) {
    inc <- 1;

    # genearte the variables for the fixed line x2 = x1 + 0.1
    a <- 1;
    b <- 0.1;

    # run the perceptron algorithm 100 times
    iter <- 100;
    incr <- 100;
    # set up matrices and vectors used for iteration and data collection
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
                # call the perceptron algorithm
                coeff <- perceptron(incr*i, inc, a, b, gamma);
                # record the amount of iterations needed to find w_*
                updates[i,j] <- coeff$iter;
                # record the values of t, rho, and w produced the perceptron algorithm
                t[i,j] <- coeff$t;
                rho[i,j] <- coeff$rho;
                w[i*j,] <- coeff$w;
                # calculate the test error
                error[i,j] <- areas(a, b, coeff$a, coeff$b, gamma, 0);
                # calculate epsilon for a confidence interval of 90%
                epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
                # record the amount of times the iteration limit was reached
                broke <- broke + coeff$broke;
            }
        }
        total_time <- proc.time() - timer;
    }
    else {
        error1 <- matrix( , nrow = length(x), ncol = iter);
        error2 <- matrix( , nrow = length(x), ncol = iter);
        timer <- proc.time();
        # runs just like when gamma == 0, with one difference
        for(i in x) {
            for (j in 1:iter) {
                coeff <- perceptron(incr*i, inc, a, b, gamma);
                updates[i,j] <- coeff$iter;
                t[i,j] <- coeff$t;
                rho[i,j] <- coeff$rho;
                w[i*j,] <- coeff$w;
                # we have two error values, one for the line offset by +gamma, and one 
                # for the line offset by -gamma
                error1[i,j] <- areas(a, b + gamma, coeff$a, coeff$b, gamma, 1);
                error2[i,j] <- areas(a, b - gamma, coeff$a, coeff$b, gamma, -1);
                epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
                broke <- broke + coeff$broke;
            }
        }
        total_time <- proc.time() - timer;
        error <- error1 + error2;
    }

    # calculate two viable w_* values for rho of each dataset size 
    w_star <- matrix(,nrow=1,ncol=3);
    j <- seq(1,iter);
    for(i in x) {
        pos <- j[rho[i,j]>0];
        w_star <- rbind(w_star, head(w[pos*i,],2));
    }

    w_star <- w_star[-1,];
    print("wstar");
    print(w_star);

    # sort the error values in ascending order, to get empirical confidence intervals
    non_hoeff <- non_hoeffdings(error);
    # get mean values for each dataset size
    error_mean <- rowMeans(error);
    update_mean <- rowMeans(updates);
    t_mean <- rowMeans(t);

    # calculate the heoffding values for hte 90% confidence intervals
    hoeff_5 <- error_mean - epsilon;
    hoeff_95 <- error_mean + epsilon;

    #set up and plot the graphs
    if (gamma == 0) {
        maximum <- max(hoeff_95)+0.075;
        minimum <- min(hoeff_5)-0.001;
    }
    else {
        maximum <- max(non_hoeff[,95])+0.01;
        minimum <- min(non_hoeff[,5])-0.001;
    }
    print(total_time);
    print(broke);
    plot(x*incr, seq(minimum,maximum-0.0000001,(maximum-minimum)/(500/incr)), type='n', xlab = "sample size", ylab = "Error probability");
    lines(x*incr, error_mean, type = 'p');
    lines(lowess(x*incr, error_mean));
    lines(x*incr, non_hoeff[,5], col="blue", type = 'p');
    lines(lowess(x*incr, non_hoeff[,5]), col="blue");
    lines(x*incr, non_hoeff[,95], col="red", type = 'p');
    lines(lowess(x*incr, non_hoeff[,95]), col = "red");
    if (gamma == 0) {
        lines(x*incr, hoeff_5, col="green", type = 'p');
        lines(lowess(x*incr, hoeff_5), col = "green");
        lines(x*incr, hoeff_95, col="orange", type = 'p');
        lines(lowess(x*incr, hoeff_95), col = "orange");
    }
}

select_case <- function(x0, line1, line2, a, b) {
    y0 <- (a*x0) + b;
    # determine which case the current situation is
    if ((x0 <= 0) || (y0 <= 0)) {case <- 1;}
    else if (((x0 > 0) && (y0 >= 0)) && ((x0 >= 1) || (y0 >= 1))) {case <- 3;}
    else if ((x0 > 0) && (y0 > 0) && (y0 < 1) && (x0 < 1)) {
        if (sign(line1$a) == sign(line2$a)){
            case <- 21;
        }
        else {
            case <- 22;            
        }
    }

    # look for whether line2 intersection or line1 intersection with the top of the box
    # intersect, to determine which line is y1 and which is y2 (more details about y1 and
    # y2 in the report)
    if ((case == 1) || (case == 21)) {
        if (line1$top < line2$top) {
            y1 <- line1;
            y2 <- line2;
            fixed <- 1;
        }
        else if (line1$top > line2$top) {
            y1 <- line2;
            y2 <- line1;
            fixed <- 2;
        }
    }
    else if (case == 3) {
        if (line1$bot < line2$bot) {
            y1 <- line1;
            y2 <- line2;
            fixed <- 1;
        }
        else if (line1$bot > line2$bot) {
            y1 <- line2;
            y2 <- line1;
            fixed <- 2;
        }
    }
    else if (case == 22) {
        y1 <- line1;
        y2 <- line2;
        fixed <- 1;
    }
    return(list(case=case, y1=y1, y2=y2, fixed=fixed));
}

# calculation of the result of the integrals needed for the error calculation
line_integral <- function(lim1, lim2, lim3, y) {
    return((.5 * y$a * (lim2^2 - lim1^2)) + ((y$b - 1) * lim2) - (y$b * lim1) + lim3)
}

case <- function(y1, y2, x0, case, gamma, pos, fixed) {
    # set the bounds for the integration to calculate the error
    if (y1$bot <= 0) {q <- 0;}
    else if ((y1$bot > 0) && (y1$bot < 1)) {q <- y1$bot;}
    else if (y1$bot >= 1) {return(0);}
    
    if (y1$top <= 0) {r <- 0;}
    else if ((y1$top > 0) && (y1$top < 1)) {r <- y1$top;}
    else if (y1$top >= 1) {r <- 1;}
    
    if (y2$bot <= 0) {t <- 0;}
    else if ((y2$bot > 0) && (y2$bot < 1)) {t <- y2$bot;}
    else if (y2$bot >= 1) {t <- 1;}
    
    if (y2$top <= 0) {
        if(case == 22) {s <- 0;}
        else if (case == 21) {return(0);}
    }
    else if ((y2$top > 0) && (y2$top < 1)) {s <- y2$top;}
    else if (y2$top >= 1) {s <- 1;}

    # depending on which case the perceptron alogrithm line falls under, perform the correct
    # version of the algorithm to find the error
    if ((case == 1) || (case == 3)) {
        inte <- line_integral(q,r,1,y1) - line_integral(t,s,1,y2);
        if (gamma == 0) {
            return(inte);
        }
        else {
            if (pos == 1) {
                if (fixed == 2) {
                    return(inte);
                }
                else {
                    return(0);
                }
            }
            else if (pos == -1) {
                if (fixed == 1) {
                    return(inte);
                }
                else {
                    return(0);
                }
            }
        }
    }
    else if (case == 21) {
        i1 <- line_integral(t, x0, x0, y2) - line_integral(q, x0, x0, y1);
        i2 <- line_integral(x0, r, 1, y1) - line_integral(x0, s, 1, y2);
        if (gamma  == 0) {
            return(i1 + i2);
        }
        else {
            if (pos == 1) {
                if (fixed == 2) {
                    return(i2);
                }
                else if (fixed == 1) {
                    return(i1);
                }
            }
            else if (pos == -1) {
                if (fixed == 2) {
                    return(i1);
                }
                else if (fixed == 1) {
                    return(i2);
                }
            }
        }
    }
    else if (case == 22) {
        if (gamma == 0) {
            y1_ <- y1;
            y1_$a <- -y1$a;
            y1_$b <- y1$a + y1$b;

            y2_ <- y2;
            y2_$a <- -y2$a;
            y2_$b <- y2$a + y2$b;
            
            i1 <- line_integral(q, x0, x0, y1) + line_integral(x0, t, t, y2);
            i2 <- line_integral(1-r, 1-x0, 1-x0, y2_) + line_integral(1-x0, 1-s, 1-s, y1_);

            return(1-i1-(-i2));
        }
        else {
            return(0);
        }
    }
}

areas <- function(a, b, c, d, gamma, pos) {
    # find the intersection point between the lines
    x0 <- intersect(a, b, c, d);
    # define the two lines that are to be considered
    line1 <- list(a=a, b=b, bot=intersect(a, b, 0, 0), top=intersect(a, b, 0, 1));
    line2 <- list(a=c, b=d, bot=intersect(c, d, 0, 0), top=intersect(c, d, 0, 1));
    # determine what case the perceptron generated algorithm falls under
    sel <- select_case(x0, line1, line2, a, b);
    # calculate the error value 
    res <- case(sel$y1, sel$y2, x0, sel$case, gamma, pos, sel$fixed);
    return(res);
}

non_hoeffdings <- function(error) {
    return(t(apply(error, 1, sort)));
}

error_epsilon <- function(i, j, vars) {
    coeff <- perceptron(incr*i, inc, a, b);
    vars$error[i,j] <- areas(a, b, coeff$a, coeff$b);
    vars$epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
    return(list(error=error, epsilon=epsilon));
}

#calculate the intersection between two lines
intersect <- function(a, b, c, d) {
    return((d-b)/(a-c));
}
