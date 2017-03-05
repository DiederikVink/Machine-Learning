#include "generate.hpp"
#include <eigen3/Eigen/Dense>
#include <random>
#include <iostream>
#include <chrono>

typedef std::chrono::high_resolution_clock seed_clock;

bool function(const double& x1, const double& x2) {
    return(x2 > x1*(x1 - 1)*(x1 - 2));
}

void generate_points(Eigen::MatrixXd &x1, Eigen::MatrixXd &x2, Eigen::MatrixXd &y, const double& size, const double& bottom, const double& top, const double& left, const double& right, const double& distortion, std::vector<char>& color) {

    Eigen::MatrixXd x1tmp(1, (int)size);
    Eigen::MatrixXd x2tmp(1, (int)size);
    Eigen::MatrixXd ytmp(1, (int)size);
    Eigen::MatrixXd line;

    std::mt19937 gen_eng;
    std::uniform_real_distribution<double> x1dist(bottom, top);
    std::uniform_real_distribution<double> x2dist(left, right);
    std::uniform_real_distribution<double> ydist(0, 1);

    double randval;
    auto seed_val = seed_clock::now().time_since_epoch().count(); 
    gen_eng.seed(x1dist(gen_eng) * x2dist(gen_eng) * seed_val);

    for(int i = 0; i < size; i++) {
        x1tmp(0, i) = x1dist(gen_eng);
        gen_eng.seed(x1dist(gen_eng) * seed_val);
        x2tmp(0, i)  = x2dist(gen_eng);
        gen_eng.seed(x2dist(gen_eng) * seed_val);

        if(function(x1tmp(0, i), x2tmp(0, i))) {
            ytmp(0, i) = 1;
            color.push_back('b');
        }
        else {
            ytmp(0, i) = -1; 
            color.push_back('r');
        }
        randval = ydist(gen_eng);
        if(randval < distortion)  {
            ytmp(0, i) = ytmp(0, i) * -1;
            if(color[i] == 'b') {
                color[i] = 'r';
            }
            else {
                color[i] = 'b';
            }
        }

        gen_eng.seed(ydist(gen_eng) * seed_val);
    }

    x1 = x1tmp;
    x2 = x2tmp;
    y = ytmp;
}

//void generate_random(Eigen::MatrixXd &point, const double& a, const double& b, int size) {
//    typedef std::chrono::high_resolution_clock seed_clock;
//    Eigen::MatrixXd tmp(1,size);
//    auto seed_val = seed_clock::now().time_since_epoch().count();
//
//    std::mt19937 gen_eng;
//    std::uniform_real_distribution<double> dist(a, b);
//    gen_eng.seed(dist(gen_eng) * seed_val);
//
//    for (int i = 0; i < size; i++) {
//        tmp(0, i) = dist(gen_eng);
//        gen_eng.seed(tmp(0,i) * dist(gen_eng) * seed_val);
//    }
//
//    point = tmp;
//
//}
