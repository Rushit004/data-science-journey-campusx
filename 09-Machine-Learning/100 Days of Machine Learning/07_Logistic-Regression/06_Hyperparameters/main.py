"""
Logistic Regression Hyperparameter Simulator
Original concept & app: CampusX (100 Days of ML)
This version: fixed for compatibility with current scikit-learn releases
(multi_class parameter removed upstream, penalty=None handled properly,
l1_ratio now a real float, solver/penalty errors surfaced cleanly).

Run with:  streamlit run app.py
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from sklearn.datasets import make_blobs
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def load_initial_graph(dataset_name, ax):
    """Generate a synthetic 2D dataset and draw the raw scatter plot."""
    if dataset_name == "Binary":
        X, y = make_blobs(n_features=2, centers=2, random_state=6)
    else:  # "Multiclass"
        X, y = make_blobs(n_features=2, centers=3, random_state=2)

    ax.scatter(X[:, 0], X[:, 1], c=y, cmap="rainbow", edgecolors="black")
    return X, y


def draw_meshgrid(X):
    """Build a grid over the feature space so we can shade the decision regions."""
    a = np.arange(X[:, 0].min() - 1, X[:, 0].max() + 1, 0.05)
    b = np.arange(X[:, 1].min() - 1, X[:, 1].max() + 1, 0.05)
    XX, YY = np.meshgrid(a, b)
    input_array = np.c_[XX.ravel(), YY.ravel()]
    return XX, YY, input_array


# ----------------------------------------------------------------------
# Streamlit page setup
# ----------------------------------------------------------------------

plt.style.use("fivethirtyeight")
st.set_page_config(page_title="Logistic Regression Hyperparameters", layout="centered")
st.sidebar.markdown("# Logistic Regression Classifier")

dataset = st.sidebar.selectbox("Select Dataset", ("Binary", "Multiclass"))

penalty = st.sidebar.selectbox("Regularization (penalty)", ("l2", "l1", "elasticnet", "None"))

c_input = st.sidebar.number_input("C (inverse regularization strength)", value=1.0, min_value=0.001, max_value=1000.0)

solver = st.sidebar.selectbox(
    "Solver", ("lbfgs", "liblinear", "newton-cg", "newton-cholesky", "sag", "saga")
)

max_iter = int(st.sidebar.number_input("Max Iterations", value=100, min_value=10, max_value=20000, step=10))

multiclass_strategy = st.sidebar.selectbox(
    "Multiclass Strategy",
    ("auto (multinomial)", "One-vs-Rest (OvR)"),
    help="'auto' lets scikit-learn use the joint multinomial/softmax loss. "
         "'OvR' trains one binary classifier per class via OneVsRestClassifier.",
)

# l1_ratio is only meaningful for elasticnet — only show it then
l1_ratio = None
if penalty == "elasticnet":
    l1_ratio = st.sidebar.slider("L1 Ratio (Elastic Net mix)", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

# ----------------------------------------------------------------------
# Initial (untrained) plot
# ----------------------------------------------------------------------

fig, ax = plt.subplots()
X, y = load_initial_graph(dataset, ax)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
orig = st.pyplot(fig)

# ----------------------------------------------------------------------
# Run the model
# ----------------------------------------------------------------------

if st.sidebar.button("Run Algorithm"):
    orig.empty()

    model_params = {
        "penalty": None if penalty == "None" else penalty,
        "C": float(c_input),
        "solver": solver,
        "max_iter": max_iter,
    }
    if penalty == "elasticnet":
        model_params["l1_ratio"] = l1_ratio

    base_clf = LogisticRegression(**model_params)

    # scikit-learn no longer accepts multi_class='ovr' directly (parameter was
    # removed) — OneVsRestClassifier is the current supported way to get that
    # behaviour, so we wrap the estimator instead of passing a kwarg.
    if multiclass_strategy == "One-vs-Rest (OvR)":
        clf = OneVsRestClassifier(base_clf)
    else:
        clf = base_clf

    try:
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        XX, YY, input_array = draw_meshgrid(X)
        labels = clf.predict(input_array)

        fig2, ax2 = plt.subplots()
        ax2.contourf(XX, YY, labels.reshape(XX.shape), alpha=0.5, cmap="rainbow")
        ax2.scatter(X[:, 0], X[:, 1], c=y, cmap="rainbow", edgecolors="black")
        ax2.set_xlabel("Feature 1")
        ax2.set_ylabel("Feature 2")
        ax2.set_title(f"Logistic Regression (penalty={penalty}, C={c_input}, solver={solver})")

        st.pyplot(fig2)
        st.subheader(f"Accuracy (Logistic Regression): {round(accuracy_score(y_test, y_pred), 2)}")

    except ValueError as e:
        st.error(f"Error: {e}")
        st.info(
            "That combination of penalty/solver/multiclass-strategy isn't supported. "
            "Common fixes: 'elasticnet' needs solver='saga'; 'liblinear' can't do "
            "multinomial multiclass directly — use the OvR strategy with it instead."
        )