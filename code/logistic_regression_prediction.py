import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    # read in the processed data
    df = pd.read_csv('/home/twidis/ultianalytics/data/combined_data.csv');

    # split into features and values
    X = df.iloc[:,4:13];
    Y = df.iloc[:,13];

    # split into training and test datasets
    seed = 7;
    test_size = 0.2;
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state = seed);

    # fit the model with the training data
    model = LogisticRegression(solver='liblinear');
    model.fit(x_train, y_train);

    # make predictions for test data
    y_pred = model.predict(x_test);
    predictions = [round(value) for value in y_pred];

    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions);
    print('Accuracy: %.2f%%' % (accuracy * 100.0))

if __name__ == "__main__":
    main();
