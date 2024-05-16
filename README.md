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

We have now 3 types of experiments to do. 

### Type 1 : (Testing by Madhav)

Generate random graph $G$. Create `n` classes of graphs $G_1,\dots,G_n$ by randomly perturbing the time labels of some percentage of edges of $G$. Then for each class get copies of $G_i$ by again perturbing the time labels, but on a smaller percentage of edges. Compute the kernel on this dataset and implement SVM.

#### Results :

1. V = 100, E = 1000, Sparsity = 0.2, PSSK, SVM

| Classes | Class Perturb % | Within Perturb % | Avg Accuracy |
|---------|-----------------|------------------|--------------|
| 3       | 3               | 1                | 0.99         |
| 5       | 3               | 1                | 0.99         |
| 7       | 3               | 1                | 0.98         |
| 9       | 3               | 1                | 0.99         |

2. V = 100, E = 1000, Sparsity = 0.2, big_change = 4%, small_change = 1.5%, PSSK, SVM (running)

### Type 2 : (Testing by Rohit)

Generate `n` different random graphs $G_1,\dots,G_n$. Randomly perturb time labels of some percentage of edges of $G_i$ to get (slightly different) copies of the graph $G_i$ to create a class for each $i$. Then compute the kernel on this dataset and implement SVM.

#### Results : (Was taking too much time for a single run as well)

1. V = 50, E = 1000, Sparsity = 0.7843137254901961

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

2. V = 100, E = 1000, Sparsity = 0.19801980198019803. (Will update table)
3. V = 100, E = 2000, Sparsity = 0.39603960396039606. (Will update table)
4. V = 100, E = 3000, Sparsity = 0.594059405940594. (Will update table)
5. V = 100, E = 4000, Sparsity = 0.7920792079207921. (Will update table)

### Type 3 : (Testing not started yet)

Sort of a combination of both type 1 and type 2. Generate random graphs, then for each graph generate the data as type 1. Then form the kernels and perform SVM.
