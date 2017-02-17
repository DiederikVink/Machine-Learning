#include "rm.hpp"

double RM(int dvc, int n, double w, double delta) {
    double b1 = (8 * dvc)/n;
    double b2 = log(2*n + 1);
    double b3 = 8/n;
    double b4 = 8/(w*delta);
    double b5 = log(b4);
    double b6 = sqrt(b1 * b2 + b3 * b5);
    double b7 = 1/(2*n);
    double b8 = 4/(w*delta);
    double b9 = b7 * log(b8);
    return(sqrt(b9));
}

