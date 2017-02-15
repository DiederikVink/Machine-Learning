#include <iostream>
#include "generate.h"
#include <eigen3/Eigen/Dense>

int main() {
    Eigen::MatrixXd x1;
    Eigen::MatrixXd x2;
    generate_points (x1, x2, 100, 0, 2.5, -1, 2);
    std::cout << "x1:\n" << x1 << std::endl;
    std::cout << "x2:\n" << x2 << std::endl;
}
