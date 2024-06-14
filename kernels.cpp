#include <iostream>
#include <vector>
#include <cmath>
#include <functional>
#include <numeric>
#include <Eigen/Dense>

using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::function;

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

MatrixXd pairwisePersistenceDiagramKernels(const vector<MatrixXd> &X, const vector<MatrixXd> &Y, 
                                         const string &kernel = "sliced_wasserstein", 
                                         double bandwidth = 1.0, int num_directions = 10) {
    int n = X.size();
    int m = Y.size();
    MatrixXd K(n, m);

    if (kernel == "persistence_weighted_gaussian") {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                K(i, j) = persistenceWeightedGaussianKernel(X[i], Y[j], [](VectorXd x) { return 1.0; }, bandwidth);
            }
        }
    } else if (kernel == "persistence_scale_space") {
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                K(i, j) = persistenceScaleSpaceKernel(X[i], Y[j], bandwidth);
            }
        }
    } else {
        // Handle other kernels
    }
    return K;
}

// class SlicedWassersteinKernel {
// public:
//     SlicedWassersteinKernel(int num_directions = 10, double bandwidth = 1.0)
//         : num_directions(num_directions), bandwidth(bandwidth) {}

//     MatrixXd fitTransform(const vector<MatrixXd> &X) {
//         diagrams_ = X;
//         return pairwisePersistenceDiagramKernels(X, X, "sliced_wasserstein", bandwidth, num_directions);
//     }

//     double operator()(const MatrixXd &diag1, const MatrixXd &diag2) {
//         // Implement _sliced_wasserstein_distance
//         return exp(-/*_sliced_wasserstein_distance(diag1, diag2, num_directions)*/ / bandwidth);
//     }

// private:
//     int num_directions;
//     double bandwidth;
//     vector<MatrixXd> diagrams_;
// };

// Define other kernel classes similarly...

int main() {
    // Example usage
    MatrixXd D1(2, 2);
    D1 << 0.0, 1.0,
          2.0, 3.0;

    MatrixXd D2(2, 2);
    D2 << 0.0, 1.0,
          2.0, 3.0;

    vector<MatrixXd> X = {D1, D2};
    // SlicedWassersteinKernel swKernel(10, 1.0);
    double K = persistenceScaleSpaceKernel(D1,D2);
    cout << "Kernel matrix entry:\n" << K << endl;

    return 0;
}
