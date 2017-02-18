#ifndef TEST_ERROR_H
#define TEST_ERROR_H

#include <eigen3/Eigen/Dense>
#include "generate.hpp"
#include "perceptron.hpp"
#include <iostream>

double test(double size, const Eigen::MatrixXd &x, const Eigen::MatrixXd &w, const Eigen::MatrixXd &y);
double test_error(const double& size, const double& degree, const double& dist, const Eigen::MatrixXd &w);

#endif
