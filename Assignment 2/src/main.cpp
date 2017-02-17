#include <iostream>
#include "generate.h"
#include "classify.hpp"
#include "rm.hpp"
#include "perceptron.hpp"
#include "json.hpp"
#include <eigen3/Eigen/Dense>
#include <chrono>
#include <vector>
#include <fstream>

using json = nlohmann::json;

void print(json &graph_data, const std::vector<double> &out1, const std::vector<double> &out2, std::vector<double> &line, std::vector<double> &pline, std::vector<char> &color, std::string title, std::string xlabel, std::string ylabel, std::string legend) {
    graph_data = {
        {"title", "title_here"},
        {"legend", "legend_here"},
        {"xlabel", "xlabel_here"},
        {"ylabel", "ylabel_here"},
        {"x", out1},
        {"y", out2},
        {"col", color},
        {"line", line},
        {"pline", pline}
    };
}

void create_json(json &graph_data, const std::vector<double> &out1, const std::vector<double> &out2, std::vector<double> &line, std::vector<double> &pline, std::vector<char> &color, std::string title, std::string xlabel, std::string ylabel, std::string legend, std::string filename) {
    print(graph_data, out1, out2, line, pline, color, title, xlabel, ylabel, legend);
    std::ofstream out_file;
    out_file.open(filename);
    out_file << graph_data;
    out_file.close();
}

int main() {
    //TODO: change functional and file decomposition
    int degree = 4;
    int repeats = 100;
    int size = 1000;
    int iterations = 1000;
    int fail_size;
    int q_min;
    double fail_avg;
    double dist = 0.1;
    double SRM;
    double SRM_min = 20000000000000;
    double ERM;
    double ERM_min = 20000000000000;
    Eigen::MatrixXd x1;
    Eigen::MatrixXd x2;
    Eigen::MatrixXd xfeature;
    Eigen::MatrixXd y;
    Eigen::MatrixXd w;
    Eigen::MatrixXd srm_w_min(degree+2,1);
    Eigen::MatrixXd erm_w_min(degree+2,1);
    Eigen::MatrixXd w_avg(degree+2,1);
    Eigen::MatrixXd H;
    Eigen::MatrixXd line;
    Eigen::MatrixXd pline;
    std::vector<double> out1;
    std::vector<double> out2;
    std::vector<double> outline;
    std::vector<double> outpline;
    std::vector<double> q_w_avg;
    std::vector<double> q_fail_avg;
    std::vector<char> color;
    typedef std::chrono::high_resolution_clock timer;

    auto start = timer::now();

    for (int q = 0; q <= degree; q++) {
        Eigen::MatrixXd w_sum(q+2,1);
        fail_size = 0;

        for (int i  = 0; i < repeats; i++) {
            generate_points (x1, x2, size, 0, 2.5, -1, 2);
            classify(x1, x2, y, color, line, pline, dist);
            create_feature(q + 2, x1, x2, xfeature, w);
            fail_size += perceptron(size, iterations, xfeature, y, w);
            w_sum =  w_sum + w;
            //std::cout << i << " " << std::endl;
        }
        
        w_avg = w_sum / repeats;    
        std::cout << "fs: " << fail_size << std::endl;
        fail_avg = fail_size / repeats;

        SRM = fail_avg + RM(q+2, size, 0.2, 0.1);
        ERM = fail_avg + RM(q+2, size, 1, 0.1);
        std::cout << "fa: " << fail_avg << std::endl;
        std::cout << RM(q+2, size, 0.2, 0.1);
        std::cout << "SRM: " << SRM << std::endl;
        std::cout << "SRM_min: " << SRM_min << std::endl;

        if (SRM_min > SRM) {
            srm_w_min = w_avg;
            SRM_min = SRM;
        }

        if (ERM_min > ERM) {
            erm_w_min = w_avg;
            ERM_min = ERM;
        }

        //q_w_avg.push_back(w_avg/repeats);
        //q_fail_avg.push_back(fail_size/repeats);
    }

    auto finish = timer::now();
    std::cout << (double)std::chrono::duration_cast<std::chrono::nanoseconds>(finish - start).count()/1000000000<< std::endl;
    std::cout << (double)fail_avg << std::endl;

    percep_line(srm_w_min, x1, pline);

    out1.assign(x1.data(), x1.data()+x1.size());
    out2.assign(x2.data(), x2.data()+x2.size());
    outline.assign(line.data(), line.data()+line.size());
    outpline.assign(pline.data(), pline.data()+pline.size());
    json graph_data;
    create_json(graph_data, out1, out2, outline, outpline, color, "title", "xlab", "ylab", "legend", "files/graphs.json");
    return 0;
}

