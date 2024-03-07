"""
Subspace method example on covariate shift dataset
====================================================

An example of the subspace methods on a dataset subject
to covariate shift
"""

# Author:   Ruben Bueno <ruben.bueno@polytechnique.edu>
#
# License: BSD 3-Clause
# sphinx_gallery_thumbnail_number = 4

# %% Imports
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.svm import SVC

from skada import (
    SubspaceAlignment,
    TransferComponentAnalysis,
    TransferJointMatching,
    source_target_split,
)
from skada.datasets import make_shifted_datasets

# %%
#     The subspaces methods
# ------------------------------------------
#
# The goal of subspace is to project data from a d dimensional space
# into a d' dimensional space with d'<d.
# This kind of da method is especially good when we work with subspace
# shift, meaning that there is a subspace on which, when projected on it,
# the source and target data have the same distributions.

base_classifier = SVC()

print(f"Will be using {base_classifier} as base classifier", end="\n\n")

# %%
# We generate our 2D dataset with 2 classes
# ------------------------------------------
#
# We generate a simple 2D dataset with subspace shift.

RANDOM_SEED = 42

X, y, sample_domain = make_shifted_datasets(
    n_samples_source=20,
    n_samples_target=20,
    noise=0.1,
    random_state=RANDOM_SEED,
    shift="subspace",
)

Xs, Xt, ys, yt = source_target_split(X, y, sample_domain=sample_domain)

# %%
# Plot of the dataset:
# ------------------------------------------

x_min, x_max = -2.4, 2.4
y_min, y_max = -2.4, 2.4


figsize = (8, 4)
figure, axes = plt.subplots(1, 2, figsize=figsize)

cm = plt.cm.RdBu
colormap = ListedColormap(["#FFA056", "#6C4C7C"])
ax = axes[0]
ax.set_title("Source data")
# Plot the source points:
ax.scatter(Xs[:, 0], Xs[:, 1], c=ys, cmap=colormap, alpha=0.7, s=[15])

ax.set_xticks(()), ax.set_yticks(())
ax.set_xlim(x_min, x_max), ax.set_ylim(y_min, y_max)

ax = axes[1]

ax.set_title("Target data")
# Plot the target points:
ax.scatter(Xt[:, 0], Xt[:, 1], c=ys, cmap=colormap, alpha=0.1, s=[15])
ax.scatter(Xt[:, 0], Xt[:, 1], c=yt, cmap=colormap, alpha=0.7, s=[15])
figure.suptitle("Plot of the dataset", fontsize=16, y=1)
ax.set_xticks(()), ax.set_yticks(())
ax.set_xlim(x_min, x_max), ax.set_ylim(y_min, y_max)

# %%
#     Illustration of the problem with no domain adaptation
# ------------------------------------------
#
# When not using domain adaptation, the classifier won't train on
# data that is distributed as the target sample domain, it will thus
# not be performing optimaly.

# We create a dict to store scores:
scores_dict = {}


def create_plots(
    clf,
    name="Without DA",
    suptitle=None,
):
    size = np.array([16] * Xs.shape[0])

    if suptitle is None:
        suptitle = f"Illustration of the {name} method"
    figure, axes = plt.subplots(1, 3, figsize=figsize)
    ax = axes[1]
    score = clf.score(Xt, yt)
    DecisionBoundaryDisplay.from_estimator(
        clf,
        Xs,
        cmap=colormap,
        alpha=0.1,
        ax=ax,
        eps=0.5,
        response_method="predict",
    )

    # Plot the target points:
    ax.scatter(
        Xt[:, 0],
        Xt[:, 1],
        c=yt,
        cmap=colormap,
        alpha=0.7,
        s=[15],
    )

    ax.set_xticks(()), ax.set_yticks(())
    ax.set_xlim(x_min, x_max), ax.set_ylim(y_min, y_max)
    ax.set_title("Accuracy on target", fontsize=12)
    ax.text(
        x_max - 0.3,
        y_min + 0.3,
        ("%.2f" % score).lstrip("0"),
        size=15,
        horizontalalignment="right",
    )
    scores_dict[name] = score

    ax = axes[0]

    # Plot the source points:
    ax.scatter(Xs[:, 0], Xs[:, 1], c=ys, cmap=colormap, alpha=0.7, s=size)

    ax.set_xticks(()), ax.set_yticks(())
    ax.set_xlim(x_min, x_max), ax.set_ylim(y_min, y_max)
    ax.set_title("Training with rewegihted data", fontsize=12)
    if name != "Without DA":
        ax = axes[2]
        keys = list(clf.named_steps.keys())
        subspace_estimator = clf.named_steps[keys[0]].base_estimator
        subspace_estimator.fit(X, sample_domain=sample_domain)
        ax.scatter(
            subspace_estimator.adapt(Xt),
            [0] * Xt.shape[0],
            c=yt,
            cmap=colormap,
            alpha=0.5,
            s=size,
        )
        ax.set_xticks(()), ax.set_yticks(())
        ax.set_title("Subspace")

    figure.suptitle(suptitle, fontsize=16, y=1)


clf = base_classifier
clf.fit(Xs, ys)
create_plots(
    base_classifier, "Without DA", suptitle="Illustration of the classifier with no DA"
)


# %%
#     Illustration of the subspace Alignment method
# ------------------------------------------
#
# As we assume that the  source and target domains are represented
# by subspaces described by eigenvectors;
# This method seeks a domain adaptation solution by learning a mapping
# function which aligns the source subspace with the target one.
#
# See [1]_ for details:
# .. [1] Basura Fernando et. al. Unsupervised Visual
#        Domain Adaptation Using Subspace Alignment.
#        In IEEE International Conference on Computer Vision, 2013.

clf = SubspaceAlignment(base_classifier, n_components=1)
clf.fit(X, y, sample_domain=sample_domain)
create_plots(clf, "Subspace Alignment")

# %%
#     Illustration of the Transfer Component Analysis method
# ------------------------------------------
#
# The goal of Transfer Component Analysis (or TCA) is to learn some transfer
# components across domains in a reproducing kernel Hilbert space using maximum
# mean discrepancy (mmd).
#
# See [2]_ for details:
# .. [2] Sinno Jialin Pan et. al. Domain Adaptation via
#        Transfer Component Analysis. In IEEE Transactions
#        on Neural Networks, 2011.

clf = TransferComponentAnalysis(base_classifier, n_components=1, mu=2)
clf.fit(X, y, sample_domain=sample_domain)
create_plots(clf, "TCA")

# %%
#     Illustration of the Transfer Joint Matching method
# ------------------------------------------
#
# In most of the previous works, we explored two learning strategies independently for
# domain adaptation: feature matching and instance reweighting. Transfer Joint Matching
# or TJM aims to use both, by adding a constant to tradeoff between to two.
#
# See [3]_ for details:
# .. [3] Long et al., 2014] Long, M., Wang, J., Ding, G., Sun, J., and Yu, P. (2014).
#         Transfer joint matching for unsupervised domain adaptation. In IEEE Conference
#         on Computer Vision and Pattern Recognition (CVPR), pages 1410–1417.

clf = TransferJointMatching(base_classifier, tradeoff=2, n_components=1, max_iter=20)
clf.fit(X, y, sample_domain=sample_domain)
create_plots(
    clf,
    "TransferJointMatching",
)


# %%
#     Comparisaon of score between reweighting methods:
# ------------------------------------------


def print_scores_as_table(scores):
    keys = list(scores.keys())
    lengths = [len(k) for k in keys]
    max_lenght = max(lengths)
    for k in keys:
        print(f"{k}{' '*(max_lenght - len(k))} | ", end="")
        print(f"{scores[k]*100}{' '*(6-len(str(scores[k]*100)))}%")


print_scores_as_table(scores_dict)

plt.show()