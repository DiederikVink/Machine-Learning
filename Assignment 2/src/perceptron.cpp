#include "perceptron.hpp"
#include <iostream>


// TODO: color vector for graph
// TODO: line vector for graph


void create_feature(double degree, const Eigen::MatrixXd &x1, const Eigen::MatrixXd &x2, Eigen::MatrixXd &xfeature, Eigen::MatrixXd &w) {
    Eigen::MatrixXd xfeat(int(degree), x1.cols());
    Eigen::MatrixXd wtmp(int(degree), 1);
    wtmp = Eigen::MatrixXd::Constant(int(degree), 1, 0.5);

    xfeat.row(0).array() = 1;
    for (int i = 1; i < degree - 1; i++) {
        xfeat.row(i) = x1.array().pow(i);
        //xfeat.row(i) = x1.array().pow(degree - (i - 1));
    }
    xfeat.row(degree - 1).array() = x2.array();

    xfeature = xfeat;
    w = wtmp;
}

double sign(const double &x) {
    if (x >= 0)
        return 1;
    else
        return -1;
}

void percep_line(const Eigen::MatrixXd &w, const Eigen::MatrixXd &x, Eigen::MatrixXd &line_vals) {
    Eigen::MatrixXd tmp_line_vals(1, x.cols());
    tmp_line_vals.row(0).array() = -w(0)/w(w.rows()-1);
    std::cout << "w:\n" << w << std::endl;
    for(int i = 1; i < w.rows()-1; i++){
        tmp_line_vals = tmp_line_vals.array() - (w(i)/w(w.rows()-1) * x.array().pow(i));
    }
    line_vals = tmp_line_vals;
}

double perceptron(double size, double iterations, const Eigen::MatrixXd &x, const Eigen::MatrixXd &y, Eigen::MatrixXd &w) {
    Eigen::MatrixXd H(1, int(size));
    Eigen::MatrixXd fail(1, int(size));
    Eigen::MatrixXd min_w(w.rows(), w.cols());
    Eigen::MatrixXd::Index failRow, failCol;
    double fail_size;
    double min_fail = 2;

    for (int i = 0; i < iterations; i++){
        H = w.transpose() * x;
        H = H.unaryExpr(std::ptr_fun(sign));

        fail = H.array() * y.array();
        fail_size = ((fail.array() < 0).count())/size;

        if (fail_size < min_fail) {
            min_w = w;
            min_fail = fail_size;
        }

        if (fail_size == 0) {
            return(fail_size);
        }

        fail.array().minCoeff(&failRow, &failCol);
        w = w + y(0, failCol) * x.col(failCol);
    }
    w = min_w;
    return(min_fail);
}
