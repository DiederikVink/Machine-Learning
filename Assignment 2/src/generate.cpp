#include "generate.h"
#include <eigen3/Eigen/Dense>
#include <iostream>

void generate_points(Eigen::MatrixXd &x1, Eigen::MatrixXd &x2, const double& size, const double& bottom, const double& top, const double& left, const double& right) {
   generate_random(x1, bottom, top, size);
   generate_random(x2, left, right, size);
}

void generate_random(Eigen::MatrixXd &point, const double& a, const double& b, int size) {
    double scale_factor = (b - a)/2;
    double shift_factor = scale_factor + a; 
    Eigen::MatrixXd shift_vec = Eigen::MatrixXd::Constant(1, size, shift_factor);
    std::srand((unsigned int) time(0));
    point = (scale_factor * Eigen::MatrixXd::Random(1, size)) + shift_vec;
}
