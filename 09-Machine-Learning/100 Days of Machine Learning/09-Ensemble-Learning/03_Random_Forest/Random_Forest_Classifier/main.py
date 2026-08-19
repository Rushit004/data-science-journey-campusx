import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.metrics import accuracy_score
import pandas as pd
from pathlib import Path

def draw_meshgrid():
    a = np.arange(start=X[:, 0].min() - 1, stop=X[:, 0].max() + 1, step=0.01)
    b = np.arange(start=X[:, 1].min() - 1, stop=X[:, 1].max() + 1, step=0.01)
    XX, YY = np.meshgrid(a, b)
    input_array = np.array([XX.ravel(), YY.ravel()]).T
    return XX, YY, input_array



BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "concertriccir2.csv")
X = df.iloc[:, 0:2].values
y = df.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

plt.style.use('fivethirtyeight')
st.sidebar.markdown("# Random Forest Classifier")

n_estimators = int(
    st.sidebar.number_input('Num Estimators', min_value=1, max_value=1000, value=100, step=10)
)

# 'auto' was removed in scikit-learn 1.3 (deprecated since 1.1); valid options
# now are 'sqrt', 'log2', None, or an int/float you set manually.
max_features_choice = st.sidebar.selectbox(
    'Max Features',
    ('sqrt', 'log2', 'None', 'manual')
)

if max_features_choice == 'manual':
    max_features = int(st.sidebar.number_input('Max Features', min_value=1, max_value=X_train.shape[1], value=1))
elif max_features_choice == 'None':
    max_features = None
else:
    max_features = max_features_choice

bootstrap = st.sidebar.selectbox('Bootstrap', (True, False))  # returns real bool, not string

# max_samples is only valid when bootstrap=True; sklearn raises an error otherwise
if bootstrap:
    max_samples = st.sidebar.slider('Max Samples', 1, X_train.shape[0], X_train.shape[0], key="1236")
else:
    max_samples = None
    st.sidebar.caption("Max Samples disabled (requires Bootstrap = True)")

# Load initial graph
fig, ax = plt.subplots()
ax.scatter(X.T[0], X.T[1], c=y, cmap='rainbow')
orig = st.pyplot(fig)

if st.sidebar.button('Run Algorithm'):
    orig.empty()

    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=42,
        bootstrap=bootstrap,
        max_samples=max_samples,
        max_features=max_features
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    XX, YY, input_array = draw_meshgrid()
    labels = clf.predict(input_array)

    fig, ax = plt.subplots()
    ax.contourf(XX, YY, labels.reshape(XX.shape), alpha=0.5, cmap='rainbow')
    ax.scatter(X.T[0], X.T[1], c=y, cmap='rainbow')
    plt.xlabel("Col1")
    plt.ylabel("Col2")

    st.pyplot(fig)
    st.header("Accuracy - " + str(round(accuracy_score(y_test, y_pred), 2)))