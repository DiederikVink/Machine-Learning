#include <iostream>
#include "generate.hpp"
#include "classify.hpp"
#include "rm.hpp"
#include "perceptron.hpp"
#include "test_error.hpp"
#include "json.hpp"
#include <eigen3/Eigen/Dense>
#include <chrono>
#include <cmath>
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
    double degree = 4;
    double degree_out;
    double repeats = 1;
    double size = 10000;
    double iterations = 1000;
    double fail_size;
    double fail_tmp;
    double fail_min = 1000000000000;
    int i_min;
    double q_min;
    double fail_avg;
    double dist = 0.1;
    double SRM;
    double SRM_min = 10;
    double delta;
    Eigen::MatrixXd x1;
    Eigen::MatrixXd x2;
    Eigen::MatrixXd xfeature;
    Eigen::MatrixXd y;
    Eigen::MatrixXd w;
    Eigen::MatrixXd g_vec;
    Eigen::MatrixXd srm_w_min;
    Eigen::MatrixXd erm_total;
    Eigen::MatrixXd H;
    Eigen::MatrixXd line;
    Eigen::MatrixXd pline;
    std::vector<double> out1;
    std::vector<double> out2;
    std::vector<double> outline;
    std::vector<double> outpline;
    std::vector<double> q_w_avg;
    std::vector<double> q_fail_avg;
    std::vector<double> weight;
    std::vector<char> color;
    typedef std::chrono::high_resolution_clock timer;

    auto start = timer::now();

    std::cout << "Setup" << std::endl;
    std::cout << "Sample size (n): " << size << std::endl;
    std::cout << "Perceptron iteration limit: " << iterations << std::endl;
    std::cout << "Overall repetitions (to acquire set for an average): " << repeats << std::endl;

    //weight.push_back(0.03);
    //weight.push_back(0.07);
    //weight.push_back(0.1);
    //weight.push_back(0.3);
    //weight.push_back(0.5);
    weight.push_back(0.2);
    weight.push_back(0.2);
    weight.push_back(0.2);
    weight.push_back(0.2);
    weight.push_back(0.2);

    for (int q = degree-1; q >= 3; q--) {
        Eigen::MatrixXd g(q+2, int(repeats));
        fail_size = 0;

        std::cout << "----------------Q = " << q << "----------------" << std::endl;

        for (int i  = 0; i < repeats; i++) {
            generate_points (x1, x2, y, size, 0, 2.5, -1, 2, dist, color);
            create_feature(q + 2, x1, x2, xfeature, w);
            fail_tmp = perceptron(size, iterations, xfeature, y, w);
            fail_size += fail_tmp;
            if (fail_tmp < fail_min) {
                fail_min = fail_tmp;
                i_min = i;
            }
            g.col(i) = w;
        }
        
        fail_avg = fail_size / repeats;

        //weight = std::abs(1.1 - double(q)/3.0);
        delta = 0.1/weight[q];
        std::cout << "weight: " << weight[q] << std::endl;

        SRM = fail_avg + (1 * RM(q+2, size, weight[q], delta));

        std::cout << "SRM: " << SRM << std::endl;
        std::cout << "Complexity Term: " << RM(q+2, size, weight[q], delta) << std::endl;
        std::cout << "Training Error: " << fail_avg << std::endl;
        std::cout << "g: " << g << std::endl;

        //std::cout << "ERM Test Error (" << q << "): " << test_error(1000000, q+2, dist, g) << std::endl;

        if (SRM_min > SRM) {
            degree_out = q;
            srm_w_min = g;
            SRM_min = SRM;
        }
    }

    std::cout << "----------------Final Results----------------" << std::endl;
    std::cout << "Training Error: " << fail_min << std::endl;
    std::cout << "SRM bound: " << SRM_min << std::endl;
    std::cout << "SRM polynomial degree: " << degree_out << std::endl;
    std::cout << "Final SRM (g): " << srm_w_min << std::endl;
    //double terror = test_error(1000000, degree_out + 2, dist, srm_w_min);
    //std::cout << "Test Error: " << terror << std::endl;
    
    auto finish = timer::now();
    std::cout << "Run Time: " << (double)std::chrono::duration_cast<std::chrono::nanoseconds>(finish - start).count()/1000000000<< std::endl;

    percep_line(srm_w_min.col(i_min), x1, pline);
    Eigen::MatrixXd org_w(5,1);
    org_w << 0, -2, 3, -1, 1;
    std::cout << "orgw: " << org_w << std::endl;
    percep_line(org_w, x1, line);


    out1.assign(x1.data(), x1.data()+x1.size());
    out2.assign(x2.data(), x2.data()+x2.size());
    outline.assign(line.data(), line.data()+line.size());
    outpline.assign(pline.data(), pline.data()+pline.size());
    json graph_data;
    create_json(graph_data, out1, out2, outline, outpline, color, "title", "xlab", "ylab", "legend", "files/graphs.json");
    return 0;
}

