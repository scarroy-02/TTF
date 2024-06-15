import random
import gudhi as gd
import numpy as np
import pandas as pd
from tabulate import tabulate
from gudhi.representations import kernel_methods
import networkx as nx
from utils import *
from tqdm import tqdm
import subprocess
from joblib import Parallel, delayed
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

def svm_output(mat_train,mat_test,y_train,y_test):
    # Using SVM

    svm_classifier = SVC(kernel='precomputed')
    svm_classifier.fit(mat_train, y_train)

    # y_pred = svm_classifier.predict(mat_test)

    accuracy = svm_classifier.score(mat_test, y_test)
    print("Accuracy using SVM : ", accuracy)
    return accuracy
    # print(classification_report(y_test,y_pred))

def logistic_output(mat_train,mat_test,y_train,y_test):

    # Using logistic regression

    klr = LogisticRegression(max_iter=1000, solver='liblinear')
    klr.kernel = 'precomputed'

    klr.fit(mat_train,y_train)

    # y_pred = klr.predict(mat_test)

    accuracy = klr.score(mat_test, y_test)
    print("Accuracy using Logistic Regression : ", accuracy)
    return accuracy

    # print(classification_report(y_test,y_pred))

def new_testing(v,e,n_cluster,n_copies,wp,pers_dim):

    # Calculate sparsity
    sparsity = 2 * e / (v * (v + 1))
    print(f"Sparsity : {sparsity}")

    # Generate class graphs and assign random times to edges
    class_graphs = [nx.gnm_random_graph(v, e) for _ in range(n_cluster)]
    for G in class_graphs:
        for (u, v) in G.edges():
            G.edges[u, v]['time'] = random.randint(0, 100)

    # Apply change_graph function in parallel
    all_graphs = Parallel(n_jobs=-1)(delayed(change_graph)(grph, wp) for grph in class_graphs for _ in range(n_copies))

    # Generate labels
    label = [i for i in range(n_cluster) for _ in range(n_copies)]

    # Apply assign_weights function in parallel
    Lw = Parallel(n_jobs=-1)(delayed(assign_weights)(i) for i in all_graphs)

    # Apply adj_fillinf function in parallel
    Lwe = Parallel(n_jobs=-1)(delayed(adj_fillinf)(i) for i in Lw)

    input_diag_trial = []

    # Trying Gudhi dimension-wise
    for Ad in tqdm(Lwe):
        skeleton = gd.RipsComplex(distance_matrix=Ad, max_edge_length=2000)
        simplex_tree = skeleton.create_simplex_tree(max_dimension=pers_dim+2)
        barcode = simplex_tree.persistence()
        input_diag_trial.append(simplex_tree.persistence_intervals_in_dimension(pers_dim))

    for i in range(n_cluster*n_copies):
        input_diag_trial[i][input_diag_trial[i] == np.inf] = 10000

    X_train, X_test, y_train, y_test = train_test_split(input_diag_trial, label, test_size=0.2, random_state=42)

    X_combined = (X_train + X_test)

    # Write the diagrams to a file
    with open('persistent_diagrams.txt', 'w') as f:
        for diagram in X_combined:
            np.savetxt(f, diagram, fmt='%.2f')
            f.write('\n')

    print("Persistence diagrams file written")

    def compute_kernel_matrix():
        # Call the C++ program
        result = subprocess.run(['./kmp'], check=True)
        
        if result.returncode != 0:
            raise Exception("C++ program failed to run.")
        
        # Load the kernel matrix from the CSV file
        kernel_matrix = np.loadtxt('kernel_matrix.csv', delimiter=',')
        return kernel_matrix
    
    # Compute the kernel matrix using the C++ program
    pssk_matrix_combined = compute_kernel_matrix()

    print("Kernelization complete")

    # Split the kernel matrix into train and test parts
    num_train = len(X_train)
    pssk_matrix_train = pssk_matrix_combined[:num_train, :num_train]
    pssk_matrix_test = pssk_matrix_combined[num_train:, :num_train]

    # Weighted Gaussian Kernel

    # pwgk = kernel_methods.PersistenceWeightedGaussianKernel(bandwidth=1)
    # pwgk_matrix_combined = pwgk.fit_transform(X_combined)
    # pwgk_matrix_train = pwgk_matrix_combined[:num_train, :num_train]
    # pwgk_matrix_test = pwgk_matrix_combined[num_train:, :num_train]

    print("Using Scale Space Kernel")
    return svm_output(pssk_matrix_train,pssk_matrix_test,y_train,y_test), logistic_output(pssk_matrix_train,pssk_matrix_test,y_train,y_test)

    # print("Using Weighted Gaussian Kernel : ")
    # svm_output(pwgk_matrix_train,pwgk_matrix_test,y_train,y_test)
    # logistic_output(pwgk_matrix_train,pwgk_matrix_test,y_train,y_test)

def run_experiments(v, e, n_clusters_list, n_copies, wp_list, pers_dim, n_runs=5):
    results = []

    for n_cluster in n_clusters_list:
        for wp in wp_list:
            svm_accuracies = []
            logistic_accuracies = []
            
            for _ in range(n_runs):
                svm_accuracy, logistic_accuracy = new_testing(v, e, n_cluster, n_copies, wp, pers_dim)
                svm_accuracies.append(svm_accuracy)
                logistic_accuracies.append(logistic_accuracy)
            
            svm_avg_accuracy = np.mean(svm_accuracies)
            svm_std_accuracy = np.std(svm_accuracies)
            logistic_avg_accuracy = np.mean(logistic_accuracies)
            logistic_std_accuracy = np.std(logistic_accuracies)
            
            results.append((n_cluster, wp*100, svm_avg_accuracy, svm_std_accuracy, logistic_avg_accuracy, logistic_std_accuracy))
    
    return results

# Parameters
v = 50
e = 1000
n_clusters_list = [3, 5, 7, 9]
n_copies = 100
wp_list = [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
pers_dim = 2
n_runs = 5

# Run experiments
results = run_experiments(v, e, n_clusters_list, n_copies, wp_list, pers_dim, n_runs)

# Create DataFrame
columns = ['Classes', 'Perturbation %', 'SVM Avg Accuracy', 'SVM StdDev', 'Logistic Avg Accuracy', 'Logistic StdDev']
df = pd.DataFrame(results, columns=columns)

# Use tabulate to format the DataFrame as a Markdown table
markdown_table = tabulate(df, headers='keys', tablefmt='pipe', showindex=False)

# Write the table to a text file
with open('experiment_results.md', 'w') as f:
    f.write(markdown_table)

print("Results have been written to experiment_results.md")