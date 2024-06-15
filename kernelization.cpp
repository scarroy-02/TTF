#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <cmath>
#include <functional>
#include <numeric>
#include <Eigen/Dense>
#include <chrono>
// #include "cnpy.h"
// #include "H5Cpp.h"


using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::function;
// using H5::H5File;
// using H5::DataSet;
// using H5::DataSpace;
// using H5::PredType;

double gaussianKernel(double x, double bandwidth) {
    return exp(-x * x / (2 * bandwidth * bandwidth)) / (sqrt(2 * M_PI) * bandwidth);
}

double persistenceWeightedGaussianKernel(const MatrixXd &D1, const MatrixXd &D2, 
                                         function<double(VectorXd)> weight = [](VectorXd x) { return 1.0; }, 
                                         double bandwidth = 1.0) {
    int n = D1.rows();
    int m = D2.rows();
    VectorXd ws1(n), ws2(m);
    for (int i = 0; i < n; ++i) ws1(i) = weight(D1.row(i));
    for (int i = 0; i < m; ++i) ws2(i) = weight(D2.row(i));

    double result = 0.0;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            result += ws1(i) * ws2(j) * gaussianKernel((D1.row(i) - D2.row(j)).norm(), bandwidth);
        }
    }
    return result;
}

double persistenceScaleSpaceKernel(const MatrixXd &D1, const MatrixXd &D2, double bandwidth = 1.0) {
    int n = D1.rows();
    MatrixXd DD1(2 * n, 2);
    DD1 << D1, D1.rowwise().reverse();

    int m = D2.rows();
    MatrixXd DD2(2 * m, 2);
    DD2 << D2, D2.rowwise().reverse();

    auto weight_pss = [](VectorXd x) { return x(1) >= x(0) ? 1.0 : -1.0; };
    return 0.5 * persistenceWeightedGaussianKernel(DD1, DD2, weight_pss, bandwidth);
}

MatrixXd pairwisePersistenceDiagramKernels(const vector<MatrixXd> &X, 
                                         const string &kernel = "persistence_scale_space", 
                                         double bandwidth = 1.0) {
    int n = X.size();
    MatrixXd K(n, n);

    if (kernel == "persistence_weighted_gaussian") {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                K(i, j) = persistenceWeightedGaussianKernel(X[i], X[j], [](VectorXd x) { return 1.0; }, bandwidth);
            }
        }
    } else if (kernel == "persistence_scale_space") {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                K(i, j) = persistenceScaleSpaceKernel(X[i], X[j], bandwidth);
            }
        }
    }
    return K;
}

// vector<MatrixXd> readPersistentDiagramsNpy(const string &filename) {
//     cnpy::NpyArray arr = cnpy::npy_load(filename);
//     double* data = arr.data<double>();
//     vector<MatrixXd> diagrams;

//     for (int i = 0; i < arr.shape[0]; ++i) {
//         MatrixXd diagram(arr.shape[1], arr.shape[2]);
//         for (int j = 0; j < arr.shape[1]; ++j) {
//             for (int k = 0; k < arr.shape[2]; ++k) {
//                 diagram(j, k) = data[i * arr.shape[1] * arr.shape[2] + j * arr.shape[2] + k];
//             }
//         }
//         diagrams.push_back(diagram);
//     }

//     return diagrams;
// }

vector<MatrixXd> readPersistentDiagrams(const string &filename) {
    vector<MatrixXd> diagrams;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Unable to open file" << endl;
        return diagrams;
    }

    string line;
    while (getline(file, line)) {
        vector<VectorXd> diagram;
        do {
            if (line.empty()) break;
            stringstream ss(line);
            VectorXd point(2);
            ss >> point(0) >> point(1);
            diagram.push_back(point);
        } while (getline(file, line) && !line.empty());

        int n = diagram.size();
        MatrixXd mat(n, 2);
        for (int i = 0; i < n; ++i) {
            mat.row(i) = diagram[i];
        }
        diagrams.push_back(mat);
    }

    return diagrams;
}

// vector<MatrixXd> readPersistentDiagramsHdf5(const string &filename) {
//     vector<MatrixXd> diagrams;
//     H5File file(filename, H5F_ACC_RDONLY);

//     for (int i = 0;; ++i) {
//         try {
//             string dataset_name = "diagram_" + to_string(i);
//             DataSet dataset = file.openDataSet(dataset_name);
//             DataSpace dataspace = dataset.getSpace();

//             hsize_t dims[2];
//             dataspace.getSimpleExtentDims(dims, NULL);

//             MatrixXd diagram(dims[0], dims[1]);
//             dataset.read(diagram.data(), PredType::NATIVE_DOUBLE);

//             diagrams.push_back(diagram);
//         } catch (H5::Exception &e) {
//             break;
//         }
//     }

//     return diagrams;
// }

int main() {
    // Example usage
    string filename = "persistent_diagrams.txt"; // Replace with your file name

    // Get the start time
    auto start = std::chrono::high_resolution_clock::now();

    vector<MatrixXd> diagrams = readPersistentDiagrams(filename);
    cout << "Reading complete" << endl;

    // Get the end time
    auto end = std::chrono::high_resolution_clock::now();

    // Calculate the duration
    std::chrono::duration<double> duration = end - start;

    // Display the duration
    std::cout << "Time taken: " << duration.count() << " seconds" << std::endl;

    // Get the start time
    auto start1 = std::chrono::high_resolution_clock::now();

    MatrixXd K = pairwisePersistenceDiagramKernels(diagrams, "persistence_scale_space");
    cout << "Kernelization complete" << endl;

    // Save the kernel matrix to a file
    ofstream file("kernel_matrix.csv");
    if (file.is_open()) {
        file << K.format(Eigen::IOFormat(Eigen::StreamPrecision, Eigen::DontAlignCols, ", ", "\n"));
        file.close();
    } else {
        cerr << "Unable to open file for writing" << endl;
    }

    // Get the end time
    auto end1 = std::chrono::high_resolution_clock::now();

    // Calculate the duration
    std::chrono::duration<double> duration1 = end1 - start1;

    // Display the duration
    std::cout << "Time taken: " << duration1.count() << " seconds" << std::endl;

    // // Save the kernel matrix to a binary file
    // cnpy::npy_save("kernel_matrix.npy", K.data(), {(size_t)K.rows(), (size_t)K.cols()}, "w");

    return 0;
}