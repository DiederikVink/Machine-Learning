#!/usr/bin/env Rscript
source("q3a.r")
source("q3b.r")

main <- function() {

    q3a_main();
    q3b_main(0);
    q3b_main(0.3);
    q3b_main(0.1);
    q3b_main(0.01);
    q3b_main(0.001);
}

main()
