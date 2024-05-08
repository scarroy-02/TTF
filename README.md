# TTF Repository

Tried SVM on 3 classes of graphs with 303 total graphs. Was giving accuracy 1.0 when having 2 completely random graphs as classes.

So, made 2 classes with slight changes.

* PersistenceScaleSpaceKernel : 0.91
* PersistenceFisherKernel : 0.26
* PersistenceWeightedGaussianKernel : 0.91
* SlicedWassersteinKernel : 0.68

With big change, even persistence fisher gives 1.0 accuracy.

Now tried standardising the kernel matrix. This gives very poor accuracy with SVM as well as Logistic Regression models with precomputed kernels. The accuracy is 0.1 for both cases. Will have to fix this, or maybe use the non-standardised kernel matrices.

## Experiment 1 : 

Data : Generated a graph with $|(V,E)| = (50,100)$. Created 5 copies of it with 5% perturbation on the original graph, and for each copy created 99 (so that it is 100 for each copy) with 1% perturbation on the edges.

Without standardisation : Both PSSK and PWGK giving 1.0 accuracy for SVM and Logistic.
With standardisation : Both PSSK and PWGK giving 0.1 accuracy for SVM and Logistic.