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

## New set of experiments -

Disclaimer : These experiments were done without taking into account the dimension of the points in the persistence diagram. Will implement that aspect after this set of experiments are documented.

We have now 3 types of experiments to do. 

### Type 1 : (Testing by Madhav)

Generate random graph $G$. Create `n` classes of graphs $G_1,\dots,G_n$ by randomly perturbing the time labels of some percentage of edges of $G$. Then for each class get copies of $G_i$ by again perturbing the time labels, but on a smaller percentage of edges. Compute the kernel on this dataset and implement SVM.

#### Results :

1. V = 100, E = 1000, Sparsity = 0.2, PSSK, SVM. This is averaged over 5 runs.

| Classes | Class Perturb % | Within Perturb % | Accuracy |
|---------|-----------------|------------------|----------|
| 3       | 3               | 1                | 0.99     |
| 3       | 4               | 1.5              | 0.99     |
| 3       | 5               | 2                | 0.99     |
| 3       | 7               | 2                | 0.99     |
| 5       | 3               | 1                | 0.99     |
| 5       | 4               | 1.5              | 0.98     |
| 5       | 5               | 2                | 0.98     |
| 5       | 7               | 2                | 0.99     |
| 7       | 3               | 1                | 0.98     |
| 7       | 4               | 1.5              | 0.98     |
| 7       | 5               | 2                | 0.97     |
| 7       | 7               | 2                | 0.99     |
| 9       | 3               | 1                | 0.99     |
| 9       | 4               | 1.5              | 0.98     |
| 9       | 5               | 2                | 0.97     |
| 9       | 7               | 2                | 0.99     |

2. V = 100, E = 2000, Sparsity = 0.4, PSSK, SVM (running). This is averaged over 5 runs.

| Classes | Class Perturb % | Within Perturb % | Accuracy |
|---------|-----------------|------------------|----------|
| 3       | 3               | 1                | 0.98     |
| 5       | 3               | 1                | 0.95     |
| 7       | 3               | 1                | 0.93     |
| 9       | 3               | 1                | 0.88     |

### Type 2 : (Testing by Rohit)

Generate `n` different random graphs $G_1,\dots,G_n$. Randomly perturb time labels of some percentage of edges of $G_i$ to get (slightly different) copies of the graph $G_i$ to create a class for each $i$. Then compute the kernel on this dataset and implement SVM.

#### Results : (Was taking too much time for a single run as well)

1. V = 50, E = 1000, Sparsity = 0.7843137254901961. The below table is averaged over 5 runs.

| Classes | Perturbation % | PSSK SVM Avg Accuracy | PSSK SVM STDEV     | PSSK Logistic Avg Accuracy | PSSK Logistic STDEV | PWGK SVM Avg Accuracy | PWGK SVM STDEV     | PWGK Logistic Avg Accuracy | PWGK Logisic STDEV |
|---------|----------------|-----------------------|--------------------|----------------------------|---------------------|-----------------------|--------------------|----------------------------|--------------------|
| 3       | 3              | 0.78                  | 0.0182574185835056 | 0.78                       | 0.0298142396999972  | 0.783333333333333     | 0.0263523138347365 | 0.766666666666667          | 0.0263523138347365 |
| 3       | 4              | 0.513333333333333     | 0.137133349538161  | 0.516666666666667          | 0.129099444873581   | 0.52                  | 0.129850341205216  | 0.516666666666667          | 0.129099444873581  |
| 3       | 5              | 0.666666666666667     | 0.0754615428178118 | 0.65                       | 0.120185042515466   | 0.67                  | 0.0639009650422694 | 0.636666666666667          | 0.0844919457042438 |
| 3       | 6              | 0.546666666666667     | 0.0988826464946088 | 0.53                       | 0.0836660026534076  | 0.556666666666667     | 0.104482853457717  | 0.533333333333333          | 0.122474487139159  |
| 3       | 7              | 0.523333333333333     | 0.0976103364289755 | 0.496666666666667          | 0.0819891591749923  | 0.53                  | 0.0988826464946088 | 0.483333333333333          | 0.0799305253885453 |
| 3       | 8              | 0.526666666666667     | 0.0886629071884692 | 0.54                       | 0.0821583836257749  | 0.53                  | 0.0938379217350617 | 0.506666666666667          | 0.0821583836257749 |
| 3       | 9              | 0.473333333333333     | 0.0829993306532582 | 0.466666666666667          | 0.0964653075232519  | 0.466666666666667     | 0.067700320038633  | 0.45                       | 0.097182531580755  |
| 3       | 10             | 0.48                  | 0.0869226987360353 | 0.503333333333333          | 0.0853098926137982  | 0.48                  | 0.0908295106229248 | 0.493333333333333          | 0.104482853457717  |
| 5       | 3              | 0.546                 | 0.121161049846888  | 0.532                      | 0.128140547837131   | 0.542                 | 0.128335497817245  | 0.524                      | 0.11238327277669   |
| 5       | 4              | 0.488                 | 0.0605805249234439 | 0.46                       | 0.0821583836257749  | 0.494                 | 0.0482700735445887 | 0.422                      | 0.061400325732035  |
| 5       | 5              | 0.576                 | 0.0870631954387156 | 0.562                      | 0.0668580586017871  | 0.582                 | 0.0819756061276768 | 0.548                      | 0.0496990945591567 |
| 5       | 6              | 0.416                 | 0.0541294744108974 | 0.39                       | 0.0717635004720366  | 0.412                 | 0.0496990945591567 | 0.35                       | 0.0353553390593274 |
| 5       | 7              | 0.34                  | 0.08               | 0.326                      | 0.0983869910099908  | 0.334                 | 0.0786129760281342 | 0.334                      | 0.0998999499499374 |
| 5       | 8              | 0.34                  | 0.0570087712549569 | 0.36                       | 0.0777817459305202  | 0.344                 | 0.0585662018573853 | 0.338                      | 0.0540370243444252 |
| 5       | 9              | 0.356                 | 0.100399203184089  | 0.368                      | 0.0954986910905066  | 0.36                  | 0.0883176086632785 | 0.344                      | 0.0991463564635635 |
| 5       | 10             | 0.296                 | 0.166673333200005  | 0.268                      | 0.150731549451334   | 0.282                 | 0.144637477854116  | 0.266                      | 0.154531550176655  |
| 7       | 3              | 0.448571428571429     | 0.0938681228628543 | 0.43                       | 0.0746420027292179  | 0.454285714285714     | 0.100585023431799  | 0.414285714285714          | 0.0632858755238191 |
| 7       | 4              | 0.427142857142857     | 0.0375934210484022 | 0.418571428571429          | 0.0386639102934982  | 0.442857142857143     | 0.0397697454487859 | 0.425714285714286          | 0.0506589235042776 |
| 7       | 5              | 0.362857142857143     | 0.0304724700110022 | 0.33                       | 0.0518534040368044  | 0.365714285714286     | 0.0385978745317323 | 0.325714285714286          | 0.0444926042925641 |
| 7       | 6              | 0.395714285714286     | 0.0475416036922678 | 0.347142857142857          | 0.0412186801321529  | 0.402857142857143     | 0.0359279323998837 | 0.358571428571429          | 0.0264382221761739 |
| 7       | 7              | 0.287142857142857     | 0.0312984318574381 | 0.304285714285714          | 0.043915503282684   | 0.285714285714286     | 0.0225876975726313 | 0.29                       | 0.0376612180756116 |
| 7       | 8              | 0.304285714285714     | 0.0526346669341158 | 0.281428571428571          | 0.0389924116113034  | 0.307142857142857     | 0.0524890659167824 | 0.282857142857143          | 0.0321825152173395 |
| 7       | 9              | 0.285714285714286     | 0.0584668055133746 | 0.254285714285714          | 0.0329656593120409  | 0.291428571428571     | 0.0469476477861571 | 0.261428571428571          | 0.044204995562188  |
| 7       | 10             | 0.315714285714286     | 0.0732621794569033 | 0.292857142857143          | 0.0628814887916393  | 0.298571428571429     | 0.0576760835376753 | 0.294285714285714          | 0.0549582401762038 |
| 9       | 3              | 0.463333333333333     | 0.0563279638028292 | 0.451111111111111          | 0.058977920120401   | 0.462222222222222     | 0.051279914485397  | 0.398888888888889          | 0.077419811162866  |
| 9       | 4              | 0.421111111111111     | 0.052469862013856  | 0.41                       | 0.0521749194749951  | 0.424444444444444     | 0.0514601607862642 | 0.397777777777778          | 0.0539489928280454 |
| 9       | 5              | 0.342222222222222     | 0.0609340870364278 | 0.298888888888889          | 0.0610353065198768  | 0.34                  | 0.0612876238689849 | 0.276666666666667          | 0.0457111165127205 |
| 9       | 6              | 0.298888888888889     | 0.0278886675511359 | 0.276666666666667          | 0.0302765035409749  | 0.295555555555556     | 0.0350044088933853 | 0.273333333333333          | 0.0409003607095688 |
| 9       | 7              | 0.297777777777778     | 0.0938379217350616 | 0.285555555555556          | 0.089975991310714   | 0.296666666666667     | 0.0904890689803927 | 0.276666666666667          | 0.0769198717280955 |
| 9       | 8              | 0.243333333333333     | 0.0511292238437491 | 0.253333333333333          | 0.0616891850777392  | 0.265333333333333     | 0.0638255724902151 | 0.233333333333333          | 0.0402538242949707 |
| 9       | 9              | 0.243333333333333     | 0.0237008100085573 | 0.227777777777778          | 0.035789163129792   | 0.25968253968254      | 0.0221042788473419 | 0.221111111111111          | 0.038570122128244  |
| 9       | 10             | 0.218888888888889     | 0.039007754847871  | 0.213333333333333          | 0.0455758762266526  | 0.221111111111111     | 0.0329608821648696 | 0.198888888888889          | 0.0383695481107378 |

2. V = 100, E = 1000, Sparsity = 0.19801980198019803, PSSK. This is for one run only.

| Classes | Perturbation % | SVM Accuracy | Logistic Accuracy |
|---------|----------------|--------------|-------------------|
| 3       | 5.0            | 1.0          | 1.0               |
| 3       | 7.0            | 1.0          | 0.9833333333333333|
| 3       | 10.0           | 0.95         | 0.9333333333333333|
| 5       | 5.0            | 1.0          | 1.0               |
| 5       | 7.0            | 1.0          | 0.99              |
| 5       | 10.0           | 0.99         | 0.98              |
| 7       | 5.0            | 1.0          | 0.9928571428571429|
| 7       | 7.0            | 0.9785714285714285| 0.95         |
| 7       | 10.0           | 0.9428571428571428| 0.9357142857142857|
| 9       | 5.0            | 0.9777777777777777| 0.9666666666666667|
| 9       | 7.0            | 0.9555555555555556| 0.9555555555555556|
| 9       | 10.0           | 0.9222222222222223| 0.8944444444444445|

4. V = 100, E = 2000, Sparsity = 0.39603960396039606, PSSK. This is for one run only.

| Classes | Perturbation % | SVM Accuracy | Logistic Accuracy |
|---------|----------------|--------------|-------------------|
| 3       | 5.0            | 0.8666666666666667 | 0.8666666666666667 |
| 3       | 7.0            | 0.8166666666666667 | 0.8166666666666667 |
| 3       | 10.0           | 0.8            | 0.7666666666666667 |
| 5       | 5.0            | 0.83           | 0.69              |
| 5       | 7.0            | 0.83           | 0.75              |
| 5       | 10.0           | 0.67           | 0.62              |
| 7       | 5.0            | 0.8571428571428571 | 0.7928571428571428 |
| 7       | 7.0            | 0.6            | 0.6142857142857143 |
| 7       | 10.0           | 0.6785714285714286 | 0.5928571428571429 |
| 9       | 5.0            | 0.7722222222222223 | 0.7333333333333333 |
| 9       | 7.0            | 0.6666666666666666 | 0.55              |
| 9       | 10.0           | 0.6111111111111112 | 0.5388888888888889 |

5. V = 100, E = 3000, Sparsity = 0.594059405940594, PSSK. Data for 2 runs.

| Classes | Perturbation % | SVM Accuracy | Logistic Accuracy |
|---------|----------------|--------------|-------------------|
| 3       | 5.0            | 0.75          | 0.7               |
| 3       | 7.0            | 0.6666666666666666 | 0.6666666666666666 |
| 3       | 10.0           | 0.8           | 0.7166666666666667 |
| 5       | 5.0            | 0.61          | 0.46              |
| 5       | 7.0            | 0.63          | 0.59              |
| 5       | 10.0           | 0.61          | 0.54              |
| 7       | 5.0            | 0.6214285714285714 | 0.5857142857142857 |
| 7       | 7.0            | 0.4642857142857143 | 0.45              |
| 7       | 10.0           | 0.44285714285714284 | 0.4357142857142857 |
| 9       | 5.0            | 0.6388888888888888 | 0.5166666666666667 |
| 9       | 7.0            | 0.4722222222222222 | 0.4222222222222222 |
| 9       | 10.0           | 0.4111111111111111 | 0.37777777777777777 |

| Classes | Perturbation % | SVM Accuracy | Logistic Accuracy |
|---------|----------------|--------------|-------------------|
| 3       | 5.0            | 0.8           | 0.7166666666666667 |
| 3       | 7.0            | 0.7666666666666667 | 0.75              |
| 3       | 10.0           | 0.8166666666666667 | 0.7833333333333333 |
| 5       | 5.0            | 0.58          | 0.49              |
| 5       | 7.0            | 0.55          | 0.52              |
| 5       | 10.0           | 0.35          | 0.37              |
| 7       | 5.0            | 0.4785714285714286 | 0.45              |
| 7       | 7.0            | 0.5428571428571428 | 0.44285714285714284 |
| 7       | 10.0           | 0.4928571428571429 | 0.4142857142857143 |
| 9       | 5.0            | 0.5388888888888889 | 0.42777777777777776|
| 9       | 7.0            | 0.45555555555555555 | 0.4222222222222222 |
| 9       | 10.0           | 0.3           | 0.3111111111111111 |

6. V = 100, E = 4000, Sparsity = 0.7920792079207921, PSSK. Data for 2 runs.

| Classes | Perturbation % | SVM Accuracy | Logistic Accuracy |
|---------|----------------|--------------|-------------------|
| 3       | 5.0            | 0.8333333333333334 | 0.85              |
| 3       | 7.0            | 0.7833333333333333 | 0.8               |
| 3       | 10.0           | 0.7            | 0.75              |
| 5       | 5.0            | 0.43           | 0.44              |
| 5       | 7.0            | 0.41           | 0.41              |
| 5       | 10.0           | 0.35           | 0.34              |
| 7       | 5.0            | 0.5            | 0.45714285714285713 |
| 7       | 7.0            | 0.35           | 0.3142857142857143 |
| 7       | 10.0           | 0.4857142857142857 | 0.4642857142857143 |
| 9       | 5.0            | 0.5111111111111111 | 0.4222222222222222 |
| 9       | 7.0            | 0.45555555555555555 | 0.42777777777777776|
| 9       | 10.0           | 0.24444444444444444 | 0.2111111111111111 |

| Classes | Perturbation % | SVM Accuracy | Logistic Accuracy |
|---------|----------------|--------------|-------------------|
| 3       | 5.0            | 0.5666666666666667 | 0.5833333333333334 |
| 3       | 7.0            | 0.6833333333333333 | 0.7               |
| 3       | 10.0           | 0.7166666666666667 | 0.75              |
| 5       | 5.0            | 0.62           | 0.6               |
| 5       | 7.0            | 0.32           | 0.27              |
| 5       | 10.0           | 0.38           | 0.34              |
| 7       | 5.0            | 0.5857142857142857 | 0.5428571428571428 |
| 7       | 7.0            | 0.45           | 0.45714285714285713 |
| 7       | 10.0           | 0.3142857142857143 | 0.2785714285714286 |
| 9       | 5.0            | 0.37777777777777777 | 0.31666666666666665 |
| 9       | 7.0            | 0.4222222222222222 | 0.45              |
| 9       | 10.0           | 0.4111111111111111 | 0.35555555555555557 |

### Type 3 : (Testing not started yet)

Sort of a combination of both type 1 and type 2. Generate random graphs, then for each graph generate the data as type 1. Then form the kernels and perform SVM.

## Dimension wise experiments

* Trying dimension-wise kernelization process.
* Changed the function for incorporating the dimension wise persistence features.
* Scrapped the use of giotto-tda.
* Noticable results :
    - Tried with sparsity 0.8 graphs (50,1000), with 5% perturbation.
    - Using only dimension 2 features gave the best accuracy (95%).
    - Older accuracy using giotto was around 67% the same setup.

## Incorporating C++

The experiments from now on will use C++ for kernelization process. Steps to compile using C++ are as follows.

* Make sure you have Eigen library installed. Suppose the path is `/path/to/eigen`.
* Compile the `kernelizaion_multiprocess.cpp` program first using the following command.
```
g++ -o kmp kernelization_multiprocess.cpp -I/path/to/eigen -pthread -O3
```
* Then run the python notebook.

### Type 2 Experiment

1. 50 vertces, 1000 edges, PSSK, min-wt filtration, dim 2 points only.

|   Classes |   Perturbation % |   SVM Avg Accuracy |   SVM StdDev |   Logistic Avg Accuracy |   Logistic StdDev |
|----------:|-----------------:|-------------------:|-------------:|------------------------:|------------------:|
|         3 |                3 |           0.97     |    0.0323179 |                0.956667 |         0.0309121 |
|         3 |                4 |           0.93     |    0.0244949 |                0.923333 |         0.0416333 |
|         3 |                5 |           0.923333 |    0.0226078 |                0.89     |         0.0628932 |
|         3 |                6 |           0.87     |    0.0956847 |                0.846667 |         0.102415  |
|         3 |                7 |           0.893333 |    0.038873  |                0.886667 |         0.04      |
|         3 |                8 |           0.82     |    0.0531246 |                0.85     |         0.0666667 |
|         3 |                9 |           0.793333 |    0.0847218 |                0.793333 |         0.0898146 |
|         3 |               10 |           0.79     |    0.076449  |                0.746667 |         0.0819214 |
|         5 |                3 |           0.944    |    0.0224499 |                0.94     |         0.02      |
|         5 |                4 |           0.918    |    0.0416653 |                0.888    |         0.0881816 |
|         5 |                5 |           0.88     |    0.045607  |                0.862    |         0.0271293 |
|         5 |                6 |           0.77     |    0.0189737 |                0.786    |         0.0407922 |
|         5 |                7 |           0.824    |    0.0484149 |                0.798    |         0.0370945 |
|         5 |                8 |           0.734    |    0.0640625 |                0.708    |         0.0685274 |
|         5 |                9 |           0.734    |    0.0711618 |                0.72     |         0.0544059 |
|         5 |               10 |           0.712    |    0.0810925 |                0.69     |         0.102567  |
|         7 |                3 |           0.881429 |    0.0314934 |                0.862857 |         0.0261081 |
|         7 |                4 |           0.88     |    0.0387035 |                0.837143 |         0.0618425 |
|         7 |                5 |           0.865714 |    0.0317516 |                0.83     |         0.0342261 |
|         7 |                6 |           0.787143 |    0.0333197 |                0.758571 |         0.0236471 |
|         7 |                7 |           0.734286 |    0.0311022 |                0.738571 |         0.0390186 |
|         7 |                8 |           0.738571 |    0.0194831 |                0.708571 |         0.0276273 |
|         7 |                9 |           0.661429 |    0.0729271 |                0.632857 |         0.068898  |
|         7 |               10 |           0.607143 |    0.0959379 |                0.611429 |         0.09955   |
|         9 |                3 |           0.875556 |    0.025483  |                0.855556 |         0.0462147 |
|         9 |                4 |           0.804444 |    0.0334073 |                0.765556 |         0.0518069 |
|         9 |                5 |           0.794444 |    0.0278887 |                0.771111 |         0.0493664 |
|         9 |                6 |           0.714444 |    0.0371184 |                0.668889 |         0.0514722 |
|         9 |                7 |           0.678889 |    0.0475836 |                0.662222 |         0.0508447 |
|         9 |                8 |           0.623333 |    0.0470618 |                0.582222 |         0.0313089 |
|         9 |                9 |           0.65     |    0.0484322 |                0.606667 |         0.0496158 |
|         9 |               10 |           0.583333 |    0.0378431 |                0.544444 |         0.0389682 |


## Using Average Filteration

### Type 1 : (Testing by Madhav)


Generate random graph $G$. Create `n` classes of graphs $G_1,\dots,G_n$ by randomly perturbing the time labels of some percentage of edges of $G$. Then for each class get copies of $G_i$ by again perturbing the time labels, but on a smaller percentage of edges. Compute the kernel on this dataset and implement SVM.

The follwoing experiments are done with avg filteration. Only 2 dimensional persistence points are considred.

#### Results :

1. V = 100, E = 1000, Sparsity = 0.2, PSSK, SVM. This is averaged over 5 runs.

| Classes | Class Perturb % | Within Perturb % | Accuracy |
|---------|-----------------|------------------|----------|
| 3       | 3               | 1                | 0.99     |
| 3       | 4               | 1.5              | 0.98     |
| 3       | 5               | 2                | 1        |
| 3       | 7               | 2                | 0.99     |
| 5       | 3               | 1                | 1        |
| 5       | 4               | 1.5              | 0.99     |
| 5       | 5               | 2                | 0.98     |
| 5       | 7               | 2                | 0.99     |
| 7       | 3               | 1                | 0.97     |
| 7       | 4               | 1.5              | 0.99     |
| 7       | 5               | 2                | 0.99     |
| 7       | 7               | 2                | 0.99     |
| 9       | 3               | 1                | 0.98     |
| 9       | 4               | 1.5              | 0.98     |
| 9       | 5               | 2                | 0.98     |
| 9       | 7               | 2                | 0.99     |

2. V = 100, E = 2000, Sparsity = 0.4, PSSK, SVM. This is averaged over 5 runs.

| Classes | Class Perturb % | Within Perturb % | Accuracy |
|---------|-----------------|------------------|----------|
| 3       | 3               | 1                | 1        |
| 3       | 4               | 1.5              |   1      |
| 3       | 5               | 2                |   1      |
| 3       | 7               | 2                |   1      |
| 5       | 3               | 1                |  1       |
| 5       | 4               | 1.5              |   1   |
| 5       | 5               | 2                |    1  |
| 5       | 7               | 2                |   1  |
| 7       | 3               | 1                |   1  |
| 7       | 4               | 1.5              |   1   |
| 7       | 5               | 2                |      |
| 7       | 7               | 2                |      |
| 9       | 3               | 1                |      |
| 9       | 4               | 1.5              |      |
| 9       | 5               | 2                |   1   |
| 9       | 7               | 2                |    1  |

3. V = 100, E = 3000, Sparsity = 0.6, PSSK, SVM. This is averaged over 5 runs.

| Classes | Class Perturb % | Within Perturb % | Accuracy |
|---------|-----------------|------------------|----------|
| 3       | 3               | 1                |    1 |
| 3       | 4               | 1.5              |    1  |
| 3       | 5               | 2                |      |
| 3       | 7               | 2                |      |
| 5       | 3               | 1                |   0.99   |
| 5       | 4               | 1.5              |      |
| 5       | 5               | 2                |      |
| 5       | 7               | 2                |     |
| 7       | 3               | 1                |     |
| 7       | 4               | 1.5              |      |
| 7       | 5               | 2                |      |
| 7       | 7               | 2                |      |
| 9       | 3               | 1                |      |
| 9       | 4               | 1.5              |      |
| 9       | 5               | 2                |      |
| 9       | 7               | 2                |      |


