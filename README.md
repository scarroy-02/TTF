# TTF Repository

Tried SVM on 3 classes of graphs with 303 total graphs. Was giving accuracy 1.0 when having 2 completely random graphs as classes.

So, made 2 classes with slight changes.

* PersistenceScaleSpaceKernel : 0.91
* PersistenceFisherKernel : 0.26
* PersistenceWeightedGaussianKernel : 0.91
* SlicedWassersteinKernel : 0.68

With big change, even persistence fisher gives 1.0 accuracy.

Now tried standardising the kernel matrix. This gives very poor accuracy with SVM as well as Logistic Regression models with precomputed kernels. The accuracy is 0.1 for both cases. Will have to fix this, or maybe use the non-standardised kernel matrices.

## Experiments : 

Data : Generated a graph with $|(V,E)| = (50,100)$. Created 5 copies of it with 5% perturbation on the original graph, and for each copy created 99 (so that it is 100 for each copy) with 1% perturbation on the edges.

* Without standardisation : Both PSSK and PWGK giving 1.0 accuracy for SVM and Logistic.
* With standardisation : Both PSSK and PWGK giving 0.1 accuracy for SVM and Logistic.

Trying the next experiments without standardisation of the kernel matrix.

1. With 4% and 1% perturbations for between and within class, SVM = 1.0, Logistic = 0.99 both kernels.
2. With 3% and 1% perturbations, SVM = 1.0, Logistic = 0.99 both kernels.
3. With 3% and 2% perturbations, SVM = 0.99, Logistic = 1.0 PSSK, both 1.0 in PWGK.
4. With 2% and 1% perturbations, SVM = 0.98, Logistic - 1.0 PSSK, SVM = 0.98, Logistic = 0.99 in PWGK.

Now trying with $|(V,E)|=(50,500)$. Same as before, 5 classes, 100 in each class.

1. With 4% and 1% perturbations, SVM = 1.0, Logistic = 1.0 PSSK, SVM = 1.0, Logistic = 0.99 PWGK.
2. With 3% and 1% perturbations, SVM = 0.95, Logistic = 0.99 both kernels.
3. With 3% and 2% perturbations, SVM = 0.92, Logistic = 0.93 PSSK, both 0.94 in PWGK.
4. With 2% and 1% perturbations, SVM = 0.91, Logistic - 0.89 PSSK, SVM = 0.91, Logistic = 0.88 in PWGK.

Now trying with $|(V,E)|=(50,1000)$. Same as before, 5 classes, 100 in each class.

1. With 4% and 1% perturbations, SVM = 0.89, Logistic = 0.89 PSSK, SVM = 0.9, Logistic = 0.89 PWGK.
2. With 3% and 1% perturbations, SVM = 0.53, Logistic = 0.53 both kernels. (Drastic change here)
3. With 3% and 2% perturbations, SVM = 0.6, Logistic = 0.54 PSSK, SVM = 0.61, Logistic = 0.52 in PWGK.
4. With 2% and 1% perturbations, SVM = 0.42, Logistic - 0.42 PSSK, SVM = 0.55, Logistic = 0.45 in PWGK.

Next we increase number of vertices to 100 keeping the number of edges to be 1000. A problem is that it is taking too long, almost 2 hours for one round of testing.

1. With 4% and 1% perturbation, both 1.0 in PSSK, SVM = 1.0 and Logistic = 0.99 in PWGK.
2. With 3% and 1% perturbation, both 0.99 in both kernels.
3. With 3% and 2% perturbation, SVM = 0.98, Logistic = 0.97 in PSSK, SVM = 0.98, Logistic = 0.95 in PWGK.
4. With 2% and 1% perturbation, SVM = 1.0, Logistic = 0.98 in both kernels.

Taking 100 vertices and 3000 edges.

1. With 6% and 2% perturbation, SVM = 0.87, Logistic = 0.85 with PSSK.