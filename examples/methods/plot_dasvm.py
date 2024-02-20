"""
    plot for the dasvm estimator
==========================================

This example illustrates the dsvm method from [1].

.. [1]  Domain Adaptation Problems: A DASVM Classification
        Technique and a Circular Validation Strategy
        Lorenzo Bruzzone, Fellow, IEEE, and Mattia Marconcini, Member, IEEE

"""

# Author: Ruben Bueno <ruben.bueno@polytechnique.edu>
# dasvm plots

import numpy as np
import matplotlib.pyplot as plt

from skada.datasets import make_shifted_datasets
from skada._dasvm import DASVMEstimator
from skada.utils import check_X_y_domain, source_target_split
from sklearn.base import clone

from sklearn.svm import SVC


# base_estimator can be any classifier equipped with `decision_function` such as:
# SVC(gamma='auto'), LogisticRegression(random_state=0), etc...
base_estimator = SVC(kernel="rbf")

xlim = (-2.2, 4.2)
ylim = (-2, 4.2)

figure, axis = plt.subplots(1, 2)

X, y, sample_domain = make_shifted_datasets(
    n_samples_source=20,
    n_samples_target=15,
    shift="covariate_shift",
    noise=None,
    label="multiclass",
)
X, y, sample_domain = check_X_y_domain(X, y, sample_domain)
Xs, Xt, ys, yt = source_target_split(
    X, y, sample_domain=sample_domain
)


axis[0].scatter(Xs[:, 0], Xs[:, 1], c=ys)
axis[0].set_xlim(xlim)
axis[0].set_ylim(ylim)
axis[0].set_title("source data points")

axis[1].scatter(Xt[:, 0], Xt[:, 1], c=yt)
axis[1].set_xlim(xlim)
axis[1].set_ylim(ylim)
axis[1].set_title("target data points")

figure.suptitle("data points", fontsize=20)

estimator = DASVMEstimator(
    base_estimator=clone(base_estimator), k=5,
    save_estimators=True, save_indices=True).fit(
    X, y, sample_domain=sample_domain)

epsilon = 0.05
N = 4
K = len(estimator.estimators)//N
figure, axis = plt.subplots(1, N+1)
for i in list(range(0, N*K, K)) + [-1]:
    j = i//K if i != -1 else -1
    e = estimator.estimators[i]
    x_points = np.linspace(xlim[0], xlim[1], 200)
    y_points = np.linspace(ylim[0], ylim[1], 200)
    X = np.array([[x, y] for x in x_points for y in y_points])
    axis[j].scatter(
        X[:, 0], X[:, 1], c=e.decision_function(X), alpha=0.03)

    # plot margins
    X_ = X[np.absolute(e.decision_function(X)-1)<epsilon]
    axis[j].scatter(
        X_[:, 0], X_[:, 1], c=[1]*X_.shape[0], alpha=1, cmap="gray", s=[0.1]*X_.shape[0])
    X_ = X[np.absolute(e.decision_function(X)+1)<epsilon]
    axis[j].scatter(
        X_[:, 0], X_[:, 1], c=[1]*X_.shape[0], alpha=1, cmap="gray", s=[0.1]*X_.shape[0])
    X_ = X[np.absolute(e.decision_function(X))<epsilon]
    axis[j].scatter(
        X_[:, 0], X_[:, 1], c=[1]*X_.shape[0], alpha=1, cmap="autumn", s=[0.1]*X_.shape[0])

    X = np.concatenate((
        Xs[~estimator.indices_source_deleted[i]],
        Xt[estimator.indices_target_added[i]]))
    try:
        a = axis[j].scatter(X[:, 0], X[:, 1], c=np.concatenate((
            ys[~estimator.indices_source_deleted[i]],
            e.predict(Xt[estimator.indices_target_added[i]]))))
    except:
        a = axis[j].scatter(X[:, 0], X[:, 1], c=
        ys[~estimator.indices_source_deleted[i]])
    X = Xt[~estimator.indices_target_added[i]]
    axis[j].scatter(
        X[:, 0], X[:, 1], cmap="gray", 
        c=[0.5]*X.shape[0], alpha=0.5, vmax=1, vmin=0)

    axis[j].set_xlim(xlim)
    axis[j].set_ylim(ylim)
figure.colorbar(a)
figure.suptitle("reasulting predictions", fontsize=20)
plt.show()
