#include <iostream>
#include "generate.h"
#include "json.hpp"
#include <eigen3/Eigen/Dense>
#include <vector>
#include <fstream>

using json = nlohmann::json;

void print(json &graph_data, const std::vector<double> &out1, const std::vector<double> &out2, std::string title, std::string xlabel, std::string ylabel, std::string legend) {
    graph_data = {
        {"title", "title_here"},
        {"legend", "legend_here"},
        {"xlabel", "xlabel_here"},
        {"ylabel", "ylabel_here"},
        {"x", out1},
        {"y", out2}
    };
}

void create_json(json &graph_data, const std::vector<double> &out1, const std::vector<double> &out2, std::string title, std::string xlabel, std::string ylabel, std::string legend, std::string filename) {
    print(graph_data, out1, out2, title, xlabel, ylabel, legend);
    std::ofstream out_file;
    out_file.open(filename);
    out_file << graph_data;
    out_file.close();
}

int main() {
    Eigen::MatrixXd x1;
    Eigen::MatrixXd x2;
    std::vector<double> out1;
    std::vector<double> out2;
    generate_points (x1, x2, 100, 0, 2.5, -1, 2);
    out1.assign(x1.data(), x1.data()+x1.size());
    out2.assign(x2.data(), x2.data()+x2.size());
    json graph_data;
    create_json(graph_data, out1, out2, "title", "xlab", "ylab", "legend", "files/graphs.json");
    return 0;
}

