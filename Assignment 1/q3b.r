#!/usr/bin/env Rscript
source("q3a.r")

select_case <- function(x0, line1, line2) {
    y0 <- x0 + 0.1;
    # determine which case the current situation is
    if (x0 <= 0) {case <- 1;}
    else if (((x0 > 0) && (y0 >= 0)) && ((x0 >= 1) || (y0 >= 1))) {case <- 3;}
    else if ((x0 > 0) && (y0 > 0) && (y0 < 1) && (x0 < 1)) {
        if (sign(line1$a) == sign(line2$a)){
            case <- 21;
        }
        else {
            case <- 22;            
        }
    }
    
    if ((case == 1) || (case == 3) || (case == 21)) {
        # look for whether line2 intersection or line1 intersection with the top of the box
        # intersect
        if (line1$top < line2$top) {
            y1 <- line1;
            y2 <- line2;
        }
        else if (line1$top > line2$top) {
            y1 <- line2;
            y2 <- line1;
        }
    }
    else if (case == 22) {
        y1 <- line1;
        y2 <- line2;
    }
    return(list(case=case, y1=y1, y2=y2));
}

part_integral <- function(lim1, lim2, lim3, y) {
    return((.5 * y$a * (lim2^2 - lim1^2)) + ((y$b - 1) * lim2) - (y$b * lim1) + lim3)
}

case1_3_21 <- function(y1, y2, x0, case) {
   if (y1$bot <= 0) {q <- 0;}
   else if ((y1$bot > 0) && (y1$bot < 1)) {q <- y1$bot;}
   else if (y1$bot >= 1) {return(0);}

   if (y1$top <= 0) {r <- 0;}
   else if ((y1$top > 0) && (y1$top < 1)) {r <- y1$top;}
   else if (y1$top >= 1) {r <- 1;}

   if (y2$bot <= 0) {t <- 0;}
   else if ((y2$bot > 0) && (y2$bot < 1)) {t <- y2$bot;}
   else if (y2$bot >= 1) {t <- 1;}

   if (y2$top <= 0) {return(0);}
   else if ((y2$top > 0) && (y2$top < 1)) {s <- y2$top;}
   else if (y2$top >= 1) {s <- 1;}

   return(part_integral(q,r,1,y1)-part_integral(t,s,1,y2));
}

case2 <- function(y1, y2, x0) {
}

get_intersects <- function(a, b, c, d) {
    x0 <- intersect(a, b, c, d);
    line1 <- list(a=a, b=b, bot=intersect(a, b, 0, 0), top=intersect(a, b, 0, 1));
    line2 <- list(a=c, b=d, bot=intersect(c, d, 0, 0), top=intersect(c, d, 0, 1));
    sel <- select_case(x0, line1, line2);
    if ((sel$case == 1) || (sel$case == 3)) {
        case1_3_21(sel$y1, sel$y2, x0, sel$case);
    }
    if (sel$case2a == 21) {
        
    }
}

intersect <- function(a, b, c, d) {
    return((d-b)/(a-c));
}
