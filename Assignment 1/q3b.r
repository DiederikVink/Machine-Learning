#!/usr/bin/env Rscript
source("q3a.r")

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

    if ((case == 1) || (case == 21)) {
        # look for whether line2 intersection or line1 intersection with the top of the box
        # intersect
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

line_integral <- function(lim1, lim2, lim3, y) {
    return((.5 * y$a * (lim2^2 - lim1^2)) + ((y$b - 1) * lim2) - (y$b * lim1) + lim3)
}

case <- function(y1, y2, x0, case, gamma, pos, fixed) {
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
    x0 <- intersect(a, b, c, d);
    line1 <- list(a=a, b=b, bot=intersect(a, b, 0, 0), top=intersect(a, b, 0, 1));
    line2 <- list(a=c, b=d, bot=intersect(c, d, 0, 0), top=intersect(c, d, 0, 1));
    sel <- select_case(x0, line1, line2, a, b);
    res <- case(sel$y1, sel$y2, x0, sel$case, gamma, pos, sel$fixed);
    return(res);
}

non_hoeffdings <- function(error) {
    return(t(apply(error, 1, sort)));
}

hoeffdings <- function(error) {
    log(0.05)/2*n
}

error_epsilon <- function(i, j, vars) {
    coeff <- perceptron(incr*i, inc, a, b);
    vars$error[i,j] <- areas(a, b, coeff$a, coeff$b);
    vars$epsilon[i] <- sqrt(-log(0.05)/(2*incr*i));
    return(list(error=error, epsilon=epsilon));
}

intersect <- function(a, b, c, d) {
    return((d-b)/(a-c));
}
