#ifndef CLASSIFY_H
#define CLASSIFY_H

#include <eigen3/Eigen/Dense>
#include <iostream>
#include <vector>
#include <chrono>
#include <random>

void classify(const Eigen::MatrixXd &x1, const Eigen::MatrixXd &x2, Eigen::MatrixXd &y, std::vector<char> &color, Eigen::MatrixXd &line, double dist);
void function(Eigen::MatrixXd &x);

#endif
