import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score


def draw_meshgrid():
    a = np.arange(start=X[:, 0].min() - 1, stop=X[:, 0].max() + 1, step=0.01)
    b = np.arange(start=X[:, 1].min() - 1, stop=X[:, 1].max() + 1, step=0.01)
    XX, YY = np.meshgrid(a, b)
    input_array = np.array([XX.ravel(), YY.ravel()]).T
    return XX, YY, input_array


X, y = make_moons(n_samples=500, noise=0.30, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

plt.style.use('fivethirtyeight')

st.sidebar.markdown("# Decision Tree Classifier")

criterion = st.sidebar.selectbox('Criterion', ('gini', 'entropy'), key='criterion')
splitter = st.sidebar.selectbox('Splitter', ('best', 'random'), key='splitter')
max_depth = int(st.sidebar.number_input('Max Depth', min_value=0, value=0, key='max_depth'))

# sklearn requires min_samples_split >= 2 when given as an int
min_samples_split = st.sidebar.slider(
    'Min Samples Split', min_value=2, max_value=X_train.shape[0], value=2, key='min_samples_split'
)
min_samples_leaf = st.sidebar.slider(
    'Min Samples Leaf', min_value=1, max_value=X_train.shape[0], value=1, key='min_samples_leaf'
)
max_features = st.sidebar.slider('Max Features', min_value=1, max_value=2, value=2, key='max_features')
max_leaf_nodes = int(st.sidebar.number_input('Max Leaf Nodes', min_value=0, value=0, key='max_leaf_nodes'))
min_impurity_decrease = st.sidebar.number_input('Min Impurity Decrease', value=0.0, key='min_impurity_decrease')

# Initial scatter plot
fig, ax = plt.subplots()
ax.scatter(X[:, 0], X[:, 1], c=y, cmap='rainbow')
orig = st.pyplot(fig)

if st.sidebar.button('Run Algorithm'):
    orig.empty()

    clf = DecisionTreeClassifier(
        criterion=criterion,
        splitter=splitter,
        max_depth=max_depth if max_depth != 0 else None,
        random_state=42,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        max_leaf_nodes=max_leaf_nodes if max_leaf_nodes != 0 else None,
        min_impurity_decrease=min_impurity_decrease,
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    XX, YY, input_array = draw_meshgrid()
    labels = clf.predict(input_array)

    ax.contourf(XX, YY, labels.reshape(XX.shape), alpha=0.5, cmap='rainbow')
    plt.xlabel("Col1")
    plt.ylabel("Col2")
    st.pyplot(fig)

    st.subheader(f"Accuracy for Decision Tree: {round(accuracy_score(y_test, y_pred), 2)}")

    dot_data = export_graphviz(clf, feature_names=["Col1", "Col2"])
    st.graphviz_chart(dot_data)