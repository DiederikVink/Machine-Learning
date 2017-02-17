#include <eigen3/Eigen/Dense>

void create_feature(int degree, const Eigen::MatrixXd &x1, const Eigen::MatrixXd &x2, Eigen::MatrixXd &xfeature, Eigen::MatrixXd &w);
int perceptron(int size, int iterations, const Eigen::MatrixXd &x, const Eigen::MatrixXd &y, Eigen::MatrixXd &w);
void percep_line(const Eigen::MatrixXd &w, const Eigen::MatrixXd &x, Eigen::MatrixXd &line_vals);
double sign(const double &x);
