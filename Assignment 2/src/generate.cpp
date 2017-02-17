#include "generate.h"
#include <eigen3/Eigen/Dense>
#include <random>
#include <chrono>

void generate_points(Eigen::MatrixXd &x1, Eigen::MatrixXd &x2, const double& size, const double& bottom, const double& top, const double& left, const double& right) {
    generate_random(x1, bottom, top, size);
    //Eigen::MatrixXd tmp(1,(int)size);
    //double incr = (top - bottom)/size;
    //for (int i = 0; i < size; i++) {
    //   tmp(0,i) = (i * incr);
    //}
    //x1 = tmp;
    generate_random(x2, left, right, size);
}

void generate_random(Eigen::MatrixXd &point, const double& a, const double& b, int size) {
    typedef std::chrono::high_resolution_clock seed_clock;
    Eigen::MatrixXd tmp(1,size);
    auto seed_val = seed_clock::now().time_since_epoch().count();

    std::mt19937 gen_eng;
    std::uniform_real_distribution<double> dist(a, b);
    gen_eng.seed(dist(gen_eng) * seed_val);
    for (int i = 0; i < size; i++) {
        tmp(0, i) = dist(gen_eng);
        gen_eng.seed(tmp(0,i) * dist(gen_eng) * seed_val);
    }

    point = tmp;

}
