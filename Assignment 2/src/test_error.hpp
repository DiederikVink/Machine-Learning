#ifndef TEST_ERROR_H
#define TEST_ERROR_H

#include <eigen3/Eigen/Dense>
#include "generate.h"
#include "classify.hpp"
#include "perceptron.hpp"

double test(double size, const Eigen::MatrixXd &x, const Eigen::MatrixXd &w, const Eigen::MatrixXd &y);
double test_error(double size, double degree, const Eigen::MatrixXd &w);

#endif
