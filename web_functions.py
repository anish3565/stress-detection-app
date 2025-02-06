"""This module contains necessary function needed"""

# Import necessary modules
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import streamlit as st


@st.cache_data
def load_data():
    """This function returns the preprocessed data"""
    df = pd.read_csv('Stress.csv')
    df.rename(columns={"t": "bt"}, inplace=True)
    
    # Perform feature and target split
    X = df[["sr", "rr", "bt", "lm", "bo", "rem", "sh", "hr"]]
    y = df['sl']
    return df, X, y


@st.cache_resource
def train_model(X, y):
    """This function trains the model and returns the model and model score"""
    model = DecisionTreeClassifier(
        criterion='entropy', max_depth=4, random_state=42
    )
    model.fit(X, y)
    score = model.score(X, y)
    return model, score

def predict(X, y, features):
    # Get model and model score
    model, score = train_model(X, y)
    # Predict the value
    prediction = model.predict(np.array(features).reshape(1, -1))

    return prediction, score
