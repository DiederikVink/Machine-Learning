#ifndef GENERATE_H
#define GENERATE_H

#include <eigen3/Eigen/Dense>

void generate_points(Eigen::MatrixXd &x1, Eigen::MatrixXd &x2, const double& size, const double& bot, const double& top, const double& left, const double& right);
void generate_random(Eigen::MatrixXd &point, const double& a, const double& b, int size);

#endif
