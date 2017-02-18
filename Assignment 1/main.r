#!/usr/bin/env Rscript
source("q3a.r")
source("q3b.r")
source("q3c.r")

main <- function() {
    print("Starting dav114 Assignment 1 Machine Learning Coursework Code");
    q3a_main();

    #q3b_main(0, 1, "Single Iteration Test Error", "results/Q3/q3b2-testerror.pdf", "results/Q3/q3b2-values.out", "");
    #q3b_main(0, 100, "Average Test Error (Iteration = 100, Gamma = 0)", "results/Q3/q3b3_1-iter100-gamma0-testerror.pdf", "results/Q3/results/Q3/q3b3-iter100-gamma0-values.out", "");
    #q3b_main(0.3, 1, "Average Test Error (Iteration = 1, Gamma = 0.3)", "results/Q3/q3b4_1-iter1-gamma0_3-testerror.pdf", "results/Q3/q3b4-iter1-gamma0.3-values.out", "results/Q3/q3b4_1-iter1-gamma0_3-testerror_full.pdf");
    #q3b_main(0.1, 1, "Average Test Error (Iteration = 1, Gamma = 0.1)", "results/Q3/q3b4_1-iter1-gamma0_1-testerror.pdf", "results/Q3/q3b4-iter1-gamma0.1-values.out", "results/Q3/q3b4_1-iter1-gamma0_1-testerror_full.pdf");
    #q3b_main(0.01, 1, "Average Test Error (Iteration = 1, Gamma = 0.01)", "results/Q3/q3b4_1-iter1-gamma0_01-testerror.pdf", "results/Q3/q3b4-iter1-gamma0.01-values.out", "results/Q3/q3b4_1-iter1-gamma0_01-testerror_full.pdf");
    #q3b_main(0.001, 1, "Average Test Error (Iteration = 1, Gamma = 0.001)", "results/Q3/q3b4_1-iter1-gamma0_001-testerror.pdf", "results/Q3/q3b4-iter1-gamma0.001-values.out", "results/Q3/q3b4_1-iter1-gamma0_001-testerror_full.pdf");
    #q3b_main(0.3, 100, "Average Test Error (Iteration = 100, Gamma = 0.3)", "results/Q3/q3b4_1-iter100-gamma0_3-testerror.pdf", "results/Q3/q3b4-iter100-gamma0.3-values.out", "results/Q3/q3b4_1-iter100-gamma0_3-testerror_full.pdf");
    #q3b_main(0.1, 100, "Average Test Error (Iteration = 100, Gamma = 0.1)", "results/Q3/q3b4_1-iter100-gamma0_1-testerror.pdf", "results/Q3/q3b4-iter100-gamma0.1-values.out", "results/Q3/q3b4_1-iter100-gamma0_1-testerror_full.pdf");
    #q3b_main(0.01, 100, "Average Test Error (Iteration = 100, Gamma = 0.01)", "results/Q3/q3b4_1-iter100-gamma0_01-testerror.pdf", "results/Q3/q3b4-iter100-gamma0.01-values.out", "results/Q3/q3b4_1-iter100-gamma0_01-testerror_full.pdf");
    #q3b_main(0.001, 100, "Average Test Error (Iteration = 100, Gamma = 0.001)", "results/Q3/q3b4_1-iter100-gamma0_001-testerror.pdf", "results/Q3/q3b4-iter100-gamma0.001-values.out", "results/Q3/q3b4_1-iter100-gamma0_001-testerror_full.pdf");
    #
    #q3c_main();
}

main()
