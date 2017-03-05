#ifndef GENERATE_H
#define GENERATE_H

#include <vector>
#include <eigen3/Eigen/Dense>

bool function(const double& x1, const double& x2);
void generate_points(Eigen::MatrixXd &x1, Eigen::MatrixXd &x2, Eigen::MatrixXd &y, const double& size, const double& bottom, const double& top, const double& left, const double& right, const double& distortion, std::vector<char>& color);

#endif
