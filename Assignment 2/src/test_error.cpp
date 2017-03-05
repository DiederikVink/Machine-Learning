#include "test_error.hpp"
#include <vector>

double test(double size, const Eigen::MatrixXd &x, const Eigen::MatrixXd &w, const Eigen::MatrixXd &y) {
    Eigen::MatrixXd H =  w.transpose() * x;
    H = H.unaryExpr(std::ptr_fun(sign));
    Eigen::MatrixXd fail(H.rows(), 1);
    
    for(int i = 0; i < H.rows(); i++) {
        fail(i,0) = ((H.row(i).array() * y.array()) < 0).count() / size;
    } 
    double val = fail.col(0).sum() / fail.rows();
    return(val);
}

double test_error(const double& size, const double& degree, const double& dist, const Eigen::MatrixXd &w) { 
    Eigen::MatrixXd x1;
    Eigen::MatrixXd x2;
    Eigen::MatrixXd xfeature;
    Eigen::MatrixXd y;
    Eigen::MatrixXd line;
    Eigen::MatrixXd dummy;
    std::vector<char> color;
    generate_points(x1, x2, y, size, 0, 2.5, -1, 2, dist, color);
    create_feature(degree, x1, x2, xfeature, dummy);
    return(test(size, xfeature, w, y));
 }
