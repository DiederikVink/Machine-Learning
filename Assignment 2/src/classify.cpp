#include "classify.hpp"
void function(Eigen::MatrixXd &x) {
    Eigen::MatrixXd xtmp;
    xtmp = (x.array()*(x.array()-1)*(x.array()-2)); 
    x = xtmp;
}

void classify(const Eigen::MatrixXd &x1, const Eigen::MatrixXd &x2, Eigen::MatrixXd &y, std::vector<char> &color, Eigen::MatrixXd &line, Eigen::MatrixXd &pline, double distortion) {
    typedef std::chrono::high_resolution_clock seed_clock;
    auto seed_val = seed_clock::now().time_since_epoch().count();
    Eigen::MatrixXd y1tmp(1, x1.cols());
    Eigen::MatrixXd x1func(1, x1.cols());
    double y1tmpval;
    double randval;

    line = x1;
    function(line);

    y1tmp = line.array() - x2.array();

    std::mt19937 gen_eng;
    std::uniform_real_distribution<double> dist(0, 1);
    gen_eng.seed(dist(gen_eng) * seed_val);

    for (size_t i = 0, size = y1tmp.size(); i < size; i++) {
        
        y1tmpval = *(y1tmp.data() + i);
        if (y1tmpval >= 0) {
            y1tmp(0,i) = 1;
            color.push_back('r');
        }
        else {
            y1tmp(0,i) = -1;
            color.push_back('b');
        }
        randval = dist(gen_eng);
        if (randval < distortion) {
            y1tmp(0,i) = y1tmp(0,i) * -1;
        }

        gen_eng.seed(randval * dist(gen_eng) * seed_val);
    }
    y = y1tmp;
}
