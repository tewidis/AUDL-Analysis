#!/usr/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from xgboost import plot_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    # read in the processed data
    df = pd.read_csv('/home/twidis/ultianalytics/data/all_data.csv');

    # split into features and values
    X = df.iloc[:,5:14];
    Y = df.iloc[:,14];

    # split into training and test datasets
    seed = 7;
    test_size = 0.2;
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state = seed);

    # fit the model with the training data
    model = XGBClassifier();
    model.fit(x_train, y_train);

    # make predictions for test data
    y_pred = model.predict(x_test);
    predictions = [round(value) for value in y_pred];

    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions);
    print('Accuracy: %.2f%%' % (accuracy * 100.0))

    # get the feature importances
    plot_importance(model);
    plt.savefig('/home/twidis/ultianalytics/plots/feature_importances_xgboost.png', bbox_inches='tight');

if __name__ == "__main__":
    main();
